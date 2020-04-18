from bs4 import BeautifulSoup as bs
from selenium import webdriver

import traceback
import time

class Website:
    def __init__(self, webscrape_settings):
        self.browser = self.makeBrowser(webscrape_settings)
    def __del__(self):
        self.browser.quit()
    def __str__(self):
        return 'This is a Site instance'
    def getSiteMap(self):
        pass
    def login(self):
        pass
    def logout(self):
        pass
    def keepAlive(self):
        pass
    def makeBrowser(self, webscrape_settings):
        """
        return a driver object, call 'driver'
        """        
        if webscrape_settings['browser'] == 'Chrome':
            if not webscrape_settings['headless']:
                return webdriver.Chrome()
            else:
                options = webdriver.ChromeOptions()
                options.add_argument('-headless')
                return webdriver.Chrome(options=options)
        elif webscrape_settings['browser'] == 'FireFox':
            if not webscrape_settings['headless']:          
                return webdriver.Firefox()
            else:
                options = webdriver.FirefoxOptions()
                options.add_argument('-headless')
                return webdriver.Firefox(options=options)
        else:
            print('setting error')
            return
        
    def universal_hku_login(self, browser, credential):
        username = browser.find_element_by_id('username')
        username.send_keys(credential['username'])
        password = browser.find_element_by_id('password')
        password.send_keys(credential['password'])
        password.submit()
        time.sleep(1)    
    
    def util_getELEMfromProperties(self, selenium_object, tag_name, feature_dict):
        """
        This function is for getting the selenium object from other properties.  
        the selenium_boject is a selenium object, get from self.browser or self.browser.find('......')
        the feature_dict is like {'class': 'abc'} that for BS4
        the tag_name is a string of the tag name of the target element
        """
        targets = selenium_object.find_elements_by_tag_name(tag_name)        
        
        for target in targets:
            match = True
            for key, value in feature_dict.items():
                if match:   
                    if target.get_attribute(key) != value:
                        match = False
            if match:
                return target
