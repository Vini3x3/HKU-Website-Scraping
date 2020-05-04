from bs4 import BeautifulSoup as bs
import cachetools
from myutil import webutil, weberror

from datetime import datetime
import inspect
from time import time, sleep
from random import random

"""
-------------------------------------
| Global Functions                  |
-------------------------------------
"""


# Switch function to render requested object
def getWebsite(name, credential, settings=None):
    if name == 'Moodle':
        return Moodle(credential, settings)
    elif name == 'Portal':
        return Portal(credential, settings)
    else:
        raise weberror.CallError(3)


# Decorator for switing tab
def switchTab(func, *args):
    def wrapper(self, browser, *args):
        browser.tab(self.sitename)
        return func(self, browser, *args)
    return wrapper


# Decorator for caching
def cached(key):
    def decorator(function):
        @switchTab
        def wrapper(self, browser, *args):
            url = self.sitelinks[key]
            browser.get(url)
            if url in self.htmlcache.keys():
                if self.htmlcache[url] == len(browser.page_source):
                    return self.mycache[self.hashfunc(function.__name__, url, *args)]
            self.htmlcache[url] = len(browser.page_source)
            result = function(self, browser, *args)
            self.mycache[self.hashfunc(function.__name__, url, *args)] = result
            return result
        return wrapper
    return decorator



