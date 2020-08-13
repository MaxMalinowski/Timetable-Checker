import pathlib
import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs


class Scraper(Exception):

    browser = None
    __dir = None
    __timeout = None
    __username = None
    __password = None

    def __init__(self, directory):
        # Start browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = Chrome(options=chrome_options)
        self.browser.implicitly_wait(20)
        self.browser.get('https://www.terminal-mszi.de/LS/LGN/Login')
        # Set timeout
        self.__timeout = 5
        # Set current working directory
        self.__dir = directory
        # Set username and password
        with open(self.__dir + ".config/data.json") as json_file:
            data = json.load(json_file)
            self.__username = data["credentials"]["username"]
            self.__password = data["credentials"]["password"]

    def __switch_to_iframe(self):
        self.browser.switch_to.frame(self.browser.find_elements_by_tag_name('iframe')[0])

    def __switch_from_iframe(self):
        self.browser.switch_to.default_content()

    def __click_wrapper(self, xpath):
        element = self.browser.find_element_by_xpath(xpath)
        element.click()
        return element

    def __wait_wrapper(self, xpath):
        try:
            WebDriverWait(self.browser, self.__timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except TimeoutException:
            print("bla")

    def login(self):
        self.__click_wrapper('//*[@id="benutzername"]').send_keys(self.__username)
        self.__click_wrapper('//*[@id="passwort"]').send_keys(self.__password)
        self.__click_wrapper('//*[@id="login"]/button')

    def logout(self):
        self.browser.get('https://www.terminal-mszi.de/LS/LGN/Logout')

    def navigate_to_timetable(self):
        self.__wait_wrapper('//*[@id="hamburgerMenue"]')
        self.__wait_wrapper('//*[@id="esLayoutNavigation"]/ul/li/span/span[2]')
        self.__wait_wrapper('//*[@id="esLayoutNavigation"]/ul/li/ul/li[2]/a')

    def set_period(self, period):
        # period: 0-days, 1-workweek, 2-week, 3-month
        xpath = '//*[@id="ctl00_ContentPlaceHolder_Content_ctl00_Body_ec_Body_esb_cbpS_cbZeitraum_'
        self.__switch_to_iframe()
        self.__wait_wrapper(xpath + 'B-1"]')
        self.__wait_wrapper(xpath + 'DDD_L_LBI#T0"]'.replace('#', str(period)))
        self.__switch_from_iframe()

    def extract_timetable(self):
        self.__switch_to_iframe()
        element = self.browser.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder_Content_ctl00_Body_ec_Body_esb_cbpS_sdrUebersicht_containerBlock_content"]')
        html = bs(element.get_attribute('innerHTML'), features="html.parser").prettify()
        with open(self.__dir + ".config/tmp.html", "w") as html_file:
            html_file.write(html)
        self.__switch_from_iframe()
