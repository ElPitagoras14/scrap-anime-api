import asyncio
from bs4 import BeautifulSoup

from .utils import DELAY_TIME


async def get_streamtape_download_link(driver, url):
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)
        driver.implicitly_wait(1)
        await asyncio.sleep(DELAY_TIME)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        video = soup.find("video")
        if not video:
            return None
        src_link = video["src"]
        return "https:" + src_link
    except Exception as e:
        print(f"Error: {e}: {url}")
        return None


async def get_fichier_download_link(driver, url):
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    driver.implicitly_wait(1)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    src_link = soup.find("video")["src"]
    return src_link