class Website:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """

    def __init__(self, credential, webscrape_settings=None):
        self.sitemap = []
        self.sitelinks = {}
        self.cache = []
        self.sitename = ''
        self.cachesize = 128
        self.mycache = cachetools.LRUCache(self.cachesize)
        self.hashfunc = cachetools.keys.hashkey
        self.htmlcache = {}
        self.credential = credential
        if 'cachesize' in webscrape_settings:
            self.cachesize = webscrape_settings['cachesize']
        if webscrape_settings and 'verbose' in webscrape_settings and webscrape_settings['verbose'] > 0:
            self.debug = True
        else:
            self.debug = False

    def __del__(self):
        self.sitemap.clear()
        self.sitelinks.clear()
        self.cache.clear()

    def __str__(self):
        return 'This is a Website instance'

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def printdebug(self, msg):
        if self.debug: print(
            '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))

    def getSiteMap(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    def refresh(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        browser.get(self.sitelinks['home'])
        self.printdebug('end')

    @switchTab
    def probe(self, browser, url):
        browser.get(url)
        if url in self.htmlcache.keys():
            if self.htmlcache[url] == len(browser.page_source):
                return True
        self.htmlcache[url] = len(browser.page_source)
        return False

    def destroy(self, browser):
        self.printdebug('start')
        browser.tab(self.sitename)
        self.logout(browser)
        browser.untab(self.sitename)
        self.printdebug('end')

    def start(self, browser):
        pass


class Moodle(Website):

    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """

    def __init__(self, credential, webscrape_settings=None):
        super().__init__(credential, webscrape_settings)
        self.sitelinks = {
            'home': 'https://moodle.hku.hk',
            'login': 'http://moodle.hku.hk/login',
            'login_sublink_1': 'https://moodle.hku.hk/login/index.php?authCAS=CAS',
            'login_sublink_2': 'https://moodle.hku.hk/login/index.php',
            'logout': 'https://moodle.hku.hk/login/logout.php?sesskey=',
            'deadlines': 'https://moodle.hku.hk/my/?myoverviewtab=timeline',
        }
        self.sitename = 'Moodle'
        self.content_type = {

            'help': 'help.php?',
            'force_download': 'pluginfile.php/',

            'grade': 'grade/report/index.php?id=',
            'course': 'course/view.php?id=',
            'contact': 'user/index.php?id=',
            'user': 'user/view.php?id=',

            'File': 'mod/resource/',
            'Assignment': 'mod/assign/',
            'submit_turnitin': 'mod/turnitintooltwo/',
            'URL': 'mod/url/',
            'Page': 'mod/page/',
            'Forum': 'mod/forum/',
            'Quiz': 'mod/quiz/',
            'folder': 'mod/folder/',
            'Questionnaire': 'mod/questionnaire/',
            'choice': 'mod/choice/',
            'Group choice': 'mod/choicegroup/',
            'External tool': 'mod/lti/',
            'feedback': 'mod/feedback/',
            'vpl': 'mod/vpl/',

        }

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
        if browser.current_url == self.sitelinks['home'] or browser.current_url == self.sitelinks['home'] + '/':
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
        menu = soap.find('ul', {'id': 'action-menu-0-menu'})
        elem_as = menu.find_all('a')
        links = [elem_a['href'] for elem_a in elem_as]
        for link in links:
            if self.sitelinks['logout'] in link:
                exit_link = link
        browser.get(exit_link)
        self.printdebug('end')

    @switchTab
    def getSiteMap(self, browser):
        self.printdebug('start')
        browser.get(self.sitelinks['home'])
        soup = bs(browser.page_source, features='lxml')
        link_map = []
        boxes = soup.find_all('div', class_='coursebox')
        self.printdebug('find box')
        for box in boxes:
            courselink = box.find('a')
            link_map.append((courselink.get_text(strip=True), courselink['href']))
        self.printdebug('end')
        return link_map

    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

    def findCourseByKeywords(self, browser, keywords):
        for row in self.sitemap:
            if keywords.lower() in row[0].lower():
                return row
        raise weberror.CallError(3)

    def findAllCoursesByKeywords(self, browser, keywords):
        return [row for row in self.sitemap if keywords.lower() in row[0].lower()]

    @switchTab
    def scrapeCourseContents(self, browser, url):
        self.printdebug('start')
        result = []
        # breakpoint
        if self.probe(browser, url):
            self.printdebug('cached')
            return self.mycache[self.hashfunc(inspect.stack()[0][3], url)]
        # breakpoint
        self.printdebug('not cached')
        browser.get(url)
        self.printdebug(browser.current_url)
        soup = bs(browser.page_source, features='lxml')
        region = soup.find('section', id='region-main')
        items = region.find_all('div', class_='activityinstance')
        self.printdebug(len(items))
        for item in items:
            instance = str(item.find('span', class_='instancename'))
            # example: <span class="instancename">News announcements<span class="accesshide"> Forum</span></span>

            if '<span class="accesshide">' in instance:

                start = instance.find('<span class="instancename">') + len('<span class="instancename">')
                middle1 = instance.find('<span class="accesshide">')
                middle2 = instance.find('<span class="accesshide">') + len('<span class="accesshide">')
                end = instance.find('</span></span>')

                name = instance[start:middle1].strip()
                type = instance[middle2:end].strip()
            else:
                name = item.find('span', class_='instancename').get_text(strip=True)
                type = ''

            if item.find('div', class_='dimmed dimmed_text'):
                link = ''
            else:
                link = item.find('a')['href']

            result.append({
                'link': link,
                'name': name,
                'type': type,
            })
        # breakpoint
        self.mycache[self.hashfunc(inspect.stack()[0][3], url)] = result
        # breakpoint
        self.printdebug('end')
        return result

    @switchTab
    def scrapeCourseContentPreview(self, browser, url):
        browser.get(url)
        filename = 'screenshot' + str(time()) + str(random()) + '.png'
        # Ref: https://stackoverflow.com/a/52572919/
        # https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
        original_size = browser.get_window_size()
        required_width = browser.execute_script('return document.body.parentNode.scrollWidth')
        required_height = browser.execute_script('return document.body.parentNode.scrollHeight')
        browser.set_window_size(required_width, required_height)
        browser.find_element_by_id('region-main').screenshot(filename)  # avoids scrollbar
        browser.set_window_size(original_size['width'], original_size['height'])
        return filename

    @cached('deadlines')
    def scrapeDeadlines(self, browser):
        url = self.sitelinks['deadlines']
        browser.get(url)
        browser.wait(1)
        soup = bs(browser.page_source, features='lxml')
        div = soup.find('div', id='myoverview_timeline_view')
        deadlines = div.findAll('li', class_='event-list-item')
        # print(len(deadlines))
        result = []

        for deadline in deadlines:
            # link = deadline.find('div', class_='event-name text-truncate')
            link = deadline.find('a', class_='event-name')
            deadlinename = link.get_text(strip=True)
            # print(deadlinename)
            self.printdebug(deadlinename)
            deadlinelink = link['href']
            self.printdebug(deadlinelink)
            deadlinetime = deadline.find('div', class_='span5').get_text(strip=True)
            self.printdebug(deadlinetime)
            result.append({
                'name': link.get_text(),
                'link': link['href'],
                'time': deadline.find('div', class_='span5 text-truncate').get_text(strip=True),
            })
        return result

    """
    -------------------------------------
    | Further Extension                 |
    -------------------------------------
    """
    def findCourseContent(self, browser, course_keywords, search_keyword='', type=[], quota=-1, reverse=False, exact=False):
        # stage 1: find course link
        try:
            course_tuple = self.findCourseByKeywords(browser, course_keywords)
        except weberror.CallError:
            print('no such course')
            return

        # stage 2: find course content
        course_url = course_tuple[1]
        try:
            course_contents = self.scrapeCourseContents(browser, course_url)
        except:
            print('failed')
            return

        # stage 3: filtering
        if search_keyword != '':
            search_keyword = search_keyword.lower()
            course_contents = [row for row in course_contents if search_keyword in row['name'].lower()]

        if len(type) > 0:
            course_contents = [row for row in course_contents if row['type'] in type]
        temp = []

        if quota > 0:
            for _type in type:
                count = quota
                if not reverse:
                    for course_content in course_contents:
                        if course_content['type'] == _type and count > 0:
                            if not exact:
                                temp.append(course_content)
                            else:
                                if count == quota:
                                    temp.append(course_content)
                            count -= 1
                else:
                    for i in range(len(course_contents)-1, 0, -1):
                        if course_contents[i]['type'] == _type and count > 0:
                            if not exact:
                                temp.append(course_contents[i])
                            else:
                                if count == 1:
                                    temp.append(course_contents[i])
                            count -= 1
            course_contents = temp.copy()
        return course_contents

    def findContentByKeywords(self, browser, course_keywords, content_keywords):
        # stage 1: find course link
        try:
            course_tuple = self.findCourseByKeywords(browser, course_keywords)
        except weberror.CallError:
            print('no such course')
            return
        # stage 2: scrape course content
        print(course_tuple[1])
        try:
            result = self.scrapeCourseContents(browser, course_tuple[1])
        except:
            print('cannot scrape course content')
            return

        # stage 3: filter course content by keywords
        temp = []
        content_keywords = content_keywords.lower()
        for _ in result:
            if content_keywords in _['name'].lower():
                temp.append(_)
        print(temp)
        return temp




    def findPageView(self, browser, course_keywords):
        # stage 1: find course link
        try:
            course_tuple = self.findCourseByKeywords(browser, course_keywords)
        except weberror.CallError:
            print('no such course')
            return

        # stage 2: find course content
        course_url = course_tuple[0]
        try:
            filename = self.scrapeCourseContentPreview(browser, course_url)
        except:
            print('failed')
            return
        return filename


