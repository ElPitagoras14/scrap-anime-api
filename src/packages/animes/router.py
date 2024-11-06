import os
import time
from typing import Union
from fastapi import APIRouter, Request, Response
from loguru import logger

from utils.responses import InternalServerErrorResponse
from .service import (
    get_anime_info_controller,
    get_streaming_links_controller,
    get_single_episode_download_link_controller,
    get_range_episodes_download_links_controller,
    search_anime_query_controller,
)
from .responses import (
    AnimeCardListOut,
    AnimeDownloadLinkListOut,
    AnimeDownloadLinkOut,
    AnimeStreamingLinksOut,
    AnimeOut,
)

animes_router = APIRouter()

curr_workspace = os.getcwd()
proj_dir = os.path.dirname(curr_workspace)


@animes_router.get(
    "/info/{anime}",
    response_model=Union[AnimeOut, InternalServerErrorResponse],
)
async def get_anime_info(anime: str, response: Response, request: Request):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Getting anime information for {anime}")
        anime_info = await get_anime_info_controller(anime)
        process_time = time.time() - start_time
        logger.info(
            f"Got anime information for {anime} in {process_time:.2f} seconds"
        )
        return AnimeOut(
            request_id=request_id,
            process_time=process_time,
            func="get_anime_info",
            message="Anime information retrieved",
            payload=anime_info,
        )
    except Exception as e:
        logger.error(f"Error getting anime information for {anime}: {e}")
        response.status_code = 500
        return InternalServerErrorResponse(
            request_id=request_id, message=str(e), func="get_anime_info"
        )


@animes_router.get(
    "/search",
    response_model=Union[AnimeCardListOut, InternalServerErrorResponse],
)
async def search_anime_query(query: str, response: Response, request: Request):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Searching for anime with query: {query}")
        anime_card_list = await search_anime_query_controller(query)
        process_time = time.time() - start_time
        logger.info(
            f"Got anime search results for {query} in "
            + f"{process_time:.2f} seconds"
        )
        return AnimeCardListOut(
            request_id=request_id,
            process_time=process_time,
            func="search_anime_query",
            message="Anime search results retrieved",
            payload=anime_card_list,
        )
    except Exception as e:
        logger.error(f"Error searching for anime with query: {query}: {e}")
        response.status_code = 500
        return InternalServerErrorResponse(
            request_id=request_id, message=str(e), func="search_anime_query"
        )


@animes_router.get(
    "/streamlinks/{anime}",
    response_model=Union[AnimeStreamingLinksOut, InternalServerErrorResponse],
)
async def get_anime_streaming_links(
    anime: str, response: Response, request: Request
):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Getting anime stream links for {anime}")
        anime_links = await get_streaming_links_controller(anime)
        process_time = time.time() - start_time
        logger.info(
            f"Got anime stream links for {anime} in {process_time:.2f} seconds"
        )
        return AnimeStreamingLinksOut(
            request_id=request_id,
            process_time=process_time,
            func="get_anime_streaming_links",
            message="Anime links retrieved",
            payload=anime_links,
        )
    except Exception as e:
        logger.error(f"Error getting anime stream links for {anime}: {e}")
        response.status_code = 500
        return InternalServerErrorResponse(
            request_id=request_id,
            message=str(e),
            func="get_anime_streaming_links",
        )


@animes_router.post(
    "/downloadlinks/range",
    response_model=Union[
        AnimeDownloadLinkListOut, InternalServerErrorResponse
    ],
)
async def get_range_episodes_download_links(
    episode_links: list[dict],
    response: Response,
    request: Request,
    episode_range: str = None,
):
    start_time = time.time()
    request_id = request.state.request_id
    anime_name = None
    try:
        anime_name = "-".join(
            episode_links[0]["link"].split("/")[-1].split("-")[:-1]
        )
        logger.info(
            f"Getting anime download links for {anime_name} "
            + f"with range {episode_range}"
        )
        anime_links = await get_range_episodes_download_links_controller(
            episode_links, episode_range
        )
        process_time = time.time() - start_time
        logger.info(
            f"Got anime download links for {anime_name} "
            + f"with range {episode_range} in {process_time:.2f} seconds"
        )
        return AnimeDownloadLinkListOut(
            request_id=request_id,
            process_time=process_time,
            func="get_range_episodes_download_links",
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
            request_id=request_id,
            message=str(e),
            func="get_range_episodes_download_links",
        )


@animes_router.post(
    "/downloadlinks/single",
    response_model=Union[AnimeDownloadLinkOut, InternalServerErrorResponse],
)
async def get_single_episode_download_link(
    episode_link: str, episode_id: int, response: Response, request: Request
):
    start_time = time.time()
    request_id = request.state.request_id
    try:
        logger.info(f"Getting single download link for {episode_link}")
        download_link = await get_single_episode_download_link_controller(
            episode_link, episode_id
        )
        process_time = time.time() - start_time
        return AnimeDownloadLinkOut(
            request_id=request_id,
            process_time=process_time,
            func="get_single_episode_download_link",
            message="Single download link retrieved",
            payload=download_link,
        )
    except Exception as e:
        logger.error(
            f"Error getting single download link for {episode_link}: {e}"
        )
        response.status_code = 500
        return InternalServerErrorResponse(
            request_id=request_id,
            message=str(e),
            func="get_single_episode_download_link",
        )
