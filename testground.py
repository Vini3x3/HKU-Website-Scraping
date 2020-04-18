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
        'username': '',
        'password': '',
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
    'username': '',
    'password': '',
}

webscrape_settings = {
    # 'browser': 'Edge',
    # 'headless': False,    
    # 'verbose': 0,
    # 'initialize-website': 'All',
}
webmaster = WebMaster(credential)
print('create')
try:
    result = webmaster.query('Portal','findInvoice')
    for key, val in result.items():
        print(key)
        print(type(val))
    print('action')    
    table = result['Z_BILLPAYH2_TBL']
    for _ in table:
        print(_)
except:
    print_exc()
finally:
    webmaster.terminateThread()
    print('terminate')
