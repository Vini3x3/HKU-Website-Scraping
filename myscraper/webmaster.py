from myscraper.NativeBrowser import NewBrowser
from myscraper.HKUSites import getWebsite
from myutil import weberror

import inspect
import threading
from datetime import datetime

class WebMaster:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """
    def __init__(self, credential, webscrape_settings=None):
        self.websites = {}
        self.threads = []
        self.record = []
        self.browser = None
        self.credential = credential
        self.webscrape_settings = self.initSettings(webscrape_settings)
        self.debug = self.webscrape_settings['verbose'] > 0
        self.webscrape_settings['verbose'] -= 1
        self.mutex = threading.Lock()
        self.createBrowser()
        self.initWebsite()
        self.initThread()

    def initSettings(self, webscrape_settings):
        result = {
            'browser': 'Chrome',
            'headless': True,
            'initialize-website': 'Only Portal',
            'verbose': 0
        }
        if webscrape_settings:
            for key,val in result.items():
                if key in webscrape_settings.keys():
                    result[key] = webscrape_settings[key]
        return result

    def __del__(self):
        self.printdebug('start')        
        for key in list(self.websites):
            self.deleteWebsite(key)
        try:
            self.browser.quit()
        except:
            pass
        self.record.clear()
        self.printdebug('end')

    def __str__(self):
        return 'WebMaster'
    """
    -------------------------------------
    | Browser Related                   |
    -------------------------------------
    """

    def createBrowser(self):
        self.printdebug('start')
        self.browser = NewBrowser(self.webscrape_settings)
        self.printdebug('end')

    def needBrowser(func, *args):
        def wrapper(self, *args):
            self.mutex.acquire()            
            self.printdebug('start')
            result = func(self, *args)
            self.printdebug('end')
            self.mutex.release()
            return result
        return wrapper
    """
    -------------------------------------
    | Website Related                   |
    -------------------------------------
    """

    def initWebsite(self):
        self.printdebug('start')
        self.printdebug(self.webscrape_settings['initialize-website'])
        if self.webscrape_settings['initialize-website']=='All':
            for website_name in ['Portal', 'Moodle']:
                self.createWebsite(website_name)
        elif self.webscrape_settings['initialize-website']=='Only Portal':
            self.createWebsite('Portal')
        self.printdebug('end')

    @needBrowser
    def createWebsite(self, website_name):
        self.printdebug('start')
        self.printdebug(website_name)
        tempdict = self.webscrape_settings.copy()
        tempdict['site'] = website_name
        self.websites[website_name] = getWebsite(website_name, self.credential, tempdict)
        self.websites[website_name].start(self.browser)
        self.printdebug('end')

    @needBrowser
    def deleteWebsite(self, website_name):
        self.printdebug('start')
        self.websites[website_name].destroy(self.browser)
        del self.websites[website_name]
        self.printdebug('end')

    """
    -------------------------------------
    | Record Related                    |
    -------------------------------------
    """

    def formatRecord(self, website_name, func_name, *args):
        msg = ''  
        for _ in args:
            msg += str(_) + ', '
        return '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), website_name, func_name, msg)
    def addRecord(self, website_name, func_name, *args):
        self.record.append(self.formatRecord(website_name, func_name, *args))

    def getRecord(self):
        return self.record

    """
    -------------------------------------
    | Thread Related                    |
    -------------------------------------
    """

    def initThread(self):
        # multithreading for stayAlive
        self.printdebug('start')
        self.terminate_flag = threading.Event()
        self.keepAliveThread = threading.Thread(target=self.stayAlive)
        self.keepAliveThread.start()
        self.printdebug('end')

    def terminateThread(self):
        self.printdebug('start')
        self.terminate_flag.set()
        self.keepAliveThread.join()
        self.printdebug('end')

    def stayAlive(self):
        while not self.terminate_flag.is_set():
            self.printdebug('start')
            self.refresh()
            self.printdebug('end')
            if self.terminate_flag.wait(timeout=1500):
                break

    @needBrowser
    def refresh(self):
        for each in self.websites.values():
            each.refresh(self.browser)
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def query(self, website_name, func_name, *args):
        if website_name not in self.websites.keys():
            self.createWebsite(website_name)
        self.addRecord(website_name, func_name, *args)
        return self.scrape(website_name, func_name, *args)

    @needBrowser
    def scrape(self, website_name, func_name, *args):
        if hasattr(self.websites[website_name], func_name):
            func = getattr(self.websites[website_name], func_name)
            self.printdebug('call function')
            try:
                result = func(self.browser, *args)
            except:
                self.printdebug('function error')
                result = []
            self.printdebug('end')
            return result
        else:
            self.printdebug('no such function')
            # raise weberror.CallError(0)
            return []

    @needBrowser
    def test(self):
        self.printdebug('hello world')

    def printdebug(self, msg):        
        if self.debug: print('[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))
    