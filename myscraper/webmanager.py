# from myscraper.HKUSites import *
from mydev.changes2 import *
from myutil import weberror, webutil
import inspect
from datetime import datetime
import cachetools

class WebManager:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """
    def __init__(self, credential, webscrape_settings=None):
        self.website = None
        self.record = []
        self.webscrape_settings = self.initSettings(webscrape_settings)        
        self.debug = self.webscrape_settings['verbose'] > 0
        self.webscrape_settings['verbose'] -= 1
        self.cachesize = self.webscrape_settings['cachesize']
    def initSettings(self, webscrape_settings):
        result = {
            'verbose': 0,
            'cachesize': 128,
        }
        if webscrape_settings:
            for key,val in result.items():
                if key in webscrape_settings.keys():
                    result[key] = webscrape_settings[key]
        return result
    def __del__(self):
        self.cache = []
        self.record = []
    def __str__(self):
        return 'WebManager'
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """
    def printdebug(self, msg):        
        if self.debug: print('[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))
    def start(self, browser):
        self.printdebug('start')
        self.website.start(browser)
        self.printdebug('end')
    def destroy(self, browser):
        self.printdebug('start')
        self.website.destroy(browser)
        self.printdebug('end')
    @cachetools.cached(cache=cachetools.LRUCache(maxsize=128), key=lambda self, func_name, browser, *args: cachetools.keys.hashkey(func_name, *args))
    def scrape(self, func_name, *args):
        if hasattr(self.website, func_name):
            func = getattr(self.website, func_name)
            self.printdebug('call function')
            result = func(*args)
            self.printdebug('end')
            return result
        else:
            self.printdebug('no such function')
            raise weberror.CallError(0)
    def refresh(self, browser):
        self.printdebug('start')
        self.website.keepAlive(browser)
        self.printdebug('end')
    def query(self, func_name, *args):
        return self.scrape(func_name, *args)
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """
    # wait for the extended class

class BasicMoodleManager(WebManager):
    def __init__(self, credential, webscrape_settings=None):
        super().__init__(credential, webscrape_settings)
        self.printdebug('finish super init')
        self.website = Moodle(credential, self.webscrape_settings)
        self.printdebug('finish website init')
    
class BasicPortalManager(WebManager):
    def __init__(self, credential, webscrape_settings=None):
        super().__init__(credential, webscrape_settings)
        self.printdebug('finish super init')
        self.website = Portal(credential, self.webscrape_settings)
        self.printdebug('finish website init')
