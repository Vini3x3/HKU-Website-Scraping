from bs4 import BeautifulSoup as bs
from myutil import webutil, weberror
import inspect
from datetime import datetime

class Website:
    def __init__(self):
        self.sitemap = []
        self.sitelinks = {}
        self.cache = []
        self.sitename = ''
    def __del__(self):        
        self.sitemap.clear()
        self.sitelinks.clear()
        self.cache.clear()
    def __str__(self):
        return 'This is a Webite instance'
    def printdebug(self, msg):
        if self.debug: print('[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))
    def getSiteMap(self):
        pass
    def login(self):
        pass
    def logout(self):
        pass
    def keepAlive(self):
        pass
    def keepAlive(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        browser.get(self.sitelinks['home'])
        self.printdebug('end')
    def destroy(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        self.logout(browser)
        browser.untab(self.sitename)
        self.printdebug('end')
    def test(self, msg):
        print('this is a test')
        print(msg)


class BasicMoodle(Website):
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """    
    def __init__(self, credential, webscrape_settings=None):        
        super().__init__()
        self.sitelinks = {
            'home': 'https://moodle.hku.hk',
            'login': 'http://moodle.hku.hk/login',
            'login_sublink_1': 'https://moodle.hku.hk/login/index.php?authCAS=CAS',
            'login_sublink_2': 'https://moodle.hku.hk/login/index.php',
            'logout': 'https://moodle.hku.hk/login/logout.php?sesskey=',
            
            'help'                  : 'https://moodle.hku.hk/help.php?',
            'force_download'        : 'https://moodle.hku.hk/pluginfile.php/',

            'grade'                 : 'https://moodle.hku.hk/grade/report/index.php?id=',
            'course'                : 'https://moodle.hku.hk/course/view.php?id=',
            'contact'               : 'https://moodle.hku.hk/user/index.php?id=',
            'user'                  : 'https://moodle.hku.hk/user/view.php?id=',
            'resource'              : 'https://moodle.hku.hk/mod/resource/view.php?id=',
            'submit_file_upload'    : 'https://moodle.hku.hk/mod/assign/view.php?id=',
            'submit_turnitin'       : 'https://moodle.hku.hk/mod/turnitintooltwo/view.php?id=',
            'url'                   : 'https://moodle.hku.hk/mod/url/view.php?id=',
            'page'                  : 'https://moodle.hku.hk/mod/page/view.php?id=',
            'forum'                 : 'https://moodle.hku.hk/mod/forum/view.php?id=',
            'discussion'            : 'https://moodle.hku.hk/mod/forum/discuss.php?d=',
            'quiz'                  : 'https://moodle.hku.hk/mod/quiz/view.php?id=',   
            'folder'                : 'https://moodle.hku.hk/mod/folder/view.php?id=',            
            'questionnaire'         : 'https://moodle.hku.hk/mod/questionnaire/view.php?id=',
            'choice'                : 'https://moodle.hku.hk/mod/choice/view.php?id=',     
            'choicegroup'           : 'https://moodle.hku.hk/mod/choicegroup/view.php?id=',
            'lab'                   : 'https://moodle.hku.hk/mod/lti/view.php?id=',
            'feedback'              : 'https://moodle.hku.hk/mod/feedback/view.php?id=',
            'vpl'                   : 'https://moodle.hku.hk/mod/vpl/view.php?id=',

            'submission_deadlines'  : 'https://moodle.hku.hk/my/?myoverviewtab=timeline',
        } 
        self.sitename = 'Moodle'
        self.credential = credential
        if webscrape_settings and 'verbose' in webscrape_settings and webscrape_settings['verbose']>0:
            self.debug = True
        else:
            self.debug = False

    def __str__(self):
        return 'This is a Moodle Instance'
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """ 
    def start(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename, self.sitelinks['login'])
        self.login(browser)
        browser.wait(3, 'presence_of_element_located', 'ID', 'frontpage-course-list')        
        self.sitemap = self.getSiteMap(browser)
        self.printdebug('end')

    def login(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        browser.get(self.sitelinks['login'])
        browser.find_element_by_id('login-nav-btn').click()        
        browser.wait(1)
        self.printdebug('branch')
        if browser.current_url == self.sitelinks['home'] or browser.current_url == self.sitelinks['home']+'/':            
            self.printdebug('end case 1')
        else:
            if browser.current_url == self.sitelinks['login_sublink_2']:
                browser.get(self.sitelinks['login_sublink_1'])
                webutil.util_universal_hku_login(browser, self.credential)
                self.printdebug('end case 2')
            elif browser.current_url == self.sitelinks['login_sublink_1']:
                webutil.util_universal_hku_login(browser, self.credential)
                self.printdebug('end case 3')
            else:
                self.printdebug('end case error')
                self.printdebug(browser.current_url)

    def logout(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        exit_link = ''        
        browser.get(self.sitelinks['home'])
        response_html = browser.page_source
        soap = bs(response_html, features='lxml')
        menu = soap.find('ul',{'id':'action-menu-0-menu'})    
        elem_as = menu.find_all('a')
        links = [elem_a['href'] for elem_a in elem_as]
        for link in links:        
            if self.sitelinks['logout'] in link:
                exit_link = link
        browser.get(exit_link)
        self.printdebug('end')
    
    def getSiteMap(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)        
        browser.get(self.sitelinks['home'])        
        soup = bs(browser.page_source, features = 'lxml')
        link_map = []
        boxes = soup.find_all('div',{'class':'coursebox'})
        self.printdebug('find box')
        for box in boxes:
            course_id = box['data-courseid']
            course_name = box.find('h3').get_text()
            link_map.append((course_name, 'course', int(course_id)))
        self.printdebug('end')
        return link_map    
    
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

class BasicPortal(Website):
    """
    Base Class Function
    """
    def __init__(self, credential, webscrape_settings=None):
        # storage        
        super().__init__()
        self.credential = credential
        self.sitelinks = {
            'login'                 : 'https://hkuportal.hku.hk/login.html',

            'home'                  : 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',

            'weekSch'               : 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W',
            'grades'                : 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL?',            
            'invoice'               : 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_CHRGS_DUE.GBL?',
            'receipt'               : 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_PMT_HIST.GBL?',
        }
        self.sitename = 'Portal'
        self.credential = credential        
        if webscrape_settings and 'verbose' in webscrape_settings and webscrape_settings['verbose']>0:
            self.debug = True            
        else:
            self.debug = False

    def __str__(self):
        return 'This is a Portal Instance'
    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """ 
    def start(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename, self.sitelinks['login'])
        self.login(browser)
        browser.wait(2, 'presence_of_element_located', 'ID', 'ADMN_Z_HKU_STUDENTNOTICE_HMPG')        
        self.sitemap = self.getSiteMap(browser)
        self.printdebug('end')
    
    def login(self, browser):        
        self.printdebug('start')
        browser.get(self.sitelinks['login'])
        webutil.util_universal_hku_login(browser, self.credential)
        self.printdebug('end')

    def logout(self,browser):        
        self.printdebug('start')
        browser.get(self.sitelinks['home'])
        browser.find_element_by_link_text('Sign out').click()
        self.printdebug('end')
    
    def getSiteMap(self, browser):        
        self.printdebug('start')
        result = []        
        browser.tab(self.sitename)
        browser.get(self.sitelinks['home'])
        soap = bs(browser.page_source, features='lxml')
        for link in soap.find_all("a"):
            if link['href'][0:4] == 'http':
                result.append(link['href'])
        if len(result)<=0:
            raise weberror.ScrapeError(0)
        else:
            self.printdebug('end')
            return result
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """
    # wait for the extension class

