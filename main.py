import logging
import pathlib

from modules.scraper import Scraper


class Checker:

    current_directory = str(pathlib.Path().absolute()) + '/'

    def __init__(self):
        logging.basicConfig(filename='timetable-checker.log',
                            format='%(asctime)s - %(levelname)s ==> %(message)s',
                            level=logging.INFO)

    def check(self, period):
        webcrawler = Scraper(self.current_directory)
        try:
            webcrawler.login()
            webcrawler.navigate_to_timetable()
            webcrawler.set_period(period)
            webcrawler.extract_timetable()
        except Exception as e:
            logging.error("Exception while checking timetable: " + str(e))
        finally:
            webcrawler.logout()
            webcrawler.browser.close()

    def parse(self):
        pass

    def inform(self):
        pass


def main():
    timetable_checker = Checker()
    timetable_checker.check(3)


if __name__ == '__main__':
    main()
