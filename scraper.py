import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(headless: bool, page_load_timeout: int):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(page_load_timeout)
    return driver

def fetch_html(driver, url: str, wait_after_load: int) -> str:
    driver.get(url)
    time.sleep(wait_after_load)
    return driver.page_source
