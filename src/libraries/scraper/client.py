import asyncio
import logging
import uuid
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import (
    DELAY_TIME,
    WEBDRIVER_DELAY,
    ChromeDriverContext,
    parse_episode_range,
)
from .tab_links import get_sw_link, get_yourupload_link
from .table_links import get_streamtape_download_link
from .config import scraper_settings

ANIME_HOST = scraper_settings.HOST

preference_order_tabs = [
    "SW",
    "YourUpload",
]
role_value = "tablist"
xpath_expression = f'//*[@role="{role_value}"]'

fn_get_tab_download_link = {
    "SW": get_sw_link,
    "YourUpload": get_yourupload_link,
}

semaphore = asyncio.Semaphore(6)
logging.basicConfig(
    format="%(name)s | %(levelname)s | %(asctime)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger(__name__)


def get_order_idx(preference_order_tabs, current_tabs):
    current_tabs = {tab: idx for idx, tab in enumerate(current_tabs)}

    order_idx = []
    for tab in preference_order_tabs:
        if tab in current_tabs:
            order_idx.append(current_tabs[tab])

    return order_idx


async def async_get_streaming_links(anime, uuid_str=str(uuid.uuid4())):
    with ChromeDriverContext() as driver:
        logger.info(f"{uuid_str} | Getting streaming links for {anime}")
        driver.get(ANIME_HOST + f"/anime/{anime}")
        driver.implicitly_wait(1)

        episodes_box = WebDriverWait(driver, WEBDRIVER_DELAY).until(
            EC.presence_of_element_located((By.ID, "episodeList"))
        )
        while True:
            previous_rows_len = len(
                WebDriverWait(episodes_box, WEBDRIVER_DELAY).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
                )
            )

            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[0].scrollHeight);",
                episodes_box,
            )

            await asyncio.sleep(DELAY_TIME)

            current_row_len = len(
                WebDriverWait(episodes_box, WEBDRIVER_DELAY).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
                )
            )

            logger.info(
                f"{uuid_str} | Current found {current_row_len} "
                + f"episodes for {anime}"
            )

            if current_row_len == previous_rows_len:
                break

        page_source = driver.page_source
        episodes_box = BeautifulSoup(page_source, "html.parser").find(
            id="episodeList"
        )
        episodes = episodes_box.find_all(class_="fa-play-circle")

        links = []
        for episode in episodes:
            class_name = episode["class"]
            if "Next" in class_name:
                continue
            link = ANIME_HOST + episode.find("a")["href"]
            title = episode.find("p").text
            links.append({"link": link, "title": title})
        links.reverse()
        logger.info(
            f"{uuid_str} | Found {len(links)} streaming links for {anime}"
        )
        return links


def sync_get_streaming_links(anime):
    return asyncio.run(async_get_streaming_links(anime))


async def async_get_single_episode_download_link(
    episode_link, uuid_str=str(uuid.uuid4())
):
    async with semaphore:
        anime_episode_name = episode_link.split("/")[-1]
        with ChromeDriverContext() as driver:
            logger.info(
                f"{uuid_str} | Getting download link for {anime_episode_name}"
            )
            driver.switch_to.window(driver.window_handles[0])
            driver.get(episode_link)
            driver.implicitly_wait(1)

            page_source = driver.page_source
            test_soup = BeautifulSoup(page_source, "html.parser")

            download_table = test_soup.find(class_="Dwnl")
            download_links = download_table.find_all("a")

            driver.switch_to.window(driver.window_handles[0])
            navbar = driver.find_element(By.XPATH, xpath_expression)
            nav_tabs = navbar.find_elements(By.TAG_NAME, "li")

            titles = [nav_tab.get_attribute("title") for nav_tab in nav_tabs]
            order_idx = get_order_idx(preference_order_tabs, titles)

            for link in download_links:
                try:
                    if "mega" in link["href"] or "fichier" in link["href"]:
                        continue
                        logger.info(
                            f"{uuid_str} | Found link for {anime_episode_name} "
                            + "at service Mega"
                        )
                    if "streamtape" in link["href"]:
                        parsed_link = await get_streamtape_download_link(
                            driver, link["href"]
                        )
                        if not parsed_link:
                            continue
                        logger.info(
                            f"{uuid_str} | Found link for {anime_episode_name} "
                            + "at service Streamtape"
                        )
                        return parsed_link

                except Exception as e:
                    logger.error(
                        f"{uuid_str} | Error for {anime_episode_name}: {e}"
                    )
                    continue

            for idx in order_idx:
                try:
                    nav_tab = nav_tabs[idx]
                    driver.switch_to.window(driver.window_handles[0])
                    title = nav_tab.get_attribute("title")

                    logger.info(
                        f"{uuid_str} | Trying service {title} "
                        + f"for {anime_episode_name}"
                    )

                    link = nav_tab.find_element(By.TAG_NAME, "a")
                    link.click()

                    if title in fn_get_tab_download_link:
                        curr_fn = fn_get_tab_download_link[title]
                        src_link = await curr_fn(driver)
                        if not src_link:
                            continue
                        logger.info(
                            f"{uuid_str} | Found link for {anime_episode_name} "
                            + f"at service {title}"
                        )
                        return src_link
                except Exception as e:
                    logger.error(
                        f"{uuid_str} | Error for {anime_episode_name}: {e}"
                    )
                    continue


