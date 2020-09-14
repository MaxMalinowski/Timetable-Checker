import json
import logging

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
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.browser = Chrome(options=chrome_options)
        self.browser.implicitly_wait(20)
        self.browser.get('https://terminal-mszi.de/LS/-339999550/SIS')
        # Set timeout
        self.__timeout = 5
        # Set current working directory
        self.__dir = directory
        # Set username and password
        with open(self.__dir + ".config/data.json") as json_file:
            data = json.load(json_file)
            self.__username = data["credentials"]["username"]
            self.__password = data["credentials"]["password"]
        logging.info('Successfully initialized Scraper-Object')

    def __switch_to_iframe(self):
        logging.info('Switching to iframe')
        self.browser.switch_to.frame(self.browser.find_elements_by_tag_name('iframe')[0])

    def __switch_from_iframe(self):
        logging.info('Switching to default content')
        self.browser.switch_to.default_content()

    def __click_wrapper(self, xpath):
        logging.info('Clicking element ' + xpath)
        element = self.browser.find_element_by_xpath(xpath)
        element.click()
        return element

    def __wait_wrapper(self, xpath):
        try:
            WebDriverWait(self.browser, self.__timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            logging.info('Element ' + xpath + ' was clicked')
        except TimeoutException:
            logging.info('Element' + xpath + ' was not clicked due to not clickability')

    def login(self):
        self.__click_wrapper('//*[@id="benutzername"]').send_keys(self.__username)
        self.__click_wrapper('//*[@id="passwort"]').send_keys(self.__password)
        self.__click_wrapper('//*[@id="login"]/button')
        logging.info('Successfully logged in')

    def logout(self):
        self.browser.get('https://www.terminal-mszi.de/LS/LGN/Logout')
        logging.info('Successfully logged out')

    def navigate_to_timetable(self):
        self.__wait_wrapper('//*[@id="hamburgerMenue"]')
        self.__wait_wrapper('//*[@id="esLayoutNavigation"]/ul/li/span/span[2]')
        self.__wait_wrapper('//*[@id="esLayoutNavigation"]/ul/li/ul/li[2]/a')
        logging.info('Successfully reached the timetable view')

    def set_period(self, period):
        view_period_map = {ord('0'): 'days', ord('1'): 'workweek', ord('2'): 'week', ord('3'): 'month'}
        xpath = '//*[@id="ctl00_ContentPlaceHolder_Content_ctl00_Body_ec_Body_esb_cbpS_cbZeitraum_'
        self.__switch_to_iframe()
        self.__wait_wrapper(xpath + 'B-1"]')
        self.__wait_wrapper(xpath + 'DDD_L_LBI#T0"]'.replace('#', str(period)))
        self.__switch_from_iframe()
        logging.info('Successfully set view period to ' + str(period).translate(view_period_map))

    def extract_timetable(self):
        self.__switch_to_iframe()
        element = self.browser.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder_Content_ctl00_Body_ec_Body_esb_cbpS_sdrUebersicht_containerBlock_content"]')
        html = bs(element.get_attribute('innerHTML'), features="html.parser").prettify()
        with open(self.__dir + ".config/tmp.html", "w") as html_file:
            html_file.write(html)
        self.__switch_from_iframe()
        logging.info('Successfully saved html table to tmp.html file')
