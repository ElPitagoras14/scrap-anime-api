import logging
import os
import uuid
from typing import Union
from fastapi import APIRouter, Response

from utils.responses import InternalServerErrorResponse, SuccessResponse
from .service import (
    get_anime_info,
    get_streaming_links_controller,
    get_single_download_link_controller,
    get_download_links_controller,
    get_saved_anime_controller,
    get_single_saved_anime_controller,
    save_saved_anime_controller,
    delete_saved_anime_controller,
    search_anime_query,
)
from .schemas import Saved
from .responses import (
    AnimeCardListOut,
    AnimeDownloadLinksOut,
    AnimeLinksOut,
    AnimeOut,
    DownloadLinkOut,
    SavedListOut,
    SavedOut,
)

anime_router = APIRouter()

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


@anime_router.get(
    "/info/{anime}",
    response_model=Union[AnimeOut, InternalServerErrorResponse],
)
async def get_anime(anime: str, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Getting anime information for {anime}")
        anime_info = await get_anime_info(anime, uuid_str)
        return AnimeOut(
            func="get_anime",
            message="Anime information retrieved",
            payload=anime_info,
        )
    except Exception as e:
        logger.error(
            f"{uuid_str} | Error getting anime information for {anime}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(message=str(e), func="get_anime")


@anime_router.get(
    "/search",
    response_model=Union[AnimeCardListOut, InternalServerErrorResponse],
)
async def search_anime(query: str, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Searching for anime with query: {query}")
        anime_card_list = await search_anime_query(query, uuid_str)
        return AnimeCardListOut(
            func="search_anime",
            message="Anime search results retrieved",
            payload=anime_card_list,
        )
    except Exception as e:
        logger.error(
            f"{uuid_str} | Error searching for anime with query: {query}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(message=str(e), func="search_anime")


@anime_router.get(
    "/streamlinks/{anime}",
    response_model=Union[AnimeLinksOut, InternalServerErrorResponse],
)
async def get_anime_streaming_links(anime: str, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Getting anime stream links for {anime}")
        anime_links = await get_streaming_links_controller(anime, uuid_str)
        return AnimeLinksOut(
            func="get_anime_links",
            message="Anime links retrieved",
            payload=anime_links,
        )
    except Exception as e:
        logger.error(
            f"{uuid_str} | Error getting anime stream links for {anime}: {e}"
        )
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
    anime_name = None
    uuid_str = str(uuid.uuid4())
    try:
        anime_name = "-".join(
            episode_links[0]["link"].split("/")[-1].split("-")[:-1]
        )
        logger.info(
            f"{uuid_str} | Getting anime download links for {anime_name} "
            + f"with range {episode_range}"
        )
        anime_links = await get_download_links_controller(
            episode_links, episode_range, uuid_str
        )
        return AnimeDownloadLinksOut(
            func="get_anime_download_links",
            message="Anime download links retrieved",
            payload=anime_links,
        )
    except Exception as e:
        logger.error(
            f"Error getting anime download links for {anime_name} "
            + f"with range {episode_range}: {e}"
        )
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
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(
            f"{uuid_str} | Getting single download link for {episode_link}"
        )
        download_link = await get_single_download_link_controller(
            episode_link, episode_id, uuid_str
        )
        return DownloadLinkOut(
            func="get_single_download_link",
            message="Single download link retrieved",
            payload=download_link,
        )
    except Exception as e:
        logger.error(
            f"Error getting single download link for {episode_link}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_single_download_link"
        )


@anime_router.get(
    "/saved",
    response_model=Union[SavedListOut, InternalServerErrorResponse],
)
async def get_saved_anime(response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Getting all saved animes")
        saved = await get_saved_anime_controller(uuid_str)
        return SavedListOut(
            func="get_saved_anime",
            message="Saved anime retrieved",
            payload=saved,
        )
    except Exception as e:
        logger.error(f"{uuid_str} | Error getting saved anime: {e}")
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_saved_anime"
        )


@anime_router.get(
    "/saved/{anime_id}",
    response_model=Union[SavedOut, InternalServerErrorResponse],
)
async def get_single_saved_anime(anime_id: str, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(
            f"{uuid_str} | Getting single saved anime with id: {anime_id}"
        )
        saved = await get_single_saved_anime_controller(anime_id, uuid_str)
        return SavedOut(
            func="get_single_saved_anime",
            message="Saved anime retrieved",
            payload=saved,
        )
    except Exception as e:
        logger.error(
            f"Error getting single saved anime with id: {anime_id}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="get_single_saved_anime"
        )


@anime_router.post(
    "/saved",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def save_saved_anime(anime: Saved, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Saving anime with id: {anime.anime_id}")
        save_response = await save_saved_anime_controller(anime, uuid_str)
        if not save_response:
            raise Exception("Error saving anime history")
        return SuccessResponse(
            func="save_saved_anime",
            message="Anime saved",
        )
    except Exception as e:
        logger.error(
            f"{uuid_str} | Error saving anime with id: {anime.anime_id}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="save_saved_anime"
        )


@anime_router.delete(
    "/saved/single/{anime_id}",
    response_model=Union[SuccessResponse, InternalServerErrorResponse],
)
async def delete_saved_anime(anime_id: str, response: Response):
    uuid_str = str(uuid.uuid4())
    try:
        logger.info(f"{uuid_str} | Deleting saved anime with id: {anime_id}")
        delete_response = delete_saved_anime_controller(anime_id, uuid_str)
        if not delete_response:
            raise Exception("Error deleting anime history")
        return SuccessResponse(
            func="delete_saved_anime",
            message="Anime deleted",
        )
    except Exception as e:
        logger.error(
            f"{uuid_str} | Error deleting saved anime with id: {anime_id}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(
            message=str(e), func="delete_saved_anime"
        )
