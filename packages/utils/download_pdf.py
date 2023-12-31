from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from packages.utils.helper import wait_for_loading, create_chrome_browser, print_info_message, print_status_message, print_success_message, enter_user_password, get_label_name
from packages.utils.details import PRINT_URL
from time import sleep
import os


def download_label(path, lot, fg):
    delay = 20
    browser = create_chrome_browser()
    browser.get(PRINT_URL + path)

    print_status_message("Starting Download Label: '{}'".format(fg))

    # get credentials
    enter_user_password(browser=browser)

    print_info_message("Clicking Login Button")
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(
        (By.ID, "LogonPageSubmitButton"))).click()
    
    wait_for_loading(browser)
    
    print_info_message("Clicking Print Button")
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='PrintFormPrintButton']"))).click()

    wait_for_loading(browser)

    print_info_message("Clicking Dropdown Menu")
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-toggle='dropdown']"))).click()

    wait_for_loading(browser)

    print_info_message("Entering Lot Number: {}".format(lot))
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='search']"))).send_keys(lot)

    print_info_message("Selecting Lot Number: {}".format(lot))
    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='dataTables_scrollBody']/table/tbody/tr[1]"))).click()

    wait_for_loading(browser)

    print_info_message("Clicking Print Button")
    browser.find_element(By.XPATH, "//input[@type='submit']").click()

    wait_for_loading(browser)

    print_info_message("Clicking Download Button")
    WebDriverWait(browser, delay).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@download]"))).click()

    # sleep(5)
    # keyboard.press('enter')

    print_info_message("Waiting for the download to complete...")
    seconds = 0
    dl_wait = True
    while dl_wait:
        if not os.path.exists(os.path.join('C:\\Users\\{}\\Downloads'.format(os.getlogin()), get_label_name(path=path) + '.pdf')):
            sleep(seconds)
            seconds += 1
        else:
            break

    print_success_message(
        "{} file successfully downloaded".format(fg))