def sync_get_single_episode_download_link(episode_link):
    return asyncio.run(async_get_single_episode_download_link(episode_link))


async def async_get_download_links(
    episode_links, episodes_range=None, uuid_str=str(uuid.uuid4())
):
    episodes = (
        parse_episode_range(episodes_range)
        if episodes_range
        else range(1, len(episode_links) + 1)
    )
    logger.info(f"{uuid_str} | Getting download links for episodes {episodes}")
    final_download_links = []
    tasks = []
    anime = "-".join(episode_links[0]["link"].split("/")[-1].split("-")[:-1])
    for episode_id in episodes:
        episode_link = episode_links[episode_id - 1]["link"]
        download_link_task = asyncio.create_task(
            async_get_single_episode_download_link(episode_link, uuid_str)
        )
        tasks.append(
            {
                "title": episode_links[episode_id - 1]["title"],
                "task": download_link_task,
                "episode": episode_id,
            }
        )

    results = await asyncio.gather(
        *[task["task"] for task in tasks], return_exceptions=True
    )

    logger.info(f"{uuid_str} | Finished getting download links")

    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(
                f"{uuid_str} | Error for {tasks[idx]['title']}: {result}"
            )
            continue
        final_download_links.append(
            {
                "title": tasks[idx]["title"],
                "download_link": result,
                "episode": tasks[idx]["episode"],
            }
        )

    anime_download_info = {
        "anime": anime,
        "download_links": final_download_links,
    }
    logger.info(
        f"{uuid_str} | Found {len(final_download_links)} "
        + f"download links for {anime}"
    )
    return anime_download_info


def sync_get_download_links(episode_links, episodes_range=None):
    return asyncio.run(async_get_download_links(episode_links, episodes_range))


async def async_get_emission_date(anime, uuid_str=str(uuid.uuid4())):
    with ChromeDriverContext() as driver:
        logger.info(f"{uuid_str} | Getting emission date for {anime}")
        driver.get(ANIME_HOST + f"/anime/{anime}")
        driver.implicitly_wait(1)

        episodes_box = WebDriverWait(driver, WEBDRIVER_DELAY).until(
            EC.presence_of_element_located((By.ID, "episodeList"))
        )
        current_rows_len = len(episodes_box.find_elements(By.TAG_NAME, "li"))
        while current_rows_len == 0:
            current_rows_len = len(
                WebDriverWait(episodes_box, WEBDRIVER_DELAY).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
                )
            )

        page_source = episodes_box.get_attribute("outerHTML")
        soup = BeautifulSoup(page_source, "html.parser")
        week_day = soup.find_all("li")[0].find("span").text
        logger.info(
            f"{uuid_str} | Found emission date for {anime}: {week_day}"
        )

        return week_day


def sync_get_emission_date(anime):
    return asyncio.run(async_get_emission_date(anime))
