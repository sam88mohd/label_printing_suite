from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from packages import get_product_links
from time import sleep
import pyinputplus as pp
import pandas as pd

EXECUTABLE_PATH = Path("c:\\chromedriver.exe")
RESULT_DIR = Path("results")


def read_csv(file):
    file = RESULT_DIR / Path(file)
    df = pd.read_csv(file)
    return df.loc[:, 'LINK']


def show_page(links):
    browser_options = get_product_links.browserOptions()
    browser_options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(
        service=Service(executable_path=EXECUTABLE_PATH), options=browser_options)

    browser.maximize_window()

    for index, link in enumerate(links):
        if not link == "FALSE":
            browser.get(link)
        else:
            continue
        if browser.title == "MasterControl Login":
            get_product_links.login(browser)

        print(f"Getting {link}")

        sleep(2)
        if (index != len(links) - 1):
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[-1])


def main():
    filename = pp.inputFilename(prompt="Enter input filename: ")
    links = read_csv(filename)
    show_page(links)
