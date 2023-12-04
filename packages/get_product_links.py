from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
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


def get_link(revision):
    browser_options = browserOptions()
    browser_options.add_argument('--headless=new')
    browser = webdriver.Chrome(
        service=Service(executable_path=EXECUTABLE_PATH), options=browser_options)
    browser.get('http://edms.crbard.com/mc/login/index.cfm')

    login(browser)

    try:
        print(f"Start Searching for {revision}")
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "search"))).click()

        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "bigFrame")))

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'basicTabLink'))).click()

        browser.find_element(By.ID, "firstText").send_keys(revision)
        browser.find_element(By.ID, "searchButton").click()

        sleep(5)
        browser.switch_to.default_content()
        browser.switch_to.frame(browser.find_element(By.ID, "myframe"))
        browser.find_element(By.ID, "Documents_panel").click()
        link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.ID, "titleLink1"))).get_attribute('href').split("=")
        print("Found the links!")
        return f"http://edms.crbard.com/mc/Main/MASTERControl/vault/view_doc.cfm?ls_id={link[1]}"
    except Exception:
        print("Failed to get the link url. There something wrong!")
        return False


def get_codes(file):
    codes = []
    try:
        with open(file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                r = {
                    'FG CODE': row['FG CODE'],
                    'REVISION #': row['REVISION #'],
                    'REV DATE': row['REV DATE'][2:],
                    'ARTWORK': row['ARTWORK']
                }
                codes.append(r)
    except PermissionError:
        print("Please close the input file and run the script again!")
    return codes


def write_file(func):
    def wrapper(*args, **kwargs):
        filename = RESULT_DIR / args[1]
        print("Initializing operations...")
        with open(filename, 'w', newline='') as f:
            header = ["FG CODE", "REVISION #", "REV DATE", "ARTWORK", "LINK"]
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(func(*args, **kwargs))
            print("Done saving informations into the file!")
    return wrapper


@write_file
def append_code(*args):
    c = []
    for code in args[0]:
        start_msg = "Getting " + code['REVISION #']
        stop_msg = "Got the link. Fetching new link!"
        print("*" * 100)
        print('\n')
        print(start_msg)
        valid = get_link(code['REVISION #'])
        if not valid:
            if 'BAW' in code['REVISION #']:
                revision = code['REVISION #'].replace('BAW', 'PK').strip()
                print("Trying searching with prefix PK...")
                link = get_link(revision)
                code['LINK'] = link
            elif 'PK' in code['REVISION #']:
                revision = code['REVISION #'].replace('PK', 'BAW').strip()
                print("Trying searching with prefix BAW...")
                link = get_link(revision)
                code['LINK'] = link
            else:
                print("No valid link found.")
        else:
            code['LINK'] = valid
        print(stop_msg)
        print()
        print("*" * 100)
        c.append(code)
    return c


def main():
    filename = INPUT_DIR / pp.inputFilename(prompt="Enter input filename: ")
    codes = get_codes(filename)
    append_code(codes, Path(filename).name)

if __name__ == "__main__":
    main()