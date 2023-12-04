from packages.utils.details import EXECUTABLE_PATH
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from halo import Halo
from spinners import Spinners
import csv
import shutil
import os


colorama_init()


def create_browser():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    browser = webdriver.Chrome(service=Service(
        executable_path=EXECUTABLE_PATH), options=chrome_options)
    # browser.minimize_window()
    return browser


def print_info_message(msg):
    print("{}[INFO]{}         {}".format(
        Fore.LIGHTBLUE_EX, Style.RESET_ALL, msg))


def print_success_message(msg):
    print("{}[SUCCESS]{}      {}".format(Fore.LIGHTGREEN_EX, Style.RESET_ALL, msg))


def print_status_message(msg):
    print()
    print("{}[STATUS]{}       {}".format(Fore.YELLOW, Style.RESET_ALL, msg))
    print()


def print_error_message(msg):
    print()
    print("{}[ERROR]{}        {}".format(Fore.RED, Style.RESET_ALL, msg))
    print()


def print_done_message(msg):
    print()
    print("{}[DONE]{}         {}".format(Fore.GREEN, Style.RESET_ALL, msg))
    print()

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
    timer = 500
    # display Wait message to user
    spinner = Halo(text="[LOADING]      Waiting for Print Portal to finish fetching data ",
                   spinner=Spinners.bouncingBar.value, placement='right', text_color='cyan')
    spinner.start()
    WebDriverWait(browser, timer).until(
        EC.invisibility_of_element((By.CLASS_NAME, "loadingoverlay")))
    spinner.stop()


def move_file(filename, fg):
    source_folder = 'C:\\Users\\{}\\Downloads'.format(os.getlogin())
    destination_folder = 'pdf'
    rename_file = "{}-({})".format(filename, fg)

    print_info_message(
        "Rename the Download file and add suffix: {}".format(fg))
    os.rename(os.path.join(source_folder, filename + '.pdf'),
              os.path.join(source_folder, rename_file + '.pdf'))

    print_info_message("Checking if '{}' folder contains {}.pdf".format(
        destination_folder, filename))
    if os.path.isfile(os.path.join(destination_folder, rename_file + ".pdf")):
        print_info_message("{}.pdf found. Deleting the file to avoid duplications...".format(
            rename_file))
        os.remove(os.path.join(destination_folder, rename_file + ".pdf"))

    print_info_message("Moving '{}-{}' from '{}' folder to '{}' folder.".format(filename,
                                                                                fg, os.path.basename(source_folder), os.path.basename(destination_folder)))
    shutil.move(os.path.join(source_folder, rename_file + '.pdf'),
                destination_folder)


def checking_folder():
    destination_folder = 'pdf'

    print_info_message("Checking if the destination files exists...")
    if not os.path.exists(destination_folder):
        print_info_message(
            "Destination folder not exists. Creating the folder now.")
        os.mkdir("pdf")
