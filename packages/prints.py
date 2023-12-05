from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from packages.utils.helper import create_chrome_browser, enter_user_password, wait_for_loading, print_info_message
from packages.utils.details import URETHRAL_URL_PATH


def print_label(label_type, lot, serial, printer):
    browser = create_chrome_browser()
    if label_type == 'Inner Carton Label':
        browser.get(URETHRAL_URL_PATH + label_type + "/UI1390.btw")
    elif label_type == 'Outer Carton Label (Shipper)':
        browser.get(URETHRAL_URL_PATH + label_type + "/UO1390.btw")
    elif label_type == 'Pouch Label':
        browser.get(URETHRAL_URL_PATH + label_type + "/UP1390.btw")

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
