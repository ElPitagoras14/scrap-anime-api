from libraries.scraper import (
    sync_get_streaming_links,
    sync_get_download_links,
    sync_get_single_episode_download_link,
    sync_get_emission_date,
)
import logging
import os

curr_workspace = os.getcwd()


logger = logging.getLogger("scraper")
file_handler = logging.FileHandler(f"{curr_workspace}/scraper.log")
file_handler.setFormatter(
    logging.Formatter(
        fmt="%(name)s | %(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
)

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

streaming_links = sync_get_streaming_links(
    "ookami-to-koushinryou-merchant-meets-the-wise-wolf"
)
download_links = sync_get_download_links(streaming_links, "1-6")
