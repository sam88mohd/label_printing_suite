from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from packages.utils.details import PRINT_URL
from packages.utils.helper import create_chrome_browser, enter_user_password, wait_for_loading, print_info_message, print_status_message


def print_label(label_path, lot, serial, printer, fg):
    browser = create_chrome_browser()

    browser.get(PRINT_URL + label_path)

    print_status_message("Starting Download Label: '{}'".format(fg))

    # get credentials
    enter_user_password(browser=browser)

    print_info_message("Clicking Login Button")
    browser.find_element(By.ID, "LogonPageSubmitButton").click()

    select = Select(browser.find_element(
        By.XPATH, "//*[@id='SelectedPrinterInput']"))
    select.select_by_visible_text(printer)

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='SerialNumbersInput']"))).clear()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='SerialNumbersInput']"))).send_keys(serial)
    browser.find_element(
        By.XPATH, "//*[@id='PrintFormPrintButton']").click()

    wait_for_loading(browser)

    print_info_message("Clicking Dropdown Menu")
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-toggle='dropdown']"))).click()

    print_info_message("Entering Lot Number: {}".format(lot))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='search']"))).send_keys(lot)

    print_info_message("Selecting Lot Number: {}".format(lot))
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='dataTables_scrollBody']/table/tbody/tr"))).click()

    wait_for_loading(browser)

    print_info_message("Clicking Print Button")
    browser.find_element(By.XPATH, "//input[@type='submit']").click()

    wait_for_loading(browser)

    WebDriverWait(browser, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='PrintPageModalDialog']/div/div/div[3]/button"))).click()
