import asyncio
import json
import logging
import os
import shutil
import ssl
import urllib.request as urlrequest
from pathlib import Path
from urllib.error import URLError

import dotenv
from retry import retry
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

# noinspection PyUnresolvedReferences
ssl._create_default_https_context = ssl._create_unverified_context
dotenv.load_dotenv()

WGET = Path("wget.txt")
FOLDER = Path("downloads")
TO_SKIP = Path("to_skip.txt")


class LootStudios:
    def __init__(self):
        self.logger = logging.getLogger("Loot Studios")
        if WGET.exists():
            with open(WGET) as fr:
                self.to_download = json.load(fr)
        else:
            self.to_download = {}

    @staticmethod
    @retry(WebDriverException, tries=5, delay=1)
    def get(driver, url):
        driver.get(url)

    def download(self, url, filename: Path):
        self.logger.debug(f"Downloading {filename.name}")
        try:
            with urlrequest.urlopen(url) as response, open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
        except URLError as err:
            self.logger.warning("Download of %s failed", filename.name)
            self.logger.debug("Error: %s", err)

    async def download_all(self):
        await asyncio.gather(
            *[
                asyncio.to_thread(self.download, d["url"], Path(d["path"]))
                for d in self.to_download.values()
            ]
        )

    def get_data(self):
        try:
            with open(TO_SKIP) as f:
                to_skip = {l.strip() for l in f}
        except FileNotFoundError:
            to_skip = set()

        with webdriver.Chrome() as driver:
            driver.get("https://www.loot-studios.com/login")
            driver.find_element(value="member_email").send_keys(os.environ["EMAIL"])
            driver.find_element(value="member_password").send_keys(
                os.environ["LOOT_PASSWORD"].strip()
            )
            driver.find_element(By.NAME, "commit").click()

            i = 1
            while True:
                driver.get(f"https://www.loot-studios.com/library?page={i}")
                products = {
                    l.get_attribute("href")
                    for l in driver.find_element(
                        By.XPATH, "/html/body/div[1]/div/div[3]/div"
                    ).find_elements(By.TAG_NAME, "a")
                }

                if "products" not in ",".join(products):
                    break

                for product in products:
                    if "library" in product or product in to_skip:
                        continue

                    self.get(driver, product)
                    mainfolder = driver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div/h1",
                    ).text
                    if mainfolder.lower() != "welcome pack":
                        mainfolder = " ".join(mainfolder.strip().split()[:-1])
                    mainfolder = FOLDER.joinpath(mainfolder)
                    os.makedirs(mainfolder, exist_ok=True)

                    categories = set()
                    syllabus = driver.find_element(
                        By.XPATH, '//*[@id="section-product_syllabus"]/div/div'
                    )
                    for element in syllabus.find_elements(
                        By.CLASS_NAME, "syllabus__item"
                    ):
                        for href in element.find_elements(By.TAG_NAME, "a"):
                            if href.text != "Show More":
                                categories.add(href.get_attribute("href"))
                    categories = sorted(categories)

                    for category in categories:
                        self.get(driver, category)

                        try:
                            downloads = driver.find_element(
                                By.CLASS_NAME, "downloads"
                            ).find_elements(By.TAG_NAME, "a")
                        except NoSuchElementException:
                            continue

                        subfolder = driver.find_element(
                            By.CLASS_NAME, "panel__title"
                        ).text
                        subfolder.replace('"', "'")
                        path = mainfolder.joinpath(subfolder)
                        os.makedirs(path, exist_ok=True)

                        for d in downloads:
                            with open("run.sh", "a") as f:
                                f.write(
                                    f'wget "{d.get_attribute("href")}" -O "{path}/{d.text}" &\n'
                                )
                            self.to_download[str(d.text)] = {
                                "url": d.get_attribute("href"),
                                "path": str(path.joinpath(d.text)),
                            }

                    with open(TO_SKIP, "a") as f:
                        f.write(product + "\n")
                i += 1

    def run(self):
        try:
            self.get_data()
        except WebDriverException as err:
            logging.warning(str(err))

        with open(WGET, "w") as fwget:
            json.dump(self.to_download, fwget, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
    downloader = LootStudios()
    downloader.run()
    asyncio.run(downloader.download_all())
