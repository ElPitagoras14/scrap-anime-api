from typing import Union
from fastapi import APIRouter, Response

from utils.responses import InternalServerErrorResponse
from .service import (
    get_anime_info,
    get_download_links_controller,
    get_single_download_link_controller,
    get_streaming_links_controller,
    search_anime_query,
)
from .responses import (
    AnimeCardListOut,
    AnimeDownloadLinksOut,
    AnimeLinksOut,
    AnimeOut,
    DownloadLinkOut,
)

anime_router = APIRouter()


@anime_router.get(
    "/info/{anime}",
    response_model=Union[AnimeOut, InternalServerErrorResponse],
)
async def get_anime(anime: str, response: Response):
    try:
        anime_info = await get_anime_info(anime)
        return AnimeOut(
            func="get_anime",
            message="Anime information retrieved",
            payload=anime_info,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(message=str(e), func="get_anime")


@anime_router.get(
    "/search",
    response_model=Union[AnimeCardListOut, InternalServerErrorResponse],
)
async def search_anime(query: str, response: Response):
    try:
        anime_card_list = await search_anime_query(query)
        return AnimeCardListOut(
            func="search_anime",
            message="Anime search results retrieved",
            payload=anime_card_list,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(message=str(e), func="search_anime")


@anime_router.get(
    "/streamlinks/{anime}",
    response_model=Union[AnimeLinksOut, InternalServerErrorResponse],
)
async def get_anime_streaming_links(anime: str, response: Response):
    try:
        anime_links = await get_streaming_links_controller(anime)
        print("Terminé de obtener los links")
        return AnimeLinksOut(
            func="get_anime_links",
            message="Anime links retrieved",
            payload=anime_links,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_anime_links"
        )


@anime_router.post(
    "/downloadlinks/range",
    response_model=Union[AnimeDownloadLinksOut, InternalServerErrorResponse],
)
async def get_anime_download_links(
    episode_links: list[dict],
    response: Response,
    episode_range: str = None,
):
    try:
        anime_links = await get_download_links_controller(
            episode_links, episode_range
        )
        return AnimeDownloadLinksOut(
            func="get_anime_download_links",
            message="Anime download links retrieved",
            payload=anime_links,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_anime_links"
        )


@anime_router.post(
    "/downloadlinks/single",
    response_model=Union[DownloadLinkOut, InternalServerErrorResponse],
)
async def get_single_download_link(
    episode_link: str, episode_id: int, response: Response
):
    try:
        download_link = await get_single_download_link_controller(
            episode_link, episode_id
        )
        print("Terminé de obtener el download link")
        return DownloadLinkOut(
            func="get_single_download_link",
            message="Single download link retrieved",
            payload=download_link,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_single_download_link"
        )
