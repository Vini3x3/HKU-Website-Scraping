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
def get_website(website, username, password, **kwargs):
    websites = ['Portal', 'Moodle']
    if website not in websites:
        raise weberror.CallError(4)
    else:
        klass = globals()[website]
        return klass(username, password, **kwargs)


# Decorator for switching tab
def switch_tab(func, *args):
    def wrapper(self, browser, *args):
        browser.tab(self.site_name)
        return func(self, browser, *args)
    return wrapper


# Decorator for caching
def cached(key):
    def decorator(function):
        @switch_tab
        def wrapper(self, browser, *args):
            url = self.site_links[key]
            browser.get(url)
            if url in self.html_cache.keys():
                if self.html_cache[url] == len(browser.page_source):
                    return self.func_cache[self.hash_func(function.__name__, url, *args)]
            self.html_cache[url] = len(browser.page_source)
            result = function(self, browser, *args)
            self.func_cache[self.hash_func(function.__name__, url, *args)] = result
            return result
        return wrapper
    return decorator


class Website:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """

    def __init__(self, username, password, cachesize=128, verbose=0):
        # setting
        self.sitemap = []
        self.site_links = {}
        self.site_name = ''
        self.func_cache = cachetools.LRUCache(cachesize)
        self.html_cache = {}
        self.hash_func = cachetools.keys.hashkey

        # copy argument
        self.username = username
        self.password = password
        self.debug = verbose > 0

    def __str__(self):
        return 'This is a Website instance'

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def print_debug(self, msg):
        if self.debug:
            print(
                '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg)
            )

    def get_sitemap(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    @switch_tab
    def refresh(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['home'])
        self.print_debug('end')

    @switch_tab
    def destroy(self, browser):
        self.print_debug('start')
        self.logout(browser)
        browser.untab(self.site_name)
        self.print_debug('end')

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
        self.site_links = {
            'home': 'https://moodle.hku.hk',
            'login': 'http://moodle.hku.hk/login',
            'login_sublink_1': 'https://moodle.hku.hk/login/index.php?authCAS=CAS',
            'login_sublink_2': 'https://moodle.hku.hk/login/index.php',
            'logout': 'https://moodle.hku.hk/login/logout.php?sesskey=',
            'deadlines': 'https://moodle.hku.hk/my/?myoverviewtab=timeline',
        }
        self.site_name = 'Moodle'

    def __str__(self):
        return 'This is a Moodle Instance'

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def start(self, browser):
        self.print_debug('start')
        browser.tab(self.site_name, self.site_links['login'])
        self.login(browser)
        browser.wait(3, 'presence_of_element_located', 'ID', 'frontpage-course-list')
        self.sitemap = self.get_sitemap(browser)
        self.print_debug('end')

    @switch_tab
    def login(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['login'])
        browser.find_element_by_id('login-nav-btn').click()
        browser.wait(1)
        self.print_debug('branch')
        if browser.current_url == self.site_links['home'] or browser.current_url == self.site_links['home'] + '/':
            self.print_debug('end case 1')
        else:
            if browser.current_url == self.site_links['login_sublink_2']:
                browser.get(self.site_links['login_sublink_1'])
                webutil.util_universal_hku_login(browser, self.username, self.password)
                self.print_debug('end case 2')
            elif browser.current_url == self.site_links['login_sublink_1']:
                webutil.util_universal_hku_login(browser, self.credential)
                self.print_debug('end case 3')
            else:
                self.print_debug('end case error')
                self.print_debug(browser.current_url)

    @switch_tab
    def logout(self, browser):
        self.print_debug('start')
        exit_link = ''
        browser.get(self.site_links['home'])
        response_html = browser.page_source
        soap = bs(response_html, features='lxml')
        menu = soap.find('ul', {'id': 'action-menu-0-menu'})
        elem_as = menu.find_all('a')
        links = [elem_a['href'] for elem_a in elem_as]
        for link in links:
            if self.site_links['logout'] in link:
                exit_link = link
        browser.get(exit_link)
        self.print_debug('end')

    @switch_tab
    def get_sitemap(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['home'])
        soup = bs(browser.page_source, features='lxml')
        link_map = []
        boxes = soup.find_all('div', class_='coursebox')
        self.print_debug('find box')
        for box in boxes:
            course_link_elem = box.find('a')
            link_map.append((course_link_elem.get_text(strip=True), course_link_elem['href']))
        self.print_debug('end')
        return link_map

    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

    @cachetools.cached(
        cache=cachetools.LRUCache(maxsize=128),
        key=lambda self, browser, keywords: cachetools.keys.hashkey(keywords)
    )
    def find_course_by_keywords(self, browser, keywords):
        for row in self.sitemap:
            if keywords.lower() in row[0].lower():
                return row
        raise weberror.CallError(3)

    @cachetools.cached(
        cache=cachetools.LRUCache(maxsize=128),
        key=lambda self, browser, keywords: cachetools.keys.hashkey(keywords)
    )
    def find_all_courses_by_keywords(self, browser, keywords):
        return [row for row in self.sitemap if keywords.lower() in row[0].lower()]

    @switch_tab
    def scrape_course_content(self, browser, url):
        self.site_links['temp'] = url

        @cached('temp')
        def _scrape_course_content(self, browser):
            self.print_debug('begin')
            result = []
            self.print_debug('not cached')
            browser.get(url)
            self.print_debug(browser.current_url)
            soup = bs(browser.page_source, features='lxml')
            region = soup.find('section', id='region-main')
            items = region.find_all('div', class_='activityinstance')
            self.print_debug(len(items))
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
            self.print_debug('end')
            return result

        result = _scrape_course_content(self, browser)
        del self.site_links['temp']
        return result

    @switch_tab
    def scrape_course_preview(self, browser, url):
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
    def scrape_deadlines(self, browser):
        url = self.site_links['deadlines']
        browser.get(url)
        browser.wait(1)
        soup = bs(browser.page_source, features='lxml')
        div = soup.find('div', id='myoverview_timeline_view')
        deadlines = div.findAll('li', class_='event-list-item')
        # print(len(deadlines))
        result = []

        for deadline in deadlines:            
            link = deadline.find('a', class_='event-name')
            deadline_name = link.get_text(strip=True)            
            self.print_debug(deadline_name)
            deadline_link = link['href']
            self.print_debug(deadline_link)
            deadline_time = deadline.find('div', class_='span5').get_text(strip=True)
            self.print_debug(deadline_time)
            result.append({
                'name': link.get_text(),
                'link': link['href'],
                'time': deadline.find('div', class_='span5 text-truncate').get_text(strip=True),
            })
        return result


class Portal(Website):
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """

    def __init__(self, credential, webscrape_settings=None):
        # storage
        super().__init__(credential, webscrape_settings)
        self.site_links = {
            'login': 'https://hkuportal.hku.hk/login.html',
            'home': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
            'logout': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/?cmd=logout',

            'weekSch': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W.GBL',
            'transcript': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/Z_SS_MENU.Z_TSRPT_WEB_STDT.GBL',
            'invoice': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_CHRGS_DUE.GBL',
            'receipt': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_PMT_HIST.GBL',
            'activity': 'https://sis-main.hku.hk/psc/sisprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSF_SS_ACCT_ACTVTY.GBL',
        }
        self.site_name = 'Portal'

    def __str__(self):
        return 'This is a Portal Instance'

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def start(self, browser):
        self.print_debug('start')
        browser.tab(self.site_name, self.site_links['login'])
        self.login(browser)
        # browser.wait(2, 'presence_of_element_located', 'ID', 'ADMN_Z_HKU_STUDENTNOTICE_HMPG')
        self.sitemap = self.get_sitemap(browser)
        self.print_debug('end')

    def login(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['login'])
        webutil.util_universal_hku_login(browser, self.username, self.password)
        self.print_debug('end')

    def logout(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['logout'])
        self.print_debug('end')

    @switch_tab
    def get_sitemap(self, browser):
        self.print_debug('start')
        browser.get(self.site_links['home'])
        soup = bs(browser.page_source, features='lxml')
        link_map = []
        boxes = soup.find_all('div', class_='coursebox')
        self.print_debug('find box')
        for box in boxes:
            course_link = box.find('a')
            link_map.append((course_link.get_text(strip=True), course_link['href']))
        self.print_debug('end')
        return link_map

    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """

    @cached('weekSch')
    def display_weekly_schedule(self, browser, target_date, start_time, end_time):

        """
        extract the HTML weekly schedule
        date, start_time, end_time, where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format
        """
        # stage 1: get the page of weekly schedule
        weekly_schedule_url = self.site_links['weekSch']
        browser.get(weekly_schedule_url)

        self.print_debug('stage 1 ends')

        # stage 2: select the right week and time range
        date = browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
        date.clear()
        date.send_keys(target_date)
        input_start_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')
        input_start_time.clear()
        input_start_time.send_keys(start_time)
        input_end_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
        input_end_time.clear()
        input_end_time.send_keys(end_time)
        refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL$8$')
        refresh.click()

        self.print_debug('stage 2 ends')

        # stage 3: scrape data
        browser.wait(5, 'invisibility_of_element_located', 'ID', 'WAIT_win0')
        browser.wait(1)
        soup = bs(browser.page_source, features='lxml')
        timetable = soup.find('table', id='WEEKLY_SCHED_HTMLAREA')

        self.print_debug('stage 3 ends')

        # stage 4: post processing
        timetable['class'] = 'table'
        time_labels = timetable.find_all('span', {'class': 'SSSTEXTWEEKLYTIME'})
        for time_label in time_labels:
            time_label.parent['class'] = 'font-weight-bold'
        time_labels = timetable.find_all('span', {'class': 'SSSTEXTWEEKLY'})
        for time_label in time_labels:
            time_label.parent['class'] = 'table-warning'

        self.print_debug('stage 4 ends')

        result = timetable.prettify()
        return result

    @cached('transcript')
    def find_transcript(self, browser):
        result = {}
        transcript_link = self.site_links['transcript']
        browser.get(transcript_link)

        frame = bs(browser.page_source, features='lxml')
        soup2 = frame.find(id='ACE_width')
        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
        for table in tables:
            result[table['id'].split('$')[0]] = webutil.util_soup2List(table)
        return result

    @cached('invoice')
    def find_invoice(self, browser):
        return self.scrape_table(browser, self.site_links['invoice'])

    @cached('receipt')
    def find_receipt(self, browser):
        return self.scrape_table(browser, self.site_links['receipt'])

    @cached('activity')
    def find_account_activity(self, browser):
        return self.scrape_table(browser, self.site_links['activity'])

    def scrape_table(self, browser, url):
        result = {}
        self.print_debug(url)
        browser.get(url)
        frame = bs(browser.page_source, features='lxml')
        soup = frame.find(id='ACE_width')
        tables = soup.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
        self.print_debug(len(tables))
        for table in tables:
            if table.find('table', {'class': 'PSLEVEL1GRID'}):
                result[table['id'].split('$')[0]] = webutil.util_soup2List(
                    table.find('table', {'class': 'PSLEVEL1GRID'}))
        return result

    @cached('weekSch')
    def find_weekly_sch(self, browser, target_date, start_time, end_time):

        """
        extract the HTML weekly schedule
        date, start_time, end_time, where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format
        """
        # stage 1: get the page of weekly schedule
        weekly_schedule_url = self.site_links['weekSch']
        browser.get(weekly_schedule_url)

        self.print_debug('stage 1 ends')

        # stage 2: select the right week and time range
        date = browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
        date.clear()
        date.send_keys(target_date)
        input_start_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')
        input_start_time.clear()
        input_start_time.send_keys(start_time)
        input_end_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
        input_end_time.clear()
        input_end_time.send_keys(end_time)
        refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL$8$')
        refresh.click()

        self.print_debug('stage 2 ends')

        # stage 3: scrape data
        browser.wait(5, 'invisibility_of_element_located', 'ID', 'WAIT_win0')
        browser.wait(1)
        soup = bs(browser.page_source, features='lxml')
        timetable = soup.find('table', id='WEEKLY_SCHED_HTMLAREA')

        self.print_debug('stage 3 ends')

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
        return result
