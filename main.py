import logging
import pathlib

from modules.scraper import Scraper
from modules.parser import Parser


class Checker:

    current_directory = str(pathlib.Path().absolute()) + '/'

    def __init__(self):
        logging.basicConfig(filename='timetable-checker.log',
                            format='%(asctime)s - %(levelname)s ==> %(message)s',
                            level=logging.INFO)
        logging.info('Timebale Checker Started')

    def check(self, period):
        logging.info('Checking timetable started')
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
            logging. info('Checking timetable finished')

    def parse(self):
        logging.info('Parsing data started')
        parser = Parser(self.current_directory)
        parser.extract_grob()
        logging.info('Parsing data finished')

    def inform(self):
        pass


def main():
    timetable_checker = Checker()
    #timetable_checker.check(3)
    timetable_checker.parse()
    logging.info('Timebale Checker Finished\n\n')


if __name__ == '__main__':
    main()
