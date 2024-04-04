import asyncio
import aiohttp
from bs4 import BeautifulSoup

from .config import anime_settings
from .utils import (
    cast_anime_card_list,
    cast_anime_download_links,
    cast_anime_info,
    cast_anime_streaming_links,
    cast_single_anime_download_link,
)
from libraries.scraper import (
    get_streaming_links,
    get_download_links,
    get_single_episode_download_link,
)

HOST = anime_settings.HOST


def get_anime_cards(page: str):
    soup = BeautifulSoup(page, "html.parser")
    anime_list = []
    anime_container = soup.find_all(
        "ul", class_="ListAnimes AX Rows A03 C02 D02"
    )[0].find_all("li")
    for anime in anime_container:
        title = anime.find("h3").text
        anime_id = anime.find("a")["href"].split("/")[-1]
        cover = anime.find("img")["src"]
        cover_url = cover
        anime_list.append(
            {"title": title, "cover_url": cover_url, "anime_id": anime_id}
        )
    return anime_list


async def get_anime_info(anime: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(HOST + f"/anime/{anime}") as response:
            page = await response.text()
            soup = BeautifulSoup(page, "html.parser")
            title = soup.find("h1").text
            cover = soup.find_all("div", class_="AnimeCover")[0].find("img")[
                "src"
            ]
            cover_url = HOST + cover
            finished = soup.find_all("p", class_="AnmStts")[0].text
            description = soup.find_all("div", class_="Description")[0].text
            anime_info = cast_anime_info(
                title, cover_url, finished, description
            )
            return anime_info


async def search_anime_query(query: str):
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
            return anime_card_list


async def get_streaming_links_controller(anime: str):
    task = asyncio.create_task(get_streaming_links(anime))
    streaming_links = await asyncio.gather(task)
    streaming_links = streaming_links[0]
    casted_streaming_links = cast_anime_streaming_links(anime, streaming_links)
    return casted_streaming_links


async def get_download_links_controller(
    episode_links: list[dict], episode_range: str = None
):
    task = asyncio.create_task(
        get_download_links(episode_links, episode_range)
    )
    download_links = await asyncio.gather(task)
    download_links = download_links[0]
    print(download_links)
    casted_streaming_links = cast_anime_download_links(download_links)
    return casted_streaming_links


async def get_single_download_link_controller(
    episode_link: str, episode_id: int
):
    name = "-".join(episode_link.split("/")[-1].split("-")[:-1])
    task = asyncio.create_task(get_single_episode_download_link(episode_link))
    download_link = await asyncio.gather(task)
    download_link = download_link[0]
    return cast_single_anime_download_link(name, download_link, episode_id)
