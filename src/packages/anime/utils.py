from .responses import (
    Anime,
    AnimeCard,
    AnimeCardList,
    AnimeDownloadLinks,
    AnimeLinks,
    DownloadLink,
    DownloadList,
    Episode,
    SavedList,
)
from .schemas import Download, Saved


def cast_anime_info(name: str, cover: str, finished: str, description: str):
    is_finished = finished == "Finalizado"
    parsed_description = description.replace("\n", "").strip()
    return Anime(
        name=name,
        finished=is_finished,
        description=parsed_description,
        image_src=cover,
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


def cast_single_download(download: dict):
    return Download(
        id=download.id,
        date=download.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        file_url=download.file_url,
        file_name=download.file_name,
        anime=download.anime,
        episode_id=download.episode_id,
        title=download.title,
        image_src=download.image_src,
        progress=download.progress,
        total_size=download.total_size,
    )


def cast_download_list(downloads: list[dict]):
    return DownloadList(
        items=[cast_single_download(history) for history in downloads],
        total=len(downloads),
    )


def cast_single_saved_anime(saved_anime: dict):
    return Saved(
        animeId=saved_anime.anime_id,
        name=saved_anime.name,
        imageSrc=saved_anime.image_src,
    )


def cast_saved_anime(saved_animes: list[dict]):
    return SavedList(
        items=[cast_single_saved_anime(anime) for anime in saved_animes],
        total=len(saved_animes),
    )
