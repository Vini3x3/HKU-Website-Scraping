"""import libraries"""
from myscraper.NativeBrowser import *
from bs4 import BeautifulSoup as bs
from time import time
from traceback import print_exc
# from myutil.testsuit import testsuit2 as testsuit
from myutil import testsuit

"""settings"""
browser_names = ['Chrome', 'Firefox', 'Edge']

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
@testsuit.compileTest
def test_get_url(browser):
    browser.get(urls[0])
    if browser.current_url != urls[0]:
        return False


@testsuit.compileTest
def test_get_page_source(browser):
    html = ''
    html = browser.page_source
    if html != html_answer:
        print('page_source not equal')
        return False
    else:
        return True


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


@testsuit.compileTest
def test_create_tab(browser):
    browser.tab('firstsite', urls[2])
    browser.tab('secondsite', urls[3])


@testsuit.compileTest
def test_switch_tab(browser):
    browser.tab(0)
    browser.tab('firstsite')


@testsuit.compileTest
def test_destroy_tab(browser):
    browser.untab('secondsite')


@testsuit.compileTest
def test_destroy_browser(browser):
    browser.quit()


@testsuit.timedTest(repeat=10)
def main_test(browser_name):
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
    try:
        browser = NewBrowser({'browser': browser_name})
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
        test_result['destroy tab'] = test_destroy_tab(browser)
    if test_result['create browser']:
        test_result['destroy browser'] = test_destroy_browser(browser)


if __name__ == '__main__':

    for browser_name in browser_names:
        time = main_test(browser_name)
        print(time, browser_name)
        # browser = NewBrowser({'browser': browser_name})
