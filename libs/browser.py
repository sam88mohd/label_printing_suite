from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from os import getenv


class Browser:
    def __init__(self, code):
        load_dotenv()
        self.code = code
        EXECUTABLE_PATH = Path("c:\\chromedriver.exe")
        browserOptions = Options()

        browserOptions.add_argument('--ignore-certificate-errors')
        browserOptions.add_argument('--incognito')
        browserOptions.add_argument('--log-level=3')
        browserOptions.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        self.__browser = webdriver.Chrome(service=Service(
            executable_path=EXECUTABLE_PATH), options=browserOptions)
        self.__browser.get('http://edms.crbard.com/mc/login/index.cfm')
        self.USERNAME = getenv("MC-USERNAME")
        self.PASSWORD = getenv("MC-PASSWORD")
        self.__login(browser=self.__browser, USERNAME=self.USERNAME, PASSWORD=self.PASSWORD)


    @staticmethod
    def __login(browser, USERNAME, PASSWORD):
        print("Login to Master Control...")
        browser.find_element(By.ID, "username").clear()
        browser.find_element(By.ID, "username").send_keys(USERNAME)
        browser.find_element(By.ID, "password").clear()
        browser.find_element(By.ID, "password").send_keys(PASSWORD)
        browser.find_element(By.ID, "loginButton").click()

    def get_link(self):
        try:
            print(f"Start Searching for {self.code}")
            WebDriverWait(self.__browser, 10).until(
                EC.element_to_be_clickable((By.ID, "search"))).click()

            WebDriverWait(self.__browser, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "bigFrame")))

            WebDriverWait(self.__browser, 10).until(
                EC.element_to_be_clickable((By.ID, 'basicTabLink'))).click()

            self.__browser.find_element(
                By.ID, "firstText").send_keys(self.code)
            self.__browser.find_element(By.ID, "searchButton").click()

            sleep(5)
            self.__browser.switch_to.default_content()
            self.__browser.switch_to.frame(
                self.__browser.find_element(By.ID, "myframe"))
            self.__browser.find_element(By.ID, "Documents_panel").click()
            link = WebDriverWait(self.__browser, 10).until(EC.element_to_be_clickable(
                (By.ID, "titleLink1"))).get_attribute('href').split("=")
            print("Found the links!")
            return f"http://edms.crbard.com/mc/Main/MASTERControl/vault/view_doc.cfm?ls_id={link[1]}"
        except Exception:
            print("Failed to get the link url. There something wrong!")
            return False
