from bs4 import BeautifulSoup as bs
from selenium import webdriver

import traceback
import time

import website
import weberror

class HKUSites(website.Website):

    """
    Base Class Function
    """

    def __init__(self, credential, webscrape_settings):        
        # storage
        self.credential = credential
        self.sitelinks = {
            'Portal':{
                'login': 'https://hkuportal.hku.hk/login.html',
                'home': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
                'weekSch': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W',
                'grades': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL?',
                'grades2': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL?',
            },
            'Moodle': {
                'home': 'https://moodle.hku.hk',
                'login': 'http://moodle.hku.hk/login',
                'login_sublink_1': 'https://moodle.hku.hk/login/index.php?authCAS=CAS',
                'login_sublink_2': 'https://moodle.hku.hk/login/index.php',
                'logout': 'https://moodle.hku.hk/login/logout.php?sesskey=',

                'resource': 'https://moodle.hku.hk/mod/resource/view.php?',
                'submit_file_upload': 'https://moodle.hku.hk/mod/turnitintooltwo/view.php?id=',
                'submit_turnitin': 'https://moodle.hku.hk/mod/assign/view.php?id=',            
                'grade': 'https://moodle.hku.hk/grade/report/index.php?id=',
                'url': 'https://moodle.hku.hk/mod/url/view.php?id=',
                'submit_answer': 'https://moodle.hku.hk/mod/assign/view.php?id=',
                'forum': 'https://moodle.hku.hk/mod/forum/view.php?id=',
            },
            'Library': {
                'home': 'https://julac.hosted.exlibrisgroup.com/primo-explore/account?vid=HKU&amp=&amp=&amp=&section=overview',
                'login': 'https://hkall-shib.hosted.exlibrisgroup.com/pds?func=load-login&calling_system=primo&institute=HKU_ALMA&lang=und&url=https://julac.hosted.exlibrisgroup.com:443/primo_library/libweb/pdsLogin?targetURL=https://julac.hosted.exlibrisgroup.com/primo-explore/account?vid=HKU&fromLogin=true&from-new-ui=1&authenticationProfile=HKALL_PDS',
                'exam': 'https://exambase.lib.hku.hk/exhibits/show/exam/home',
                'submit_exam': 'javascript:check_form();'
            }
        }
                
        self.debug = webscrape_settings['debug']        
        # Let's rock and roll        
        super().__init__(webscrape_settings)
        self.login()
        # self.sitemap = self.getSiteMap()

    def __del__(self):
        self.logout()
        super().__del__()

    def __str__(self):
        return 'This is a Portal Instance'    

    def login(self):
        """
        input a browser object and sign in
        """
        self.Portal_login()
        if self.debug: print('Portal Logout')
        self.Moodle_login()
        if self.debug: print('Moodle Login')        
        self.Library_login()
        if self.debug: print('Library Logout')

        if self.debug: print('Success Login')

    def logout(self):
        """
        exit by inputing a browser object
        """
        self.Library_logout()
        if self.debug: print('Library Logout')
        self.Moodle_logout()
        if self.debug: print('Moodle Logout')
        self.Portal_logout()
        if self.debug: print('Portal Logout')
        
        if self.debug: print('Success Logout')

    def Portal_login(self):
        self.browser.get(self.sitelinks['Portal']['login'])
        self.util_universal_hku_login(self.browser, self.credential)

    def Moodle_login(self):
        self.browser.get(self.sitelinks['Moodle']['login'])
        self.browser.find_element_by_id('login-nav-btn').click()
        time.sleep(1)
        if self.browser.current_url != self.sitelinks['Moodle']['home'] and self.browser.current_url != self.sitelinks['Moodle']['home']+'/':        
            if self.browser.current_url == self.sitelinks['Moodle']['login_sublink_2']:
                self.browser.get(self.sitelinks['Moodle']['login_sublink_1'])
                self.util_universal_hku_login(self.browser, self.credential)
            elif self.browser.current_url == self.sitelinks['Moodle']['login_sublink_1']:
                self.util_universal_hku_login(self.browser, self.credential)
    
    def Library_login(self):
        self.browser.get(self.sitelinks['Library']['login'])        
        time.sleep(7)
        print(self.browser.current_url)
        if self.browser.current_url != self.sitelinks['Library']['home']:
            
            self.browser.find_element_by_xpath("//input[@name='userid']").send_keys(self.credential['username'])
            self.browser.find_element_by_xpath("//input[@name='password']").send_keys(self.credential['password'])
            self.util_getELEMfromProperties(self.browser, 'button', {'type': 'submit'}).click()
            time.sleep(5)
    
    def Portal_logout(self):
        self.browser.get(self.sitelinks['Portal']['home'])
        self.browser.find_element_by_link_text('Sign out').click()

    def Moodle_logout(self):
        exit_link = ''
        # r = self.browser.request('GET', self.sitelinks['Moodle']['home'])
        # soap = bs(r.text, features='lxml')
        self.browser.get(self.sitelinks['Moodle']['home'])
        soap = bs(self.browser.page_source, features='lxml')

        menu = soap.find('ul',{'id':'action-menu-0-menu'})    
        if not menu:
            raise weberror.ScrapeError(0)
        elem_as = menu.find_all('a')        
        links = [elem_a['href'] for elem_a in elem_as]    
        for link in links:        
            if self.sitelinks['Moodle']['logout'] in link:
                exit_link = link
        if exit_link == '':
            raise weberror.ScrapeError(1)
        else:
            self.browser.get(exit_link)

    def Library_logout(self):
        self.browser.get(self.sitelinks['Library']['home'])        
        time.sleep(2)
        self.util_getELEMfromProperties(self.browser, 'button', {'class': 'user-button user-menu-button button-with-menu-arrow md-button md-primoExplore-theme md-ink-ripple', 'type': 'button'}).click()
        time.sleep(2)
        self.browser.find_element_by_id('signOutButton').click()

    def getSiteMap(self):
        result = []
        r = self.browser.request('GET', self.sitelinks['home'])
        soap = bs(r.text, features='lxml')
        for link in soap.find_all("a"):
            if link['href'][0:4] == 'http':
                result.append(link['href'])        
        if len(result)<=0:
            raise weberror.ScrapeError(0)
        else:
            return result

    def keepAlive(self):
        self.browser.get(self.sitelinks['home'])        

    """
    Extra Class Function
    """

    def findWeeklySchedule(self, argv):
        """
        extract the HTML weekly schedule
        argv = [date, starttime, endtime], where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format    
        """
        # stage 1: get the frame of weekly schedule    
        weekly_schedule_url = ''
        for link in self.sitemap:
            if self.sitelinks['weekSch'] in link:
                weekly_schedule_url = link
        # self.browser.get(weekly_schedule_url)
        r1 = self.browser.request('GET', weekly_schedule_url)
        # soap = bs(self.browser.page_source, features='lxml')
        soap = bs(r1.text, features='lxml')
        frames = soap.find_all('frame')        
        for each in frames:
            if each['name'] == 'TargetContent':
                weekly_schedule_url = each['src']        
        self.browser.get(weekly_schedule_url)        

        if self.debug: print('stage 1 ends')

        # stage 2: select the right week and time range
        date = self.browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
        date.clear()
        date.send_keys(argv[0])
        start_time = self.browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')    
        start_time.clear()
        start_time.send_keys(argv[1])
        end_time = self.browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
        end_time.clear()
        end_time.send_keys(argv[2])
        refresh = self.browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL')
        refresh.click()
        
        if self.debug: print('stage 2 ends')

        # stage 3: extract the data    
        soup = bs(self.browser.page_source, features='lxml')
        table = soup.find('table', {"id": "WEEKLY_SCHED_HTMLAREA"})
        
        if self.debug: print('stage 3 ends')
        
        # stage 4: post processing
        table['class'] = 'table'
        timeLabels = table.find_all('span', {'class': 'SSSTEXTWEEKLYTIME'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'font-weight-bold'
        timeLabels = table.find_all('span', {'class': 'SSSTEXTWEEKLY'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'table-warning'

        if self.debug: print('stage 4 ends')

        return table.prettify()    

    def getStudentCourseGrades(self):
        for link in self.sitemap:
            if self.sitelinks['grades'] in link:
                r = self.browser.request('GET', link)
                soup = bs(r.text, features='lxml')
                for each in soup.find_all('frame'):
                    
                    if self.sitelinks['grades2'] in each['src']:
                                                
                        r2 = self.browser.request('GET', each['src'])

                        frame = bs(r2.text, features = 'lxml')

                        soup2 = frame.find(id='ACE_width')
                                                
                        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})                        
                        
                        # table [0] = course grades, table[1] = overall GPA
                        s = tables[0].prettify()
                        return s
                                    
                # return 'not found1'
                raise weberror.ScrapeError(0)
        # return 'not found in sitemap'
        raise weberror.ScrapeError(0)

    def getStudentGPA(self):
        for link in self.sitemap:
            if self.sitelinks['grades'] in link:
                r = self.browser.request('GET', link)
                soup = bs(r.text, features='lxml')
                for each in soup.find_all('frame'):
                    
                    if self.sitelinks['grades2'] in each['src']:
                                                
                        r2 = self.browser.request('GET', each['src'])
                        frame = bs(r2.text, features = 'lxml')
                        soup2 = frame.find(id='ACE_width')
                        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
                        
                        # table [0] = course grades, table[1] = overall GPA
                        s = tables[1].prettify()                        
                        return s
                                    
                raise weberror.ScrapeError(0)
                # return 'not found1'
        # return 'not found in sitemap'
        raise weberror.ScrapeError(0)
    
