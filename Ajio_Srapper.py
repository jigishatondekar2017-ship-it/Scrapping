
import csv
import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--start-maximized")

driver = None
products_dict = {}

try:
    driver = uc.Chrome(
        version_main=157,
        options=options
    )

    # Use the correct category URL copied from AJIO
    url = "https://www.ajio.com/menbackpacks/c/830201001"
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    scroll_pause = 2
    same_count = 0
    previous_total = 0

    while same_count < 8:

        products = driver.find_elements(
            By.CLASS_NAME, "item"
        )

        print("Visible Products:", len(products))

        for product in products:
            try:
                link = product.find_element(
                    By.TAG_NAME, "a"
                ).get_attribute("href")

                if not link or link in products_dict:
                    continue

            except Exception:
                continue

            try:
                brand = product.find_element(
                    By.CLASS_NAME, "brand"
                ).text
            except Exception:
                brand = ""

            try:
                name = product.find_element(
                    By.CLASS_NAME, "nameCls"
                ).text
            except Exception:
                name = ""

            try:
                price = product.find_element(
                    By.CLASS_NAME, "price"
                ).text
            except Exception:
                price = ""

            try:
                image = product.find_element(
                    By.TAG_NAME, "img"
                ).get_attribute("src")
            except Exception:
                image = ""

            products_dict[link] = [
                brand, name, price, image, link
            ]

        print("Collected:", len(products_dict))

        # Scroll down to load more products
        driver.execute_script(
            "window.scrollBy(0, 1200);"
        )
        time.sleep(scroll_pause)

        current_total = len(products_dict)

        if current_total == previous_total:
            same_count += 1
        else:
            same_count = 0

        previous_total = current_total

    # Save the collected products once scraping ends
    with open(
        "Ajio.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Brand",
            "Product Name",
            "Price",
            "Image URL",
            "Product Link"
        ])

        writer.writerows(products_dict.values())

    print("-" * 50)
    print("Scraping completed.")
    print("Total products:", len(products_dict))
    print("CSV saved as Ajio.csv")

finally:
    if driver is not None:
        driver.quit()
