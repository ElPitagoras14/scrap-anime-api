import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import DELAY_TIME, WEBDRIVER_DELAY

base_sw_download_url = "https://streamwish.to/f"
base_yourupload_download_url = "https://www.yourupload.com"


async def get_sw_link(driver):
    video_box = driver.find_element(By.ID, "video_box").find_element(
        By.TAG_NAME, "iframe"
    )
    src_link = video_box.get_attribute("src")
    video_id = src_link.split("/")[-1]
    try_links = [
        f"{base_sw_download_url}/{video_id}_h",
        f"{base_sw_download_url}/{video_id}_n",
    ]
    driver.switch_to.window(driver.window_handles[1])
    for link in try_links:
        try:
            driver.get(link)
            driver.implicitly_wait(5)
            button = WebDriverWait(driver, WEBDRIVER_DELAY).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            button.click()
            driver.implicitly_wait(5)
            await asyncio.sleep(DELAY_TIME)
            download_link = WebDriverWait(driver, WEBDRIVER_DELAY).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dwnlonk"))
            )
            src_link = download_link.get_attribute("href")
            if not src_link:
                continue
            return src_link
        except Exception:
            continue


async def get_yourupload_link(driver):
    try:
        xpath = "//div[@aria-label='Download Video']"
        download_button = WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        download_button.click()
        driver.implicitly_wait(5)
        driver.switch_to.window(driver.window_handles[2])

        download_button = WebDriverWait(driver, WEBDRIVER_DELAY).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-success"))
        )
        download_button.click()
        driver.implicitly_wait(5)
        await asyncio.sleep(DELAY_TIME)

        download_link = WebDriverWait(driver, WEBDRIVER_DELAY).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-success"))
        )
        src_link = download_link.get_attribute("href")
        return src_link
    except Exception:
        return None
