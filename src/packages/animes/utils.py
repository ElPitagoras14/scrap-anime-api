from databases.mysql import Episode

from .responses import (
    Anime,
    AnimeCard,
    AnimeCardList,
    AnimeDownloadLink,
    AnimeDownloadLinkList,
    AnimeStreamingLinks,
    Link,
)


def cast_anime_info(
    name: str,
    cover_url: str,
    is_finished: bool,
    description: str,
    week_day: str,
):
    return Anime(
        name=name,
        is_finished=is_finished,
        description=description,
        image_src=cover_url,
        week_day=week_day,
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


def cast_anime_streaming_links(
    anime_name: str, streaming_links: list[Episode]
):
    return AnimeStreamingLinks(
        name=anime_name,
        episodes=[
            Episode(
                name=episode.name,
                link=episode.link,
                episode_id=episode.episode_id,
            )
            for episode in streaming_links
        ],
        total=len(streaming_links),
    )


def cast_single_anime_download_link(
    name: str, download_info: str, episode_id: int
):
    link = (
        Link(
            service=download_info["service"],
            link=download_info["link"],
        )
        if download_info
        else None
    )
    return AnimeDownloadLink(
        name=name,
        download_info=link,
        episode_id=episode_id,
    )


def cast_anime_download_links(download_links: dict):
    return AnimeDownloadLinkList(
        name=download_links["anime"],
        episodes=[
            cast_single_anime_download_link(
                episode["name"],
                episode["download_info"],
                episode["episode"],
            )
            for episode in download_links["download_links"]
        ],
        total=len(download_links["download_links"]),
    )
