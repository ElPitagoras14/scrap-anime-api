from typing import Union
from fastapi import APIRouter, Response

from utils.responses import InternalServerErrorResponse, SuccessResponse
from .service import (
    delete_all_episode_download_controller,
    get_anime_info,
    get_streaming_links_controller,
    get_single_download_link_controller,
    get_download_links_controller,
    delete_episode_download_controller,
    get_download_history_controller,
    save_download_history_controller,
    get_saved_anime_controller,
    get_single_saved_anime_controller,
    save_saved_anime_controller,
    delete_saved_anime_controller,
    search_anime_query,
)
from .schemas import Download, Saved
from .responses import (
    AnimeCardListOut,
    AnimeDownloadLinksOut,
    AnimeLinksOut,
    AnimeOut,
    DownloadLinkOut,
    DownloadListOut,
    SavedListOut,
    SavedOut,
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


@anime_router.get(
    "/history",
    response_model=Union[DownloadListOut, InternalServerErrorResponse],
)
async def get_download_history(response: Response):
    try:
        history = get_download_history_controller()
        return DownloadListOut(
            func="get_download_history",
            message="Anime history retrieved",
            payload=history,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_download_history"
        )


@anime_router.post(
    "/history",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def save_download_history(anime: Download, response: Response):
    try:
        save_response = save_download_history_controller(anime)
        if not save_response:
            raise Exception("Error saving anime history")
        return SuccessResponse(
            func="save_download_history",
            message="Anime history saved",
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="save_download_history"
        )


@anime_router.delete(
    "/history/all",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def delete_all_download_history(response: Response):
    try:
        delete_response = delete_all_episode_download_controller()
        if not delete_response:
            raise Exception("Error deleting anime history")
        return SuccessResponse(
            func="delete_all_anime_history",
            message="Anime history deleted",
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="delete_all_anime_history"
        )


@anime_router.delete(
    "/history/single/{anime_id}",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def delete_download_history(anime_id: str, response: Response):
    try:
        delete_response = delete_episode_download_controller(anime_id)
        if not delete_response:
            raise Exception("Error deleting anime history")
        return SuccessResponse(
            func="delete_anime_history",
            message="Anime history deleted",
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="delete_anime_history"
        )


@anime_router.get(
    "/saved",
    response_model=Union[SavedListOut, InternalServerErrorResponse],
)
async def get_saved_anime(response: Response):
    try:
        saved = get_saved_anime_controller()
        return SavedListOut(
            func="get_saved_anime",
            message="Saved anime retrieved",
            payload=saved,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_saved_anime"
        )


@anime_router.get(
    "/saved/{anime_id}",
    response_model=Union[SavedOut, InternalServerErrorResponse],
)
async def get_single_saved_anime(anime_id: str, response: Response):
    try:
        saved = get_single_saved_anime_controller(anime_id)
        return SavedOut(
            func="get_single_saved_anime",
            message="Saved anime retrieved",
            payload=saved,
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_single_saved_anime"
        )


@anime_router.post(
    "/saved",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def save_saved_anime(episode: Saved, response: Response):
    try:
        save_response = save_saved_anime_controller(episode)
        if not save_response:
            raise Exception("Error saving anime history")
        return SuccessResponse(
            func="save_saved_anime",
            message="Anime saved",
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="save_saved_anime"
        )


@anime_router.delete(
    "/saved/single/{anime_id}",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def delete_saved_anime(anime_id: str, response: Response):
    try:
        delete_response = delete_saved_anime_controller(anime_id)
        if not delete_response:
            raise Exception("Error deleting anime history")
        return SuccessResponse(
            func="delete_saved_anime",
            message="Anime deleted",
        )
    except Exception as e:
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="delete_saved_anime"
        )
