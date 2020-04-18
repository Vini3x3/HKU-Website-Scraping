from bs4 import BeautifulSoup
# from selenium import webdriver

import time

import website
import weberror

class Library(website.Website):

    """
    Base Class Function
    """

    def __init__(self, credential, webscrape_settings):
        self.credential = credential
        self.sitelinks = {
            # 'home': 'https://julac.hosted.exlibrisgroup.com/primo-explore/account?vid=HKU&amp=&amp=&amp=&section=overview',
            'home': 'https://julac.hosted.exlibrisgroup.com/primo-explore/account?vid=HKU&section=overview',
            'login': 'https://hkall-shib.hosted.exlibrisgroup.com/pds?func=load-login&calling_system=primo&institute=HKU_ALMA&lang=und&url=https://julac.hosted.exlibrisgroup.com:443/primo_library/libweb/pdsLogin?targetURL=https://julac.hosted.exlibrisgroup.com/primo-explore/account?vid=HKU&fromLogin=true&from-new-ui=1&authenticationProfile=HKALL_PDS',
            'exam': 'https://exambase.lib.hku.hk/exhibits/show/exam/home',
            'submit_exam': 'javascript:check_form();'
        }
        self.debug = webscrape_settings['debug']
        # Let's rock and roll
        super().__init__(webscrape_settings)
        self.login()
        self.sitemap = self.getSiteMap()
    
    def __del__(self):        
        self.logout()
        super().__del__()        
    
    def __str__(self):
        return 'This is a Library Instance'
    
    def login(self):        
        self.browser.get(self.sitelinks['login'])
        if self.browser.current_url == self.sitelinks['home']:
            return
        else:
            # WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((BY.XPATH, "//input[@name='userid")))
            time.sleep(1)
            self.browser.find_element_by_xpath("//input[@name='userid']").send_keys(self.credential['username'])
            self.browser.find_element_by_xpath("//input[@name='password']").send_keys(self.credential['password'])
            self.util_getELEMfromProperties(self.browser, 'button', {'type': 'submit'}).click()
            time.sleep(5)
            return
    
    def logout(self):
        self.browser.get(self.sitelinks['home'])        
        time.sleep(2)
        self.util_getELEMfromProperties(self.browser, 'button', {'class': 'user-button user-menu-button button-with-menu-arrow md-button md-primoExplore-theme md-ink-ripple', 'type': 'button'}).click()
        time.sleep(3)
        self.browser.find_element_by_id('signOutButton').click()
    
    def getSiteMap(self):
        return []
    
    def keepAlive(self):
        self.browser.get(self.sitelinks['home'])        
    
    """
    Extra Function
    """
    
    def searchPaper(self, options):
        new_options = options
        # step 1: Check the options        
        if 'the_key' not in new_options or len(new_options['the_key'])<=0:
            return 'no keywords'
        if 'the_field' in new_options:
            if new_options['the_field'] == 'Paper Title':
                new_options['the_field']='ti'
            elif new_options['the_field'] == 'Course Number / Course Code':
                new_options['the_field']='crs'
            elif new_options['the_field'] == 'Full Text':
                new_options['the_field']='fulltext'
            else:
                new_options['the_field']='ti'
        if 'fromYear' in new_options:
            if new_options['fromYear'] < 1961:
                new_options['fromYear'] = 1961
        if 'toYear' in new_options:
            # time.localtime( time.time() )[0] is the current year in int
            if new_options['fromYear'] > time.localtime( time.time() )[0]:            
                new_options['fromYear'] = time.localtime( time.time() )[0]
        if 'the_sem1' in new_options and 'the_sem2' in new_options:
            if not new_options['the_sem1'] and not new_options['the_sem2']:
                new_options['the_sem1'] = True
        if 'the_ptype1' in new_options and 'the_ptype1' in new_options:
            if not new_options['the_ptype1'] and not new_options['the_ptype2']:
                new_options['the_ptype1'] = True
        if 'the_sort' in new_options:
            if new_options['the_sort'] == 'Title, Year':
                new_options['the_sort'] = 't'
            elif new_options['the_sort'] == 'Year, Title':
                new_options['the_sort'] = 'd'
            else:
                new_options['the_sort'] = 't'
        if 'the_no_result' in new_options:
            if new_options['the_no_result'] != 10 and new_options['the_no_result'] != 20 and new_options['the_no_result'] != 50 :
                new_options['the_no_result'] = 20
        
        # step 2: implement the options
        self.browser.get(self.sitelinks['exam'])
        self.browser.find_element_by_xpath('//input[@name="the_key"]').send_keys(new_options['the_key'])
        if 'the_field' in new_options:
            pass
               
            