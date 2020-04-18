from bs4 import BeautifulSoup as bs
# from selenium import webdriver

import traceback
import time

import website
import weberror

class Portal(website.Website):

    """
    Base Class Function
    """

    def __init__(self, credential, webscrape_settings):        
        # storage        
        self.credential = credential
        self.sitelinks = {
            'login': 'https://hkuportal.hku.hk/login.html',
            'home': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
            'weekSch': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W',
            'grades': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL?',
            'grades2': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL?',
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
        return 'This is a Portal Instance'    

    def login(self):
        """
        input a browser object and sign in
        """
        self.browser.get(self.sitelinks['login'])
        self.util_universal_hku_login(self.browser, self.credential)

    def logout(self):
        """
        exit by inputing a browser object
        """
        self.browser.get(self.sitelinks['home'])
        self.browser.find_element_by_link_text('Sign out').click()

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

    def getWeeklySchedule(self, argv):
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
    
