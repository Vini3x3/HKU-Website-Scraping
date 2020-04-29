from selenium.webdriver import Firefox, Chrome, Edge, FirefoxOptions, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as BY
from selenium.webdriver.common.keys import Keys as KEY

from time import sleep
from myutil import weberror
"""
***For BY***

CLASS_NAME = 'class name'
CSS_SELECTOR = 'css selector'
ID = 'id'
LINK_TEXT = 'link text'
NAME = 'name'
PARTIAL_LINK_TEXT = 'partial link text'
TAG_NAME = 'tag name'
XPATH = 'xpath'

***For KEY***
ADD, ALT, 
ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT, ARROW_UP
BACKSPACE, BACK_SPACE
CANCEL, CLEAR, COMMAND, CONTROL, DECIMAL, DELETE, DIVIDE, , DOWN, END, ENTER, EQUALS, ESCAPE
F1-F12, 
HELP, HOME, INSERT, LEFT, LEFT_ALT, LEFT_CONTROL, LEFT_SHIFT, META, MULTIPLY, NULL
NUMPAD0 - NUMPAD9, 
PAGE_DOWN, PAGE_UP, PAUSE, RETURN, RIGHT, SEMICOLON, SEPARATOR, SHIFT
SPACE, SUBTRACT, TAB, UP 
"""


class Browser:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """
    def __init__(self, headless=True, options=[], path=''):
        self.tabDict = {}

    def __str__(self):
        return 'Selenre' + self.__class__.__name__

    def __del__(self):
        self.tabDict = {}
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """
    def test(self):
        print('hello browser')

    def press_key(self, key):
        return getattr(KEY, key)

    def wait(self, time=0, ec=None, by=None, elem=None):
        if time == 0:
            return
        elif not ec and not by and not elem:
            sleep(time)
            return
        elif ec and by and elem and time:
            wait = WebDriverWait(self, time)
            by_attr = getattr(BY, by)
            ec_func = getattr(EC, ec)
            result = wait.until(ec_func((by_attr, elem)))
            return result
        else:
            raise weberror.CallError(3)

    def tab(self, target, arg=None):
        if target is None:
            raise weberror.CallError(3)
        if isinstance(target, int) and target<len(self.tabDict):
            self.switch_to.window(self.window_handles[target])
        else:
            if target not in self.tabDict.keys():
                if not arg:
                    raise weberror.CallError(3)
                else:
                    self.execute_script("window.open('"+arg+"');")
                    index = len(self.tabDict) + 1
                    self.tabDict[target] = index
                    self.switch_to.window(self.window_handles[index])
            else:
                index = self.tabDict[target]
                self.switch_to.window(self.window_handles[index])

    def untab(self, target):
        if not target:
            raise weberror.CallError(3)
        else:
            if target not in self.tabDict.keys():
                raise weberror.CallError(3)
            else:
                index = self.tabDict[target]
                self.switch_to.window(self.window_handles[index])
                self.execute_script('window.close()')
                self.tabDict.pop(target)
                for key in self.tabDict.keys():
                    if self.tabDict[key] > index:
                        self.tabDict[key] -= 1


class NewFirefox(Browser, Firefox):
    def __init__(self, headless=True, options=[], path='myengine\geckodriver'):
        browser_options = FirefoxOptions()
        for _ in options:
            browser_options.add_argument(_)
        browser_options.headless = headless
        Firefox.__init__(self, options=browser_options, executable_path=path)
        Browser.__init__(self)

    def __str__(self):
        return Browser.__str__(self)


class NewChrome(Browser, Chrome):
    def __init__(self, headless=True, options=[], path='myengine\chromedriver'):
        browser_options = ChromeOptions()
        for _ in options:
            browser_options.add_argument(_)
        browser_options.headless = headless
        browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        Chrome.__init__(self, options=browser_options, executable_path=path)
        Browser.__init__(self)

    def __str__(self):
        return Browser.__str__(self)


class NewEdge(Browser, Edge):
    def __init__(self, headless=True, options=[], path='myengine\MicrosoftWebDriver'):
        # browser_options = EdgeOptions()
        # for _ in options:
        #     browser_options.add_argument(_)
        # Edge.__init__(self, options=browser_options, executable_path=path)
        Edge.__init__(self, executable_path=path)
        Browser.__init__(self)

    def __str__(self):
        return Browser.__str__(self)


def get_browser(browser, **kwargs):
    browsers = ['Chrome', 'Firefox', 'Edge']
    if browser not in browsers:
        raise weberror.CallError(4)
    else:
        klass = globals()['New' + browser]
        return klass(**kwargs)

