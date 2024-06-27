from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from .config import scraper_settings

DELAY_TIME = 7

IN_DOCKER = scraper_settings.IN_DOCKER


async def parse_episode_range(episodes_range):
    episodes = []
    ranges = episodes_range.split(",")
    seen = set()
    for item in ranges:
        if "-" in item:
            start, end = map(int, item.split("-"))
            if start < 1 or end < 1:
                continue
            for episode_num in range(start, end + 1):
                if episode_num not in seen:
                    episodes.append(episode_num)
                    seen.add(episode_num)
        else:
            parts = item.split()
            for part in parts:
                episode_num = int(part)
                if episode_num >= 1 and episode_num not in seen:
                    episodes.append(episode_num)
                    seen.add(episode_num)
    return episodes


class ChromeDriverContext:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("headless")
        options.add_argument("disable-gpu")

        self.service = ChromeService(service_args=["--log-level=OFF"])
        self.options = options
        self.driver = None

    def __enter__(self):
        if IN_DOCKER:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.options,
            )
        else:
            self.driver = webdriver.Chrome(
                options=self.options, service=self.service
            )
        self.driver.execute_script("window.open('', '_blank');")
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
