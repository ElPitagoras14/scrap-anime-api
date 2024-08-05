from datetime import datetime

from .responses import (
    Anime,
    AnimeCard,
    AnimeCardList,
    AnimeDownloadLinks,
    AnimeLinks,
    DownloadLink,
    Episode,
    SavedList,
)
from .schemas import Saved


def cast_anime_info(
    name: str, cover: str, finished: str, description: str, emission_date: str
):
    is_finished = finished == "Finalizado"
    parsed_description = description.replace("\n", "").strip()
    week_day = None
    if emission_date:
        week_day = datetime.strptime(emission_date, "%Y-%m-%d")
        week_day = week_day.strftime("%A")
    return Anime(
        name=name,
        finished=is_finished,
        description=parsed_description,
        image_src=cover,
        weekDay=week_day,
    )


def cast_anime_card_list(anime_card_list: list[dict]):
    return AnimeCardList(
        items=[
            AnimeCard(
                name=anime["name"],
                image_src=anime["cover_url"],
                anime_id=anime["anime_id"],
            )
            for anime in anime_card_list
        ],
        total=len(anime_card_list),
    )


def cast_anime_streaming_links(anime_name: str, streaming_links: list[dict]):
    return AnimeLinks(
        name=anime_name,
        episodes=[
            Episode(
                title=episode["title"],
                link=episode["link"],
                episode_id=idx + 1,
            )
            for idx, episode in enumerate(streaming_links)
        ],
        total=len(streaming_links),
    )


def cast_single_anime_download_link(title: str, link: str, episode_id: int):
    return DownloadLink(
        title=title,
        link=link,
        episode_id=episode_id,
    )


def cast_anime_download_links(download_links: dict):
    return AnimeDownloadLinks(
        name=download_links["anime"],
        episodes=[
            cast_single_anime_download_link(
                episode["title"], episode["download_link"], episode["episode"]
            )
            for episode in download_links["download_links"]
        ],
        total=len(download_links),
    )


def cast_single_saved_anime(saved_anime: dict):
    return Saved(
        animeId=saved_anime.anime_id,
        name=saved_anime.name,
        imageSrc=saved_anime.image_src,
        weekDay=saved_anime.week_day,
    )


def cast_saved_anime_list(saved_animes: list[dict]):
    return SavedList(
        items=[cast_single_saved_anime(anime) for anime in saved_animes],
        total=len(saved_animes),
    )
