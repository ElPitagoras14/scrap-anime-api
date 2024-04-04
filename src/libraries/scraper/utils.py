from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService

DELAY_TIME = 7


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


class EdgeDriverContext:
    def __init__(self):
        options = webdriver.EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-autofill")
        options.add_argument("--headless")
        options.add_argument("log-level=3")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.service = EdgeService(service_args=["--log-level=OFF"])
        self.options = options
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Edge(
            options=self.options, service=self.service
        )
        self.driver.execute_script("window.open('', '_blank');")
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()
