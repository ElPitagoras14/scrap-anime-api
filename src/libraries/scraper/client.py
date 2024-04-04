import asyncio
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .utils import DELAY_TIME, EdgeDriverContext, parse_episode_range
from .tab_links import get_sw_link, get_yourupload_link
from .table_links import get_streamtape_download_link
from .config import scraper_settings

unuseful_tabs = ["Mega"]
role_value = "tablist"
xpath_expression = f'//*[@role="{role_value}"]'

SCRAPER_HOST = scraper_settings.HOST


async def get_streaming_links(anime):
    with EdgeDriverContext() as driver:
        driver.get(SCRAPER_HOST + f"/anime/{anime}")
        driver.implicitly_wait(1)

        episodes_box = driver.find_element(By.ID, "episodeList")
        while True:
            numero_de_filas_anterior = len(
                episodes_box.find_elements(By.TAG_NAME, "li")
            )

            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[0].scrollHeight);",
                episodes_box,
            )

            print("Scrolling...")
            await asyncio.sleep(DELAY_TIME)

            numero_de_filas_actual = len(
                episodes_box.find_elements(By.TAG_NAME, "li")
            )

            if numero_de_filas_actual == numero_de_filas_anterior:
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
            link = SCRAPER_HOST + episode.find("a")["href"]
            name = episode.find("p").text
            links.append({"link": link, "name": name})
        links.reverse()
        return links


async def get_single_episode_download_link(episode_link):
    with EdgeDriverContext() as driver:
        return await get_single_download_link(episode_link, driver)


async def get_single_download_link(episode_link, driver):
    driver.switch_to.window(driver.window_handles[0])
    driver.get(episode_link)
    driver.implicitly_wait(1)

    page_source = driver.page_source
    test_soup = BeautifulSoup(page_source, "html.parser")

    download_table = test_soup.find(class_="Dwnl")
    download_links = download_table.find_all("a")

    for link in download_links:
        if "mega" in link["href"] or "fichier" in link["href"]:
            continue
        if "streamtape" in link["href"]:
            parsed_link = await get_streamtape_download_link(
                driver, link["href"]
            )
            if not parsed_link:
                continue
            return parsed_link

    driver.switch_to.window(driver.window_handles[0])
    navbar = driver.find_element(By.XPATH, xpath_expression)
    nav_tabs = navbar.find_elements(By.TAG_NAME, "li")

    for nav_tab in nav_tabs:
        driver.switch_to.window(driver.window_handles[0])
        title = nav_tab.get_attribute("title")
        if title in unuseful_tabs:
            continue

        link = nav_tab.find_element(By.TAG_NAME, "a")
        link.click()

        if title == "SW":
            src_link = await get_sw_link(driver)
            if not src_link:
                continue
            print(src_link)
            return src_link

        if title == "YourUpload":
            src_link = await get_yourupload_link(driver)
            if not src_link:
                continue
            print(src_link)
            return src_link


async def get_download_links(episode_links, episodes_range=None):
    episodes = (
        await parse_episode_range(episodes_range)
        if episodes_range
        else range(1, len(episode_links) + 1)
    )
    with EdgeDriverContext() as driver:
        final_download_links = []
        anime = "-".join(
            episode_links[0]["link"].split("/")[-1].split("-")[:-1]
        )
        for episode_id in episodes:
            episode_link = episode_links[episode_id - 1]["link"]
            download_link = await get_single_download_link(episode_link, driver)
            if not download_link:
                final_download_links.append(None)
                continue
            final_download_links.append(
                {
                    "episode": episode_id,
                    "download_link": download_link,
                    "name": episode_links[episode_id - 1]["name"],
                }
            )
        anime_download_info = {
            "anime": anime,
            "download_links": final_download_links,
        }
        return anime_download_info
