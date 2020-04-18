from myscraper.webmaster import WebMaster
from traceback import print_exc

"""
This set contains 3 major things that you should know: 

1. webutil is updated, so the updated version is here.  Thus, an updated version is here.  
2. testsuit is updated.  It is created by me to test things.  Feel free to use if you need.  
3. changes2.py is a bit messy, but I will expalin one by one: 
    - switchTab: a decorator function that will switch to the target website's tab.  
      (P.S. You can turn off the browser headless mode to see how it works.  )
    - probe: a function that helps to see if the length of HTML is changed or not.  
    - init: new things added, cachesize (for caching), mycache ( for function caching) and htmlcache (for record HTML length in probe function)
    - (P.S. the init has some problem, it cannot init from webmaster.  But I will fix that bug later.  Now just enjoy the 128 default cachesize)
    
    - The above are the basic things, and below is how to make things work together: 
    - Basically every scraper function follows the same suit.  Below is the abstraction: 
    @switchTab
    def findXXX(self, browser, any_argument):
        # any code
        url = 'abc
        # breakpoints for checking if the html has changed or not
        if self.probe(browser, url):
            return self.mycache[self.hashfunc(inspect.stack()[0][3], any_argument)]
        # breakpoints for checking if the html has changed or not
        browser.get(url)
        # any code
        result = xxx
        #breakpoint for storing in mycache
        self.mycache[self.hashfunc(inspect.stack()[0][3], any_argument)] = result
        #breakpoint for storing in mycache
        return result
    - You can see these example like findTranscript and findInvoice.  
    - One more thing: myutil.webutil has a function call util_soup2list(soup_obj).  That can convert a bs4 obj of a html table into list.   
    - Examples are as illustrated in the this file.  
    - For any enquiry, please contact Vincent Chu for further details. 
"""

credential = {
    'username': '',
    'password': '',
}

webmaster = WebMaster(credential)
print('create')
try:
    result = webmaster.query('Portal','findInvoice')
    for key, val in result.items():
        print(key)
        print(type(val))    
    table = result['Z_BILLPAYH2_TBL']
    for _ in table:
        print(_)

    print("===========")
    result = webmaster.query('Portal','findTranscript')
    for key, val in result.items():
        print(key)
        print(type(val))    
    table = result['GPA']
    for _ in table:
        print(_)
except:
    print_exc()
finally:
    webmaster.terminateThread()
    print('terminate')


# examples on how to use the test function in testsuit3
from myutil.testsuit import testsuit3 as testsuit

# see any problem when it runs
@testsuit.log('test', 1, 'riskycode')
@testsuit.compileTest
def testSafety(webmaster):
    webmaster.query('Portal','findWeeklySchedule', '25/01/2020','8:00AM','11:00PM')

# see how long it runs
@testsuit.log('test', 2, 'cachetools')
@testsuit.timedTest(repeat=10)
def testCaching(webmaster):
    webmaster.query('Portal','findWeeklySchedule', '25/01/2020','8:00AM','11:00PM')

testsuit.printlog('field', 'Simple Testsuit3')
webmaster = WebMaster(credential)
try:
    valid = testSafety(webmaster)
    print(valid)
    testsuit.printlog('log', 'finish testSafety')
    time = testCaching(webmaster)
    print(time)    
except:
    print_exc()
finally:
    webmaster.terminateThread()
testsuit.printlog('doublesep')
testsuit.printlog('report', 'Simple Testsuit3')
testsuit.printlog('result', 'riskycode', valid)
testsuit.printlog('result', 'cachetools', time)
testsuit.printlog('doublesep')


# advaced usage
testsuit.printlog('field', 'Advanced Testsuit3')
def inittest():
    credential = {
        'username': '',
        'password': '',
    }    
    webmaster = WebMaster(credential)    
    return webmaster
def errorhandler(webmaster):
    print_exc()
def endtest(webmaster):
    webmaster.terminateThread()
def validate(data):
    print(type(data))
    testsuit.printlog('log', data)
    return data < 15
@testsuit.timedTest(repeat=10)
def testground(webmaster):
    result = webmaster.query('Portal','findInvoice')
    # for key, val in result.items():
    #     print(key)
    #     print(type(val))    
    table = result['Z_BILLPAYH2_TBL']
    # for _ in table:
    #     print(_)
    # print("===========")
    result = webmaster.query('Portal','findTranscript')
    # for key, val in result.items():
    #     print(key)
    #     print(type(val))    
    table = result['GPA']
    # for _ in table:
    #     print(_)

testsuit.inittest = inittest
testsuit.testground = testground
testsuit.endtest = endtest
testsuit.errorhandler = errorhandler
testsuit.validate = validate
testsuit.test()
testsuit.printlog('doublesep')
