from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from .config import scraper_settings

DELAY_TIME = 7
WEBDRIVER_DELAY = 30

IN_DOCKER = scraper_settings.IN_DOCKER


def parse_episode_range(episodes_range):
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
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("window-size=1920x1080")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-autofill")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

        self.service = ChromeService()
        self.options = options
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome(
            options=self.options,
            service=self.service,
        )
        self.driver.execute_script("window.open('', '_blank');")
        self.driver.set_window_size(1920, 1080)
        if not IN_DOCKER:
            self.driver.save_screenshot("output/init_screnshoot.png")

        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
