from myscraper.webmanager import *

import cachetools

def SiteManager(credential, webscrape_settings):
        manager_list = ['Moodle','Portal']
        if not webscrape_settings:
            raise weberror.CallError(2)
        elif not isinstance(webscrape_settings, dict):
            raise weberror.CallError(3)
        elif 'site' not in webscrape_settings.keys():
            raise weberror.CallError(4)
        elif webscrape_settings['site'] not in manager_list:
            raise weberror.CallError(3)
        else:
            klass = globals()[webscrape_settings['site']+'Manager']
            return klass(credential, webscrape_settings)

class MoodleManager(BasicMoodleManager):
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """
       
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

    def query(self, func_name, *args):
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            self.printdebug('call function')
            result = func(*args)
            self.printdebug('end')
            return result
        else:
            return self.scrape(func_name, *args)

    def sayHello(self, browser):
        print('hi')

    # def findCourseByKeywords(self, browser, keywords):
    #     return self.website.sitemapSearch(keywords)
    #
    # def findAllCoursesByKeywords(self, browser, keywords):
    #     return self.website.sitemapSearchAll(keywords)

    
class PortalManager(BasicPortalManager):
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """
    def query(self, func_name, *args):
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            self.printdebug('call function')
            result = func(*args)
            self.printdebug('end')
            return result
        else:
            return self.scrape(func_name, *args)
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """
    def findInvoiceQuery(self, browser, queries):
        temp = self.website.findInvoice(browser)
        result = {}
        for _ in queries:
            result[_] = temp[_]
        return result
