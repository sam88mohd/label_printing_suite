from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from dotenv import load_dotenv
from time import sleep
from os import getenv
import pyinputplus as pp
import csv

RESULT_DIR = Path("./results")
INPUT_DIR = Path("./input")
load_dotenv()
USERNAME = getenv("MC-USERNAME")
PASSWORD = getenv("MC-PASSWORD")
EXECUTABLE_PATH = Path("c:\\chromedriver.exe")


def browserOptions():
    browser_options = Options()
    browser_options.add_argument('--ignore-certificate-errors')
    browser_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    browser_options.add_argument('--incognito')
    browser_options.add_argument('--log-level=3')
    return browser_options


def login(browser):
    print("Login to Master Control...")

    browser.find_element(By.ID, "username").clear()
    browser.find_element(By.ID, "username").send_keys(USERNAME)
    browser.find_element(By.ID, "password").clear()
    browser.find_element(By.ID, "password").send_keys(PASSWORD)
    browser.find_element(By.ID, "loginButton").click()


def get_link(field):
    browser_options = browserOptions()
    browser_options.add_experimental_option('detach', True)

    for f in field:
        title = f"VP {f} *"

        browser = webdriver.Chrome(
            service=Service(executable_path=EXECUTABLE_PATH), options=browser_options)
        browser.get('http://edms.crbard.com/mc/login/index.cfm')

        browser.maximize_window()

        if browser.title == "MasterControl Login":
            login(browser)

        print(f"Start Searching for {f}")
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "search"))).click()

        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "bigFrame")))

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'basicTabLink'))).click()

        browser.find_element(By.ID, "firstText").send_keys(title)
        browser.find_element(By.ID, "searchButton").click()

        sleep(5)

        try:
            browser.switch_to.default_content()
            browser.switch_to.frame(browser.find_element(By.ID, "myframe"))
            browser.find_element(By.ID, "Documents_panel").click()
            tr = browser.find_elements(By.TAG_NAME, 'tr')
            for index, row in enumerate(tr):
                x = row.find_element(By.ID, f"titleLink{index + 1}").text
                print(x)
        except Exception:
            continue


def get_family(file):
    family = []
    try:
        with open(file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                family.append(row[0])
    except PermissionError:
        print("Please close the input file and run the script again!")
    return family


def main():
    filename = INPUT_DIR / pp.inputFilename(prompt="Enter input filename: ")
    family = get_family(filename)
    get_link(family)


if __name__ == "__main__":
    main()
