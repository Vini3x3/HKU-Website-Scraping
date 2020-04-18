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
    def __init__(self, webscrape_settings = None):                
        self.tabDict = {}        
    def __str__(self):
        return 'Selenre' + self.__class__.__name__
    def __del__(self):
        self.tabDict = {}    
    def initSettings(default_webdriver_path, webscrape_settings = None):                
        result = {'options':[], 'path':default_webdriver_path, 'headless':True}
        if webscrape_settings:
            for key,val in result.items():
                if key in webscrape_settings.keys():
                    result[key] = webscrape_settings[key]
        return result
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """ 
    def test(self):
        print('hello browser')
    def pressKey(self, key):
        return getattr(KEY, key)
    def wait(self, time = 0, ec = None, by = None, elem = None):
        if time == 0:
            return
        elif not ec and not by and not elem:            
            sleep(time)
            return
        elif ec and by and elem and time:            
            wait = WebDriverWait(self, time)
            BYattr = getattr(BY, by)
            ECfunc = getattr(EC, ec)
            result = wait.until(ECfunc((BYattr, elem)))
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
    def __init__(self, webscrape_settings = None):        
        browser_args = Browser.initSettings('myengine\geckodriver', webscrape_settings)        
        options = FirefoxOptions()
        for _ in browser_args['options']:
            options.add_argument(_)
        options.headless = browser_args['headless']
        Firefox.__init__(self, options=options, executable_path=browser_args['path'])        
        Browser.__init__(self)

    def __str__(self):
        return Browser.__str__(self)

class NewChrome(Browser, Chrome):
    def __init__(self, webscrape_settings = None):        
        browser_args = Browser.initSettings('myengine\chromedriver', webscrape_settings)        
        options = ChromeOptions()
        for _ in browser_args['options']:
            options.add_argument(_)
        options.headless = browser_args['headless']
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        Chrome.__init__(self, options=options, executable_path=browser_args['path'])        
        Browser.__init__(self)

    def __str__(self):
        return Browser.__str__(self)

class NewEdge(Browser, Edge):
    def __init__(self, webscrape_settings = None):        
        browser_args = Browser.initSettings('myengine\MicrosoftWebDriver', webscrape_settings)
        # options = EdgeOptions()
        # for _ in browser_args['options']:
        #     options.add_argument(_)
        # Edge.__init__(self, options=options, executable_path=browser_args['path'])
        Edge.__init__(self, executable_path=browser_args['path'])        
        Browser.__init__(self)

    def __str__(self):        
        return Browser.__str__(self)

def NewBrowser(webscrape_settings):
    browser_list = ['Chrome', 'Firefox', 'Edge']
    if webscrape_settings == None:
        raise weberror.CallError(1)
    elif not isinstance(webscrape_settings, dict):
        raise weberror.CallError(3)
    elif 'browser' not in webscrape_settings.keys():
        raise weberror.CallError(4)
    elif webscrape_settings['browser'] not in browser_list:
        raise weberror.CallError(3)
    else:
        klass = globals()['New' + webscrape_settings['browser']]
        return klass(webscrape_settings)        
            