"""import libraries"""
from myscraper.NativeBrowser import *
from bs4 import BeautifulSoup as bs
from time import time
from traceback import print_exc
from myutil.testsuit import testsuit3 as testsuit


@testsuit.timedTest(repeat=10)
def scrape_element(browser, url, id):
    browser.get(url)
    html = browser.find_element_by_id(id).get_attribute('innerHTML')
    bs(html, features="lxml")


@testsuit.timedTest(repeat=10)
def parse_page(browser, url, id):
    browser.get(url)
    soup = bs(browser.page_source, features="lxml")
    soup.find('div', id=id)
    

if __name__ == '__main__':
    url = 'https://www.python.org/'
    id = 'dive-into-python'
    class_ = 'flex-slideshow slideshow'
    browser = NewBrowser({'browser': 'Firefox'})
    time = scrape_element(browser, url, id)
    print(time)
    time = parse_page(browser, url, id)
    print(time)
    browser.quit()
