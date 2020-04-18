from myscraper.NativeBrowser import NewBrowser
# from myscraper.webmanager import SiteManager
from mydev.changes import SiteManager
from myutil.testsuit import testsuit2 as testsuit
from traceback import print_exc

def testground(browser, manager, *_):
    manager.scrape('getSiteMap', browser)
def errorhandler(*_):
    print_exc()
def endtest(browser, manager, *_):
    manager.destroy(browser)
    browser.quit()

credential = {
    'username': '',
    'password': '',
}

webscrape_settings = {     
    'site': 'Moodle',
    'browser': 'Firefox',
}

manager = SiteManager(credential, webscrape_settings)
browser = NewBrowser(webscrape_settings)
manager.start(browser)
testunit = testsuit()
result = testunit.timedTest(browser, manager, repeat=10, testground=testground)
print(result)
manager.destroy(browser)
browser.quit()