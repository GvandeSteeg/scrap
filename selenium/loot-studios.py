import os
import shutil
import urllib.request as urlrequest
from urllib.error import URLError

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

FOLDER = "downloads"
TO_SKIP = "to_skip.txt"

to_download = []


async def download(url, filename):
    try:
        with urlrequest.urlopen(url) as response, open(filename, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
    except URLError as err:
        print(filename, "failed")


try:
    with open(TO_SKIP) as f:
        to_skip = {l.strip() for l in f}
except FileNotFoundError:
    to_skip = set()

with webdriver.Chrome() as driver:
    driver.get("https://www.loot-studios.com/login")
    driver.find_element(value="member_email").send_keys("guus.steeg@gmail.com")
    driver.find_element(value="member_password").send_keys(
        os.environ["PASSWORD"].strip()
    )
    driver.find_element(By.NAME, "commit").click()

    i = 1
    while i <= 3:
        driver.get(f"https://www.loot-studios.com/library?page={i}")
        products = {
            l.get_attribute("href")
            for l in driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[3]/div"
            ).find_elements(By.TAG_NAME, "a")
        }
        for product in products:
            if "library" in product or product in to_skip:
                continue

            driver.get(product)
            mainfolder = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div/div/div/div/h1"
            ).text
            if mainfolder.lower() != "welcome pack":
                mainfolder = " ".join(mainfolder.strip().split()[:-1])
            mainfolder = os.path.join(FOLDER, mainfolder)
            os.makedirs(mainfolder, exist_ok=True)

            categories = set()
            syllabus = driver.find_element(
                By.XPATH, '//*[@id="section-product_syllabus"]/div/div'
            )
            for element in syllabus.find_elements(By.CLASS_NAME, "syllabus__item"):
                for href in element.find_elements(By.TAG_NAME, "a"):
                    if href.text != "Show More":
                        categories.add(href.get_attribute("href"))
            categories = sorted(categories)

            for category in categories:
                driver.get(category)

                try:
                    downloads = driver.find_element(
                        By.CLASS_NAME, "downloads"
                    ).find_elements(By.TAG_NAME, "a")
                except NoSuchElementException:
                    continue

                subfolder = driver.find_element(By.CLASS_NAME, "panel__title").text
                path = os.path.join(mainfolder, subfolder)
                os.makedirs(path, exist_ok=True)

                for d in downloads:
                    if not d.text.endswith("zip"):
                        continue
                    with open("run.sh", "a") as f:
                        f.write(
                            f'wget "{d.get_attribute("href")}" -O "{path}/{d.text}" &\n'
                        )
                    # to_download.append((d.get_attribute("href"), os.path.join(path, d.text)))

            with open(TO_SKIP, "a") as f:
                f.write(product + "\n")
        i += 1

# async def download_all():
#     for url, name in to_download:
#         await download(url, name)
#
# asyncio.run(download_all())
