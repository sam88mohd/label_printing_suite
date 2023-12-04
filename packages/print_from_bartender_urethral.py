from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
from pathlib import Path
import pyinputplus as pp
import pyinputplus as pp
import csv
import os

EXECUTABLE_PATH = Path("c:\\chromedriver.exe")
INPUT_DIR = Path("./input")
load_dotenv()
username = os.getenv("MC-USERNAME")
password = os.getenv("MC-PASSWORD")


def get_detail_from_csv(csv_file):
    # get product code from csv file
    products = []

    with open(csv_file, newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader)
        for row in csvReader:
            products.append(tuple(row))

    return products


def wait_for_loading(browser):
    # display Wait message to user
    print("[INFO] Loading...")
    WebDriverWait(browser, 200).until(
        EC.invisibility_of_element((By.CLASS_NAME, "loadingoverlay")))


def download_label(label_type, lot, serial):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')
    # chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    browser = webdriver.Chrome(service=Service(
        executable_path=EXECUTABLE_PATH), options=chrome_options)
    # browser.minimize_window()

    root_url = "https://pw01shs6btnap01.bdx.com/BarTender/Print/7f4b2eb0-2b17-4b9e-bda5-ebd99f8eb02d/Malaysia/Uretheral/"

    if label_type == 'Inner Carton Label':
        browser.get(root_url + label_type + "/UI1390.btw")
    elif label_type == 'Outer Carton Label (Shipper)':
        browser.get(root_url + label_type + "/UO1390.btw")
    elif label_type == 'Pouch Label':
        browser.get(root_url + label_type + "/UP1390.btw")

    # get credentials
    print("[INFO] Inserting Username details")
    browser.find_element(By.ID, "usernameInput").send_keys(
        "bdx\\" + username)

    print("[INFO] Inserting Password details")
    browser.find_element(By.ID, "passwordInput").send_keys(password)

    print("[INFO] Clicking Login Button")
    browser.find_element(By.ID, "LogonPageSubmitButton").click()

    select = Select(browser.find_element(
        By.XPATH, "//*[@id='SelectedPrinterInput']"))
    select.select_by_visible_text('MY_SATO CL4NX _#07')

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='SerialNumbersInput']"))).clear()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='SerialNumbersInput']"))).send_keys(serial)
    browser.find_element(
        By.XPATH, "//*[@id='PrintFormPrintButton']").click()

    wait_for_loading(browser)

    print("[INFO] Clicking Dropdown Menu")
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-toggle='dropdown']"))).click()

    print("[INFO] Entering Lot Number: {}".format(lot))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='search']"))).send_keys(lot)

    print("[INFO] Selecting Lot Number: {}".format(lot))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='dataTables_scrollBody']/table/tbody/tr"))).click()

    wait_for_loading(browser)

    print("[INFO] Clicking Print Button")
    browser.find_element(By.XPATH, "//input[@type='submit']").click()

    wait_for_loading(browser)

    WebDriverWait(browser, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='PrintPageModalDialog']/div/div/div[3]/button"))).click()


def main():
    lot_filename = INPUT_DIR / \
        pp.inputFilename(prompt="Enter input filename: ")
    choices = ['Inner Carton Label',
               'Outer Carton Label (Shipper)', 'Pouch Label']
    label_type = pp.inputMenu(choices=choices, numbered=True)
    serial = pp.inputInt(prompt="Enter how many to print: ")
    products = get_detail_from_csv(lot_filename)
    for product in products:
        lot = product[1]
        try:
            download_label(label_type=label_type, lot=lot, serial=serial)
        except Exception:
            print("Retry")
            download_label(label_type=label_type, lot=lot, serial=serial)

if __name__ == "__main__":
    main()
