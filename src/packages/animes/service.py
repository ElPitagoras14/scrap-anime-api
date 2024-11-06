import aiohttp
from loguru import logger
from datetime import datetime, timezone
from bs4 import BeautifulSoup

from libraries.animeflv_scraper import (
    get_streaming_links,
    get_single_episode_download_link,
    get_range_episodes_download_links,
    get_emission_date,
)
from databases.mysql import DatabaseSession, Anime, Episode

from .utils import (
    cast_anime_card_list,
    cast_anime_download_links,
    cast_anime_info,
    cast_anime_streaming_links,
    cast_single_anime_download_link,
)

HOST = "https://www3.animeflv.net"


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


async def get_anime_info_controller(anime: str):
    anime_info = None
    with DatabaseSession() as db:
        anime_info = db.query(Anime).filter(Anime.id == anime).first()

        if anime_info:
            anime_is_finished = anime_info.is_finished
            anime_week_day = anime_info.week_day
            anime_last_peek = anime_info.last_peek
            today = datetime.now(timezone.utc)
            today_weekday = today.strftime("%A")

            anime_info.last_peek = datetime.now(timezone.utc)

            if (
                anime_is_finished
                or not anime_week_day
                or anime_week_day != today_weekday
                or (today - anime_last_peek).days > 7
            ):
                logger.info(f"Found anime {anime} in cache database")
                anime_response = cast_anime_info(
                    anime_info.name,
                    anime_info.image_src,
                    anime_info.is_finished,
                    anime_info.description,
                    anime_info.week_day,
                )
                return anime_response

        async with aiohttp.ClientSession() as session:
            async with session.get(HOST + f"/anime/{anime}") as response:
                page = await response.text()
                soup = BeautifulSoup(page, "html.parser")
                name = soup.find("h1").text
                cover = soup.find_all("div", class_="AnimeCover")[0].find(
                    "img"
                )["src"]
                cover_url = HOST + cover
                is_finished = soup.find_all("p", class_="AnmStts")[0].text
                is_finished = is_finished == "Finalizado"
                description = soup.find_all("div", class_="Description")[
                    0
                ].text
                parsed_description = description.replace("\n", "").strip()

                week_day = None
                anime_response = None
                new_anime = None
                if anime_info:
                    if is_finished:
                        anime_info.is_finished = True
                        anime_info.week_day = None
                    anime_response = cast_anime_info(
                        name, cover_url, is_finished, description, week_day
                    )
                    logger.info(f"Updated anime {anime} in cache database")

                    db.commit()
                    db.refresh(anime_info)

                else:
                    if not is_finished:
                        week_day = await get_emission_date(anime)
                    new_anime = Anime(
                        id=anime,
                        name=name,
                        description=parsed_description,
                        image_src=cover_url,
                        is_finished=is_finished,
                        week_day=week_day,
                        last_peek=datetime.now(timezone.utc),
                    )
                    db.add(new_anime)
                    db.commit()
                    db.refresh(new_anime)

                    anime_response = cast_anime_info(
                        name,
                        cover_url,
                        is_finished,
                        parsed_description,
                        week_day,
                    )
                    logger.info(f"Found anime {anime} in animeflv")

                return anime_response


async def search_anime_query_controller(query: str):
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
                f"Found {anime_card_list.total} anime with query: {query}"
            )
            return anime_card_list


async def get_streaming_links_controller(anime_name: str):
    with DatabaseSession() as db:
        last_episode = None
        anime = db.query(Anime).filter(Anime.id == anime_name).first()
        if not anime:
            await get_anime_info_controller(anime_name)

    with DatabaseSession() as db:
        anime = db.query(Anime).filter(Anime.id == anime_name).first()
        anime_id = anime.id

        last_episode = (
            db.query(Episode)
            .filter(Episode.anime_id == anime_id)
            .order_by(Episode.id.desc())
            .first()
        )
        last_episode_name = last_episode.name if last_episode else None
        new_stream_links = await get_streaming_links(
            anime_name, last_episode_name
        )

        streaming_links = (
            db.query(Episode)
            .filter(Episode.anime_id == anime_id)
            .order_by(Episode.id)
            .all()
        )
        if new_stream_links:
            stream_to_add = []
            for idx, stream in enumerate(new_stream_links):
                stream_to_add.append(
                    Episode(
                        anime_id=anime_id,
                        episode_id=idx + len(streaming_links) + 1,
                        name=stream["name"],
                        link=stream["link"],
                    )
                )
            db.add_all(stream_to_add)
            db.commit()
            streaming_links += stream_to_add
        logger.info(
            f"Found {len(streaming_links)} streaming links for {anime.name}"
        )
        return cast_anime_streaming_links(anime.name, streaming_links)


async def get_range_episodes_download_links_controller(
    episode_links: list[dict],
    episode_range: str,
):
    download_links = await get_range_episodes_download_links(
        episode_links, episode_range
    )
    not_valid_cnt = 0
    for episode in download_links["download_links"]:
        if not episode:
            not_valid_cnt += 1
    logger.info(
        f"Found {len(download_links["download_links"]) - not_valid_cnt} "
        + f"download links for {download_links["anime"]}"
    )
    return cast_anime_download_links(download_links)


async def get_single_episode_download_link_controller(
    episode_link: str, episode_id: int
):
    name = "-".join(episode_link.split("/")[-1].split("-")[:-1])

    download_link = await get_single_episode_download_link(episode_link)

    logger.info(
        f"Found download link for {name} episode {episode_id}: {download_link}"
    )
    if not download_link:
        return None

    return cast_single_anime_download_link(name, download_link, episode_id)
