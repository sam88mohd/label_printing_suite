from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from packages.utils.details import TEN_URL_PATH, USERNAME, PASSWORD
from packages.utils.helper import wait_for_loading, create_browser
from time import sleep
# import keyboard
import os


def download_label(label, lot, fg):
    browser = create_browser()
    browser.get(TEN_URL_PATH + label + ".btw")

    print()
    print("[STATUS] Starting Download Label: '{}-{}'".format(label, fg))
    print()

    # get credentials
    print("[INFO] Inserting Username details")
    browser.find_element(By.ID, "usernameInput").send_keys("bdx\\" + USERNAME)

    print("[INFO] Inserting Password details")
    browser.find_element(By.ID, "passwordInput").send_keys(PASSWORD)

    print("[INFO] Clicking Login Button")
    browser.find_element(By.ID, "LogonPageSubmitButton").click()

    print("[INFO] Clicking Print Button")
    browser.find_element(By.ID, "PrintFormPrintButton").click()

    print("[INFO] Clicking Dropdown Menu")
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-toggle='dropdown']"))).click()

    wait_for_loading(browser)

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

    print("[INFO] Clicking Download Button")
    WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@download]"))).click()

    # sleep(5)
    # keyboard.press('enter')

    print("[INFO] Waiting for the download to complete...")
    seconds = 0
    dl_wait = True
    while dl_wait:
        if not os.path.exists(os.path.join('C:\\Users\\{}\\Downloads'.format(os.getlogin()), label + '.pdf')):
            sleep(seconds)
            seconds += 1
        else:
            break

    print()
    print("[STATUS] {}-{} file successfully downloaded".format(label, fg))
    print()
