"""
Test Metrics: 
For each browse: 
    - Create browser
    - get url
    - print page_source
    - wait (simple)
    - wait (BY)
    - create new tab
    - switch tab
    - destroy new tab    
    - Destroy browser

And the route as below: 
[0]: create browser
if [0] fails, test end.
[1]: get url
if [1] fails, go to [8].
if [3]/[4] fails, go to [5].
if [5]/[6]/[7] fails, go to [8]
"""

"""import libraries"""
# from NativeBrowser import *
from myscraper.NativeBrowser import *
from bs4 import BeautifulSoup as bs
from time import time
from traceback import print_exc
# from myutil.testsuit import testsuit2 as testsuit
from myutil import testsuit

"""settings"""
browser_names = ['NewFirefox', 'NewChrome', 'NewEdge']

"""test settings"""
html_answer = """<html><head></head><body><header>
<title>http://info.cern.ch</title>
</header>

<h1>http://info.cern.ch - home of the first website</h1>
<p>From here you can:</p>
<ul>
<li><a href="http://info.cern.ch/hypertext/WWW/TheProject.html">Browse the first website</a></li>
<li><a href="http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html">Browse the first website using the line-mode browser simulator</a></li>
<li><a href="http://home.web.cern.ch/topics/birth-web">Learn about the birth of the web</a></li>
<li><a href="http://home.web.cern.ch/about">Learn about CERN, the physics laboratory where the web was born</a></li>
</ul>

</body></html>"""

urls = [
    'http://info.cern.ch/',
    'https://home.cern/',
    'http://info.cern.ch/hypertext/WWW/TheProject.html',
    'http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html'
]

"""test cases"""


@testsuit.log('test', 1, 'get url')
@testsuit.compileTest
def test_get_url(browser):
    browser.get(urls[0])
    if browser.current_url != urls[0]:
        return False


@testsuit.log('test', 2, 'get page_source')
@testsuit.compileTest
def test_get_page_source(browser):
    html = ''
    html = browser.page_source
    if html != html_answer:
        print('page_source not equal')
        return False
    else:
        return True


@testsuit.log('test', 3, 'simple wait')
@testsuit.compileTest
def test_simple_wait(browser):
    browser.get(urls[0])
    start_time = time()
    browser.wait(5)
    end_time = time()
    if 4 < end_time - start_time < 6:
        return True
    else:
        return False


@testsuit.log('test', 4, 'advanced wait')
@testsuit.compileTest
def test_advanced_wait(browser):
    browser.get(urls[1])
    start_time = time()
    browser.wait(5, 'presence_of_element_located', 'ID', 'aswift_0')
    end_time = time()
    if end_time - start_time < 6:
        return True
    else:
        return False


@testsuit.log('test', 5, 'create tab')
@testsuit.compileTest
def test_create_tab(browser):
    browser.tab('first_site', urls[2])
    browser.tab('second_site', urls[3])


@testsuit.log('test', 6, 'switch tab')
@testsuit.compileTest
def test_switch_tab(browser):
    browser.tab(0)
    browser.tab('first_site')


@testsuit.log('test', 7, 'destroy tab')
@testsuit.compileTest
def test_destroy_tab(browser):
    browser.untab('second_site')


@testsuit.log('test', 8, 'destroy browser')
@testsuit.compileTest
def test_destroy_browser(browser):
    browser.quit()


if __name__ == '__main__':

    for browser_name in browser_names:
        klass = globals()[browser_name]
        test_result = {
            'create browser': None,
            'get url': None,
            'get page_source': None,
            'simple wait': None,
            'advanced wait': None,
            'create new tab': None,
            'switch tab': None,
            'destroy tab': None,    
            'destroy browser': None,
        }
        testsuit.printlog('field', browser_name)
        testsuit.printlog('test', 0, 'create browser')
        try:        
            browser = klass()
            test_result['create browser'] = True
        except:
            test_result['create browser'] = False
        if test_result['create browser']:            
            test_result['get url'] = test_get_url(browser)
        if test_result['get url']:            
            test_result['get page_source'] = test_get_page_source(browser)
            test_result['simple wait'] = test_simple_wait(browser)
            test_result['advanced wait'] = test_advanced_wait(browser)
            test_result['create new tab'] = test_create_tab(browser)
        if test_result['create new tab']:
            test_result['switch tab'] = test_switch_tab(browser)        
            test_result['destroy tab']=test_destroy_tab(browser)            
        if test_result['create browser']:
            test_result['destroy browser']=test_destroy_browser(browser)
        testsuit.printlog('doublesep')
        testsuit.printlog('report', browser_name)
        for key, val in test_result.items():
            testsuit.printlog('result', key, str(val))        
        testsuit.printlog('doublesep')
