import asyncio
import aiohttp
import os
import logging
from bs4 import BeautifulSoup

from libraries.scraper import (
    async_get_streaming_links,
    async_get_download_links,
    async_get_single_episode_download_link,
    async_get_emission_date,
)
from ..redis import redis_client, SavedRedis

from .config import anime_settings
from .utils import (
    cast_anime_card_list,
    cast_anime_download_links,
    cast_anime_info,
    cast_anime_streaming_links,
    cast_saved_anime_list,
    cast_single_anime_download_link,
    cast_single_saved_anime,
)
from .schemas import Saved

HOST = anime_settings.HOST

curr_workspace = os.getcwd()
proj_dir = os.path.dirname(curr_workspace)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"{proj_dir}/anime-scraper.log")
file_handler.setFormatter(
    logging.Formatter(
        fmt="%(name)s | %(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def get_anime_cards(page: str):
    soup = BeautifulSoup(page, "html.parser")
    anime_list = []
    anime_container = soup.find_all(
        "ul", class_="ListAnimes AX Rows A03 C02 D02"
    )[0].find_all("li")
    for anime in anime_container:
        name = anime.find("h3").text
        anime_id = anime.find("a")["href"].split("/")[-1]
        cover = anime.find("img")["src"]
        cover_url = cover
        anime_list.append(
            {"name": name, "cover_url": cover_url, "anime_id": anime_id}
        )
    return anime_list


async def get_anime_info(anime: str, uuid_str: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST + f"/anime/{anime}") as response:
            page = await response.text()
            soup = BeautifulSoup(page, "html.parser")
            name = soup.find("h1").text
            cover = soup.find_all("div", class_="AnimeCover")[0].find("img")[
                "src"
            ]
            cover_url = HOST + cover
            finished = soup.find_all("p", class_="AnmStts")[0].text
            description = soup.find_all("div", class_="Description")[0].text
            emission_date = None
            if finished == "En emision":
                emission_date = await async_get_emission_date(anime)
            anime_info = cast_anime_info(
                name, cover_url, finished, description, emission_date
            )
            logger.info(f"{uuid_str} | Found anime information for {anime}")
            return anime_info


async def search_anime_query(query: str, uuid_str: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST + f"/browse?q={query}") as response:
            page = await response.text()
            soup = BeautifulSoup(page, "html.parser")
            pagination = soup.find_all("div", class_="NvCnAnm")[0]
            total = int(len(pagination.find_all("li"))) - 2
            anime_list = []
            anime_list += get_anime_cards(page)

            if total > 1:
                for i in range(2, total + 1):
                    async with session.get(
                        HOST + f"/browse?q={query}&page={i}"
                    ) as response:
                        page = await response.text()
                        anime_list += get_anime_cards(page)
            anime_card_list = cast_anime_card_list(anime_list)
            logger.info(
                f"{uuid_str} | Found {len(anime_card_list.items)} anime cards "
                + f"for query: {query}"
            )
            return anime_card_list


async def get_streaming_links_controller(anime: str, uuid_str: str):
    task = asyncio.create_task(async_get_streaming_links(anime, uuid_str))
    streaming_links = await asyncio.gather(task)
    streaming_links = streaming_links[0]
    logger.info(
        f"{uuid_str} | Found {len(streaming_links)} streaming links for {anime}"
    )
    return cast_anime_streaming_links(anime, streaming_links)


async def get_download_links_controller(
    episode_links: list[dict],
    episode_range: str,
    uuid_str: str,
):
    task = asyncio.create_task(
        async_get_download_links(episode_links, episode_range, uuid_str)
    )
    download_links = await asyncio.gather(task)
    download_links = download_links[0]
    logger.info(
        f"{uuid_str} | Found {len(download_links['download_links'])} "
        + f"download links for {download_links['anime']}"
    )
    filtered_links = {
        "anime": download_links["anime"],
        "download_links": [
            episode
            for episode in download_links["download_links"]
            if episode["download_link"]
        ],
    }
    return cast_anime_download_links(filtered_links)


async def get_single_download_link_controller(
    episode_link: str, episode_id: int, uuid_str: str
):
    name = "-".join(episode_link.split("/")[-1].split("-")[:-1])
    task = asyncio.create_task(
        async_get_single_episode_download_link(episode_link, uuid_str)
    )
    download_link = await asyncio.gather(task)
    download_link = download_link[0]
    logger.info(
        f"{uuid_str} | Found download link for {name} "
        + f"episode {episode_id}: {download_link}"
    )
    if not download_link:
        return None
    return cast_single_anime_download_link(name, download_link, episode_id)


async def get_saved_anime_controller(uuid_str: str):
    saved = SavedRedis.find().all()
    logger.info(f"{uuid_str} | Found {len(saved)} saved anime")
    return cast_saved_anime_list(saved)


async def get_single_saved_anime_controller(anime_id: str, uuid_str: str):
    saved = SavedRedis.find(SavedRedis.anime_id == anime_id).all()
    if saved:
        saved = saved[0]
    logger.info(f"{uuid_str} | Found saved anime {anime_id}")
    return cast_single_saved_anime(saved) if saved else None


async def save_saved_anime_controller(anime: Saved, uuid_str: str):
    week_day = anime.week_day
    if not week_day:
        anime_info = await get_anime_info(anime.anime_id, uuid_str)
        week_day = anime_info.week_day
    saved_redis = SavedRedis(
        anime_id=anime.anime_id,
        name=anime.name,
        image_src=anime.image_src,
        week_day=str(week_day),
    )
    saved_redis.save()
    exists = SavedRedis.find(SavedRedis.anime_id == anime.anime_id).count()
    redis_client.execute_command("BGSAVE")
    logger.info(f"{uuid_str} | Saved anime {anime.anime_id}")
    return exists == 1


def delete_saved_anime_controller(anime_id: str, uuid_str: str):
    SavedRedis.delete(anime_id)
    exists = SavedRedis.find(SavedRedis.anime_id == anime_id).count()
    redis_client.execute_command("BGSAVE")
    logger.info(f"{uuid_str} | Deleted saved anime {anime_id}")
    return exists == 0
