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

        page.goto("https://www.tgju.org/profile/geram18")

        page.wait_for_timeout(7000)

        # مستقیم از DOM value (نه متن)
        elements = page.locator("span").all_inner_texts()

        browser.close()

    # پیدا کردن عدد واقعی بین همه span ها
    for t in elements:
        t = t.replace(",", "")
        if t.isdigit() and len(t) > 6:
            return int(t)

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
