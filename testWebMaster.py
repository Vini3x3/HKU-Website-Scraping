"""
Test Metrics: 
- refresh browser
- query
- get record
"""

from myscraper.webmaster import WebMaster
from myutil import testsuit
import re
from time import sleep


@testsuit.log('test', 1, 'needBrowser')
@testsuit.compileTest
def test_need_browser(webmaster):
    webmaster.test()


@testsuit.log('test', 2, 'refresh')
@testsuit.compileTest
def test_refresh(webmaster):
    webmaster.refresh()


@testsuit.log('test', 3, 'query')
@testsuit.compileTest
def test_query(webmaster):
    webmaster.query('Moodle', 'get_sitemap')


@testsuit.log('test', 4, 'record')
@testsuit.compileTest
def test_record(webmaster):
    record = webmaster.get_record()
    r = re.compile('[ .*-.*-.* .*:.*:.*..* ] .* > .* : .*')
    if r.match(record[0]) is not None:    
        print ('matches')
        if 'Moodle' in record[0] and 'get_sitemap' in record[0]:
            return True
        else:
            return False
    return False


@testsuit.log('test', 5, 'terminateThread')
@testsuit.compileTest
def test_terminate_thread(webmaster):
    webmaster.cancel()


@testsuit.log('test', 6, 'destroy webmaster')
@testsuit.compileTest
def test_destroy_webmaster(webmaster):
    del webmaster


credential = {
    'username': '',
    'password': '',
}
test_result = {
    'create webmaster': None,
    'needBrowser': None,
    'refresh': None,
    'query': None,
    'record': None,
    'terminateThread': None,
    'destroy webmaster': None,
}

if __name__ == '__main__':    
    testsuit.printlog('field', 'Web Master')
    testsuit.printlog('test', 0, 'create webmaster')
    try:
        webmaster = WebMaster(credential['username'], credential['password'], headless=False)
        test_result['create webmaster'] = True
    except:
        test_result['create webmaster'] = False
    if test_result['create webmaster']:
        test_result['needBrowser'] = test_need_browser(webmaster)
    if test_result['needBrowser']:
        test_result['refresh'] = test_refresh(webmaster)
        test_result['query'] = test_query(webmaster)
        test_result['record'] = test_record(webmaster)
    if test_result['create webmaster']:
        test_result['terminateThread'] = test_terminate_thread(webmaster)
        test_result['destroy webmaster'] = test_destroy_webmaster(webmaster)
    webmaster.cancel()
    testsuit.printlog('doublesep')
    testsuit.printlog('report', 'WebMaster')
    for key, val in test_result.items():
        testsuit.printlog('result', key, str(val))
    testsuit.printlog('doublesep')
