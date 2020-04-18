from seleniumrequests import Firefox, Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as BY
from selenium.webdriver.common.keys import Keys as KEY


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

from time import sleep

import weberror

class Browser:
    # basic functions
    def __init__(self, webscrape_settings = None):        
        self.debug = False
        self.tabDict = {}
        if webscrape_settings:
            if 'debug' in webscrape_settings.keys():
                self.debug = webscrape_settings['debug']
        
    def __str__(self):
        return 'Selenre' + self.__class__.__name__
    def __del__(self):
        self.tabDict = {}
    def test(self):
        print('hello browser')
    def manage_browser(self, browser_option, browser_path, webscrape_settings = None):        
        if not webscrape_settings:
            return {'options':None, 'path':browser_path}
        else:
            if 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                for _ in webscrape_settings['options']:
                    browser_option.add_argument(_)
                return {'options':browser_option, 'path':webscrape_settings['path']}
            elif 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' not in webscrape_settings.keys():
                for _ in webscrape_settings['options']:
                    browser_option.add_argument(_)
                return {'options':browser_option, 'path':browser_path}
            elif 'options' not in webscrape_settings.keys() and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                return {'options':None, 'path':webscrape_settings['path']}
            else:
                return {'options':None, 'path':browser_path}
            
    
    # extended functions
    def wait(self, time = 0, ec = None, by = None, elem = None, ):
        if self.debug:
            print(ec, by, elem, time)
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
    def pressKey(self, key):
        return getattr(KEY, key)    


class NewFirefox(Browser, Firefox):
    def __init__(self, webscrape_settings = None):
        Browser.__init__(self,webscrape_settings)
        # if not webscrape_settings:
        #     Firefox.__init__(self)
        # else:
        #     if 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
        #         options = webdriver.FirefoxOptions()
        #         for _ in webscrape_settings['options']:
        #             options.add_argument(_)
        #         Firefox.__init__(self, options=options, executable_path=webscrape_settings['path'])
        #     elif 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' not in webscrape_settings.keys():
        #         options = webdriver.FirefoxOptions()
        #         for _ in webscrape_settings['options']:
        #             options.add_argument(_)                
        #         Firefox.__init__(self, options=options)
        #     elif 'options' not in webscrape_settings.keys() and 'path' in webscrape_settings.keys() and webscrape_settings['path']:                
        #         Firefox.__init__(self, executable_path=webscrape_settings['path'])
        #     else:
        #         Firefox.__init__(self)
        browser_args = Browser.manage_browser(webdriver.FirefoxOptions(), 'geckodriver', webscrape_settings)
        Firefox.__init__(self, options=browser_args['options'], executable_path=browser_args['path'])

    def __str__(self):
        return 'Selenre' + self.__class__.__name__
    def test(self):
        Browser.test(self)


class Firefox(Firefox):

    def __init__(self, webscrape_settings = None):        
        self.debug = False
        self.tabDict = {}
        if not webscrape_settings:
            super().__init__()
        else:
            if 'debug' in webscrape_settings.keys() and webscrape_settings['debug']:
                self.debug = True
                            
            if 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                options = webdriver.FirefoxOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                super().__init__(options=options, executable_path=webscrape_settings['path'])
            elif 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' not in webscrape_settings.keys():
                options = webdriver.FirefoxOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                super().__init__(options=options)
            elif 'options' not in webscrape_settings.keys() and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                super().__init__(executable_path=webscrape_settings['path'])
            else:
                super().__init__()
            
    def test(self):
        print('Hello '+ self.__class__.__name__)

    def __str__(self):
        return 'Selenre' + self.__class__.__name__

    def wait(self, time = 0, ec = None, by = None, elem = None, ):
        if self.debug:
            print(ec, by, elem, time)
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

    def pressKey(self, key):
        return getattr(KEY, key)


class Chrome(Chrome):

    def __init__(self, webscrape_settings = None):        
        self.debug = False
        self.tabDict = {}
        if not webscrape_settings:
            super().__init__()
        else:
            if 'debug' in webscrape_settings.keys() and webscrape_settings['debug']:
                self.debug = True
                            
            if 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                options = webdriver.ChromeOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                super().__init__(options=options, executable_path=webscrape_settings['path'])
            elif 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' not in webscrape_settings.keys():
                options = webdriver.ChromeOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                super().__init__(options=options)
            elif 'options' not in webscrape_settings.keys() and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                super().__init__(executable_path=webscrape_settings['path'])
            else:
                super().__init__()
            
    def test(self):
        print('Hello '+ self.__class__.__name__)

    def __str__(self):
        return 'Selenre' + self.__class__.__name__

    def wait(self, time = 0, ec = None, by = None, elem = None, ):
        if self.debug:
            print(ec, by, elem, time)
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

    def pressKey(self, key):
        return getattr(KEY, key)

"""
class Edge(Edge):

    def __init__(self, webscrape_settings = None):        
        self.debug = False
        self.tabDict = {}
        if not webscrape_settings:
            return super().__init__()
        else:
            if 'debug' in webscrape_settings.keys() and webscrape_settings['debug']:
                self.debug = True
                            
            if 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                options = webdriver.EdgeOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                return super().__init__(options=options, executable_path=webscrape_settings['path'])
            elif 'options' in webscrape_settings.keys() and webscrape_settings['options'] and 'path' not in webscrape_settings.keys():
                options = webdriver.EdgeOptions()
                for _ in webscrape_settings['options']:
                    options.add_argument(_)
                return super().__init__(options=options)
            elif 'options' not in webscrape_settings.keys() and 'path' in webscrape_settings.keys() and webscrape_settings['path']:
                return super().__init__(executable_path=webscrape_settings['path'])
            else:
                return super().__init__()
            
    def test(self):
        print('Hello '+ self.__class__.__name__)

    def __str__(self):
        return 'Selenre' + self.__class__.__name__

    def wait(self, time = 0, ec = None, by = None, elem = None, ):
        if self.debug:
            print(ec, by, elem, time)
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

    def pressKey(self, key):
        return getattr(KEY, key)
"""        