class Portal(Website):
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """

    def __init__(self, credential, webscrape_settings=None):
        # storage
        super().__init__(credential, webscrape_settings)
        self.sitelinks = {
            'login': 'https://hkuportal.hku.hk/login.html',
            'home': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
            'logout': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/?cmd=logout',

            'weekSch': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W.GBL',
            'transcript': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL',
            'invoice': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_CHRGS_DUE.GBL',
            'receipt': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_PMT_HIST.GBL',
            'activity': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_ACCT_ACTVTY.GBL',
        }
        self.sitename = 'Portal'

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
        # browser.wait(2, 'presence_of_element_located', 'ID', 'ADMN_Z_HKU_STUDENTNOTICE_HMPG')
        self.sitemap = self.getSiteMap(browser)
        self.printdebug('end')

    def login(self, browser):
        self.printdebug('start')
        browser.get(self.sitelinks['login'])
        webutil.util_universal_hku_login(browser, self.credential)
        self.printdebug('end')

    def logout(self, browser):
        self.printdebug('start')
        browser.get(self.sitelinks['logout'])
        self.printdebug('end')

    @switchTab
    def getSiteMap(self, browser):
        self.printdebug('start')
        browser.get(self.sitelinks['home'])
        soup = bs(browser.page_source, features='lxml')
        link_map = []
        boxes = soup.find_all('div', class_='coursebox')
        self.printdebug('find box')
        for box in boxes:
            courselink = box.find('a')
            link_map.append((courselink.get_text(strip=True), courselink['href']))
        self.printdebug('end')
        return link_map

    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

    @cached('weekSch')
    def findWeeklySchedule(self, browser, targetdate, starttime, endtime):

        """
        extract the HTML weekly schedule
        date, starttime, endtime, where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format
        """
        # stage 1: get the page of weekly schedule
        weekly_schedule_url = self.sitelinks['weekSch']
        browser.get(weekly_schedule_url)

        self.printdebug('stage 1 ends')

        # stage 2: select the right week and time range
        date = browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
        date.clear()
        date.send_keys(targetdate)
        start_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')
        start_time.clear()
        start_time.send_keys(starttime)
        end_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
        end_time.clear()
        end_time.send_keys(endtime)
        refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL$8$')
        refresh.click()

        self.printdebug('stage 2 ends')

        # stage 3: scrape data
        # browser.wait(5, 'invisibility_of_element_located', 'ID', 'WAIT_win0')
        browser.wait(5)
        soup = bs(browser.page_source, features='lxml')
        timetable = soup.find('table', id='WEEKLY_SCHED_HTMLAREA')

        self.printdebug('stage 3 ends')

        # stage 4: post processing
        timetable['class'] = 'table'
        timeLabels = timetable.find_all('span', {'class': 'SSSTEXTWEEKLYTIME'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'font-weight-bold'
        timeLabels = timetable.find_all('span', {'class': 'SSSTEXTWEEKLY'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'table-warning'

        self.printdebug('stage 4 ends')

        result = timetable.prettify()
        return result

    @cached('transcript')
    def findTranscript(self, browser):
        result = {}
        transcriptlink = self.sitelinks['transcript']
        browser.get(transcriptlink)

        frame = bs(browser.page_source, features='lxml')
        soup2 = frame.find(id='ACE_width')
        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
        for table in tables:
            result[table['id'].split('$')[0]] = webutil.util_soup2List(table)
        return result

    @cached('invoice')
    def findInvoice(self, browser):
        return self.scrapeTable(browser, self.sitelinks['invoice'])

    @cached('receipt')
    def findReceipt(self, browser):
        return self.scrapeTable(browser, self.sitelinks['receipt'])

    @cached('activity')
    def findAccountActivity(self, browser):
        return self.scrapeTable(browser, self.sitelinks['activity'])

    def scrapeTable(self, browser, url):
        result = {}
        self.printdebug(url)
        browser.get(url)
        frame = bs(browser.page_source, features='lxml')
        soup = frame.find(id='ACE_width')
        tables = soup.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
        self.printdebug(len(tables))
        for table in tables:
            if table.find('table', {'class': 'PSLEVEL1GRID'}):
                result[table['id'].split('$')[0]] = webutil.util_soup2List(
                    table.find('table', {'class': 'PSLEVEL1GRID'}))
        return result

    @cached('weekSch')
    def findWeeklySch(self, browser, targetdate, starttime, endtime):

        """
        extract the HTML weekly schedule
        date, starttime, endtime, where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format
        """
        # stage 1: get the page of weekly schedule
        weekly_schedule_url = self.sitelinks['weekSch']
        browser.get(weekly_schedule_url)

        self.printdebug('stage 1 ends')

        # stage 2: select the right week and time range
        date = browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
        date.clear()
        date.send_keys(targetdate)
        start_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')
        start_time.clear()
        start_time.send_keys(starttime)
        end_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
        end_time.clear()
        end_time.send_keys(endtime)
        refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL$8$')
        refresh.click()

        self.printdebug('stage 2 ends')

        # stage 3: scrape data
        # browser.wait(5, 'invisibility_of_element_located', 'ID', 'WAIT_win0')
        browser.wait(5)
        soup = bs(browser.page_source, features='lxml')
        timetable = soup.find('table', id='WEEKLY_SCHED_HTMLAREA')

        self.printdebug('stage 3 ends')

        # stage 4: extract data
        result = []
        trs = timetable.find_all('tr')
        for i in range(len(trs)):
            if i == 0:
                ths = trs[i].find_all('th')
            else:
                tds = trs[i].find_all('td')
                for j in range(len(tds)):
                    time_slot = tds[j].find('span', {'style': 'color:rgb(0,0,0);background-color:rgb(182,209,146);'})
                    if time_slot:
                        data_pack_1 = time_slot.decode_contents().split('<br/>')
                        data_pack_2 = ths[j + 1].decode_contents().replace('\n', '').split('<br/>')
                        result.append({
                            'course': data_pack_1[0],
                            'date': data_pack_2[1],
                            'dow': data_pack_2[0],
                            'time': data_pack_1[2],
                            'location': data_pack_1[3]
                        })

        self.printdebug('stage 4 ends')

        return result

    def findTable(self, browser, option=[]):
        table_id = {
            'TOTAL_DUE': 'Invoice',
            'CHRGS_DUE': 'Invoice',
            'SSF_SS_BIHDR_VW': 'Invoice',
            'Z_BILLPAYH2_TBL': 'Invoice',
            'CRSE_HIST': 'Transcript',
            'GRID_GPA': 'Transcript',
            'ACCT_ACTIVITY': 'Activity',
            'POST_PAY': 'Receipt',
        }
        if type(option) is str:
            # print('a string')
            if option == 'Invoice':
                return self.findInvoice(browser)
            elif option == 'Transcript':
                return self.findTranscript(browser)
            elif option == 'Activity':
                return self.findAccountActivity(browser)
            elif option == 'Receipt':
                return self.findReceipt(browser)
            else:
                return
        elif type(option) is list:
            # print('a list')
            result = {}
            types = set([table_id[each] for each in option if each in table_id])
            for each in types:
                if each == 'Invoice':
                    temp = self.findInvoice(browser)
                    for key in temp:
                        if key in option:
                            result[key] = temp[key]
                elif each == 'Transcript':
                    temp = self.findTranscript(browser)
                    for key in temp.keys():
                        if key in option:
                            result[key] = temp[key]
                elif each == 'Activity':
                    temp = self.findAccountActivity(browser)
                    for key in temp:
                        if key in option:
                            result[key] = temp[key]
                elif option == 'Receipt':
                    temp = self.findReceipt(browser)
                    for key in temp:
                        if key in option:
                            result[key] = temp[key]
            return result

