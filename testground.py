from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from myscraper.NativeBrowser import NewChrome as Chrome
from mydev import changes2, changes
from mydev.changes2 import *
# from myutil import testsuit
from myutil.testsuit import testsuit3 as testsuit
from myutil import webutil
from traceback import print_exc
from time import time


def inittest():
    credential = {
        'username': 'u3537502',
        'password': 'YourMother62329197',
    }

    webscrape_settings = {
        # 'browser': 'Edge',
        # 'headless': False,
        # 'verbose': 0,
        # 'initialize-website': 'All',
    }
    browser = Chrome(webscrape_settings)
    website = Moodle(credential, webscrape_settings)
    website.start(browser)
    return browser, website


def errorhandler(*_):
    print_exc()


def endtest(browser, website):
    website.destroy(browser)
    browser.quit()


def validate(data):
    print(data)


@testsuit.log('field', 'testground')
def testground(browser, website):
    # result = website.sitemapSearchAll('Discrete')
    # result = website.parseCourseHTML(browser, 'https://moodle.hku.hk/course/view.php?id=71754')
    soup_dict = website.scrapeAssignment(browser, 'https://moodle.hku.hk/mod/assign/view.php?id=1737811')
    # print(soup_dict.keys())
    # print(soup_dict.values())
    # result_dict = website.extractAssignment(soup_dict)
    # print(result_dict.keys())
    # for _ in result:
    #     if _[1].path in website.contenttype:
    #         print('{:50},{}'.format(_[0], website.contenttype[_[1].path]) )
    #         # print(_[0], website.contenttype[_[1].path])
    #     else:
    #         # print(_[0], _[1].path)
    #         print('{:50}:{}'.format(_[0], _[1].path))
    # print(result[0])
    start_time = time()
    result = website.scrapeGrades(browser, 'a')
    # print(result)
    gradeTable = website.extractGrade(result)
    # print(result)
    # for _ in result:
    #     print(_)
    print(start_time - time())
    start_time = time()
    result = website.scrapeGrades(browser, 'a')
    gradeTable = website.extractGrade(result)
    # print(_)
    print(start_time - time())
    start_time = time()
    result = website.scrapeGrades(browser, 'a')
    gradeTable = website.extractGrade(result)
    # print(_)
    print(start_time - time())
    # result = website.findWeeklySchedule(browser, '25/01/2020','8:00AM','11:00PM')
    # result = website.findTranscript(browser)
    # result = website.findInvoice(browser)
    # print(result)


# testsuit.inittest = inittest
# testsuit.testground = testground
# testsuit.endtest = endtest
# testsuit.errorhandler = errorhandler
# testsuit.validate = validate
# testsuit.test()

# u = urlparse('https://moodle.hku.hk/course/view.php?id=71754')
# print(u)
# print(urlunparse(u))
# print(u.path)
# params = dict(parse_qsl(u.query))
# print(params)
# print(u.host+u.path+urlencode(params))

from myscraper.webmaster import WebMaster
import re

credential = {
    'username': 'u3537502',
    'password': 'YourMother62329197',
}

# credential = {
#     'username': 'approach',
#     'password': '123456789yht',
# }

webscrape_settings = {
    # 'browser': 'Edge',
    # 'headless': False,
    # 'verbose': 3,
    # 'initialize-website': 'All',
}


@testsuit.log('field', 'testground')
@testsuit.errorTest
def mytestground(webmaster):
    # webmaster.query('Moodle','scrapeAssignment', 'https://moodle.hku.hk/mod/assign/view.php?id=1737811')
    # result = webmaster.query('Moodle','sayHello')
    # result = webmaster.query('Moodle','getSiteMap')
    result = webmaster.query('Moodle','findAllCoursesByKeywords', 'comp')

    # result = webmaster.query('Moodle', 'scrapeCourseContents', 'https://moodle.hku.hk/course/view.php?id=43519')
    # result = webmaster.query('Moodle', 'scrapeCourseContentPreview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
    # result = webmaster.query('Portal', 'f indInvoiceQuery', ['TOTAL_DUE'])
    # result = webmaster.query('Portal', 'findInvoice')
    # result = webmaster.query('Portal', 'findTranscript')
    # result = webmaster.query('Portal', 'findAccountActivity')
    # result = webmaster.query('Portal', 'findReceipt')
    # result = webmaster.query('Portal', 'findWeeklySchedule', '25/01/2020', '8:00AM', '11:00PM')
    # result = webmaster.query('Portal', 'sayHello', ['msg'])

    for _ in result:
    print(_)
    # print(result)


webmaster = WebMaster(credential, webscrape_settings)
mytestground(webmaster)
webmaster.terminateThread()


