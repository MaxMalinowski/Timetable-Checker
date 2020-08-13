from scraper import Scraper
from parser import Parser


def main():
    webcrawler = Scraper()
    try:
        webcrawler.login()
        webcrawler.navigate_to_timetable()
        webcrawler.set_period(3)
        webcrawler.extract_timetable()
    except Exception as e:
        print(e.with_traceback())
    finally:
        webcrawler.logout()
        webcrawler.browser.close()

    data_parser = Parser()



if __name__ == '__main__':
    main()
