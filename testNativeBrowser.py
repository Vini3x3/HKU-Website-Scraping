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
from myutil.testsuit import testsuit2 as testsuit

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

def test_get_url(browser, *_):    
    browser.get(urls[0])         
def test_get_page_source(browser, *_):
    html = ''            
    html = browser.page_source
    if html != html_answer:
        print('page_source not equal')
        return False
    else:
        return True
def test_simple_wait(browser, *_):    
    browser.get(urls[0])
    start_time = time()
    browser.wait(5)
    end_time = time()
    if 4 < end_time - start_time < 6:
        return True
    else:
        return False

def test_advanced_wait(browser, *_):
    browser.get(urls[1])
    start_time = time()
    browser.wait(5, 'presence_of_element_located', 'ID', 'aswift_0')
    end_time = time()
    if end_time - start_time < 6:
        return True
    else:
        return False
def test_create_tab(browser, *_):
    browser.tab('firstsite', urls[2])
    browser.tab('secondsite', urls[3])
def test_switch_tab(browser):    
    browser.tab(0)
    browser.tab('firstsite')        
def test_destroy_tab(browser, *_):    
        browser.untab('secondsite')
def test_destroy_browser(browser, *_):        
    browser.quit()

if __name__ == '__main__':
    A = testsuit()

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
        A.log('field', browser_name)
        A.log('test', 0, 'create browser')
        try:        
            browser = klass()
            test_result['create browser']=True
        except:
            test_result['create browser']=False
        if test_result['create browser']:
            key = 'get url'
            A.log('test', 1, key)
            test_result[key] = A.compileTest(browser, testground=test_get_url)
        if test_result['get url']:
            key = 'get page_source'
            A.log('test', 2, key)
            test_result[key] = A.compileTest(browser, testground=test_get_page_source)        
        if test_result['get url']:        
            key = 'simple wait'
            A.log('test', 3, 'simple wait')
            test_result['simple wait'] = A.compileTest(browser, testground=test_simple_wait)
        if test_result['get url']:                
            key = 'advanced wait'
            A.log('test', 4, key)
            test_result[key] = A.compileTest(browser, testground=test_advanced_wait)
        if test_result['get url']:
            key = 'create new tab'
            test_result[key] = test_create_tab(browser)
            A.log('test', 5, key)
            test_result['create new tab'] = A.compileTest(browser, testground=test_create_tab)
        if test_result['create new tab']:        
            key = 'switch tab'
            A.log('test', 6, key)
            test_result[key] = A.compileTest(browser, testground=test_switch_tab)        
        if test_result['create new tab']:        
            key = 'destroy tab'
            A.log('test', 7, key)
            test_result[key]=A.compileTest(browser, testground=test_destroy_tab)
        if test_result['get url']:     
            key = 'destroy browser'
            A.log('test', 8, key)
            test_result[key]=A.compileTest(browser, testground=test_destroy_browser)
        A.log('doublesep')    
        A.log('report', browser_name)
        for key, val in test_result.items():        
            A.log('result', key, str(val))
        A.log('doublesep')