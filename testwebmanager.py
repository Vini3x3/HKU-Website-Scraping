from myscraper.NativeBrowser import NewBrowser
# from myscraper.webmanager import SiteManager
from mydev.changes import SiteManager
from myutil import testsuit

"""settings"""
scrape_time = 0

@testsuit.log('test',1,'start')
@testsuit.compileTest
def test_start(browser, manager):    
    manager.start(browser)    
    if browser.current_url != manager.website.sitelinks['home']:        
        return False

@testsuit.log('test',2,'scrape')
@testsuit.compileTest
def test_scrape(browser, manager):
    manager.scrape('getSiteMap', browser)

@testsuit.log('test',3,'cache')
@testsuit.timedTest(repeat=10)
def test_cache(browser, manager):
    manager.scrape('getSiteMap', browser)

# @testsuit.log('test',4,'clear cache')
# @testsuit.compileTest
# def test_clear_cache(browser, manager):
#     manager.clear_cache()

@testsuit.log('test',4,'destroy manager')
@testsuit.compileTest
def test_destroy_manager(browser, manager):
    manager.destroy(browser)

credential = {
    'username': '',
    'password': '',
}

testsuit.printlog('field','WebManager')
sites = ['Portal', 'Moodle']
browsers = ['Chrome', 'Firefox', 'Edge']
for site in sites:
    for browser_name in browsers:
        webscrape_settings = {     
            'site': site,
            'browser': browser_name,
        }
        test_result = {
            'create manager': None,
            'start': None,
            'scrape': None,
            'cache': None,
            # 'clear cache': None,
            'destroy manager': None,
        }
        browser = NewBrowser(webscrape_settings)
        testsuit.printlog('test', 0, 'create manager')
        try:
            manager = SiteManager(credential, webscrape_settings)
        except:
            test_result['create manager'] = False
        test_result['create manager'] = True        
        if test_result['create manager'] == True:
            manager = SiteManager(credential, webscrape_settings)
            test_result['start'] = test_start(browser, manager)            
            if test_result['start']:
                if browser.current_url != manager.website.sitelinks['home'] and browser.current_url != manager.website.sitelinks['home'] + '/':
                    test_result['start'] = False            
        if test_result['start']:
            test_result['scrape'] = test_scrape(browser, manager)
        if test_result['scrape']:
            scrape_time = test_cache(browser, manager)     
            testsuit.printlog('log', 'time = '+str(scrape_time))
            test_result['cache'] = scrape_time < 2
            # test_result['clear cache'] = test_clear_cache(browser, manager)                
            # if test_result['clear cache']:
            #     time = test_cache(browser, manager)                
            #     testsuit.printlog('log', 'time = '+str(time))
            #     if time < scrape_time:
            #         test_result['clear cache'] = False
        if test_result['start']:
            test_result['destroy manager'] = test_destroy_manager(browser, manager)

        browser.quit()

        testsuit.printlog('doublesep')
        testsuit.printlog('report', site+' '+browser_name)
        for key, val in test_result.items():
            testsuit.printlog('result', key, str(val))        
        testsuit.printlog('doublesep')

