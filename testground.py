from myscraper.webmaster import WebMaster
from myutil.testsuit import testsuit2 as testsuit
from traceback import print_exc

def testground(credential, webscrape_settings, *_):
    B = WebMaster(credential, webscrape_settings)
    result = B.query('Moodle', 'getSiteMap')
    B.test()
    # for line in B.getRecord():
    #     print(line)
    B.terminateThread()
def errorhandler(*_):
    print_exc()
def endtest(browser, manager, *_):
    pass

credential = {
    'username': '',
    'password': '',
}

webscrape_settings = {    
    # 'browser': 'Edge',
    # 'headless': False,    
    'verbose': 3,
    # 'initialize-website': 'All',
}

A = testsuit()
A.test(credential, webscrape_settings, testground=testground, errorhandler=errorhandler, endtest=endtest)
