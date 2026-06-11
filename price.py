from playwright.sync_api import sync_playwright
import re
import json
import time

CACHE_FILE = "price.json"

url = "https://www.tgju.org/profile/geram18"


def fetch_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text()

        browser.close()

    m = re.search(r"نرخ فعلی[:\s]*([\d,]+)", text)

    if m:
        return int(m.group(1).replace(",", ""))

    return None


def save(price):
    data = {
        "price": price,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def get_price():
    try:
        price = fetch_price()
        save(price)
        return price, True, None
    except:
        cached = load()
        if cached:
            return cached["price"], False, cached["time"]

        return None, False, None