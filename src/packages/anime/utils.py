from .responses import (
    Anime,
    AnimeCard,
    AnimeCardList,
    AnimeDownloadLinks,
    AnimeLinks,
    DownloadLink,
    Episode,
)
from .schemas import Download


def cast_anime_info(title: str, cover: str, finished: str, description: str):
    is_finished = finished == "Finalizado"
    parsed_description = description.replace("\n", "").strip()
    return Anime(
        name=title,
        finished=is_finished,
        description=parsed_description,
        image_src=cover,
    )


def cast_anime_card_list(anime_card_list: list[dict]):
    return AnimeCardList(
        items=[
            AnimeCard(
                title=anime["title"],
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
                name=episode["name"],
                link=episode["link"],
                episode_id=idx + 1,
            )
            for idx, episode in enumerate(streaming_links)
        ],
        total=len(streaming_links),
    )


def cast_single_anime_download_link(
    episode_name: str, download_link: str, episode_id: int
):
    return DownloadLink(
        name=episode_name,
        link=download_link,
        episode_id=episode_id,
    )


def cast_anime_download_links(download_links: list[dict]):
    return AnimeDownloadLinks(
        name=download_links["anime"],
        episodes=[
            cast_single_anime_download_link(
                episode["name"],
                episode["download_link"],
                episode["episode"],
            )
            for episode in download_links["download_links"]
        ],
        total=len(download_links),
    )


def cast_download_history(download_history: list[dict]):
    return [
        Download(
            id=history.id,
            date=history.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            file_url=history.file_url,
            file_name=history.file_name,
            anime=history.anime,
            episode_id=history.episode_id,
            description=history.description,
            image_src=history.image_src,
            progress=history.progress,
            total_size=history.total_size,
        )
        for history in download_history
    ]
