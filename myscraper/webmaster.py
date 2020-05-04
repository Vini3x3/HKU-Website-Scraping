from myscraper.NativeBrowser import get_browser
from myscraper.HKUSites import get_website
from myutil import weberror

import inspect
import threading
from datetime import datetime


class WebMaster(threading.Timer):
    """
    -------------------------------------
    | Thread Basics                     |
    -------------------------------------
    """
    def __init__(self, username, password, init_setting='Only Portal', verbose=0, cachesize=128, interval=1200, function=None, browser_name='Chrome', headless=True, options=[], **kwargs):
        # inherent
        super().__init__(interval, function)
        self.function = self.refresh

        # setting
        self.websites = {}
        self.record = []
        self.browser = None
        self.debug = verbose > 0
        self.mutex = threading.Lock()

        # copy arguments
        self.init_setting = init_setting
        self.username = username
        self.password = password
        self.verbose = verbose
        self.cachesize = cachesize

        # initialize
        self.browser = get_browser(browser_name, headless=headless, options=options, **kwargs)
        self.print_debug(self.init_setting)
        if self.init_setting == 'All':
            for website_name in ['Portal', 'Moodle']:
                self.create_website(website_name)
        elif self.init_setting == 'Only Portal':
            self.create_website('Portal')

    def run(self):
        while not self.finished.is_set():
            self.function()
            self.finished.wait(self.interval)

    def need_browser(func):
        def wrapper(self, *args, **kwargs):
            self.mutex.acquire()
            self.print_debug('begin')
            result = func(self, *args, **kwargs)
            self.print_debug('end')
            self.mutex.release()
            return result
        return wrapper

    @need_browser
    def refresh(self):
        self.print_debug('begin')
        for each in self.websites.values():
            each.refresh(self.browser)
        self.print_debug('end')

    def cancel(self):
        self.print_debug('begin')
        super().cancel()
        for key in list(self.websites):
            self.delete_website(key)
        try:
            self.browser.quit()
        except:
            pass
        self.print_debug('end')

    """
    -------------------------------------
    | Website Related                   |
    -------------------------------------
    """
    @need_browser
    def create_website(self, website_name):
        self.print_debug('begin')
        self.print_debug(website_name)
        self.websites[website_name] = get_website(website_name, self.username, self.password, cachesize=self.cachesize, verbose=self.verbose-1)
        self.websites[website_name].start(self.browser)
        self.print_debug('end')

    @need_browser
    def delete_website(self, website_name):
        self.print_debug('begin')
        self.websites[website_name].destroy(self.browser)
        del self.websites[website_name]
        self.print_debug('end')
    """
    -------------------------------------
    | Record Related                    |
    -------------------------------------
    """
    def format_record(self, website_name, func_name, *args):
        msg = ''
        for _ in args:
            msg += str(_) + ', '
        return '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), website_name, func_name, msg)

    def add_record(self, website_name, func_name, *args):
        self.record.append(self.format_record(website_name, func_name, *args))

    def get_record(self):
        return self.record

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    @need_browser
    def test(self):
        self.print_debug('hello world')

    def print_debug(self, msg):
        if self.debug:
            print(
                '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg)
            )

    def query(self, website_name, func_name, *args, **kwargs):
        if website_name not in self.websites.keys():
            self.create_website(website_name)
        self.add_record(website_name, func_name, *args)
        return self.scrape(website_name, func_name, *args, **kwargs)

    @need_browser
    def scrape(self, website_name, func_name, *args, **kwargs):
        if hasattr(self.websites[website_name], func_name):
            func = getattr(self.websites[website_name], func_name)
            self.print_debug('call function')
            result = func(self.browser, *args, **kwargs)
            self.print_debug('end')
            return result
        else:
            self.print_debug('no such function')
            raise weberror.CallError(0)

