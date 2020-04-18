from myscraper.HKUSites import *
from myutil import webutil
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import cachetools
import inspect

class Moodle(BasicMoodle):
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """
    def __init__(self, credential, webscrape_settings=None):
        super().__init__(credential, webscrape_settings)        
        self.cachesize = 128
        if 'cachesize' in webscrape_settings:
            self.cachesize = webscrape_settings['cachesize']
        self.mycache = cachetools.LRUCache(self.cachesize)
        self.hashfunc = cachetools.keys.hashkey
        self.htmlcache = {}

        self.contenttype = {
            '/help.php'                  : 'help',
            '/pluginfile.php'        : 'force_download',

            '/grade/report/index.php'                 : 'grade',
            '/course/view.php'                : 'course',
            '/user/index.php'               : 'contact',
            '/user/view.php'                  : 'user',
            '/mod/resource/view.php'              : 'resource',
            '/mod/assign/view.php'    : 'submit_file_upload',
            '/mod/turnitintooltwo/view.php'       : 'submit_turnitin',
            '/mod/url/view.php'                   : 'url',
            '/mod/page/view.php'                  : 'page',
            '/mod/forum/view.php'                 : 'forum',
            '/mod/forum/discuss.php'            : 'discussion',
            '/mod/quiz/view.php'                  : 'quiz',   
            '/mod/folder/view.php'                : 'folder',
            '/mod/questionnaire/view.php'         : 'questionnaire',
            '/mod/choice/view.php'                : 'choice',     
            '/mod/choicegroup/view.php'           : 'choicegroup',
            '/mod/lti/view.php'                   : 'lti',
            '/mod/feedback/view.php'              : 'feedback',
            '/mod/vpl/view.php'                   : 'vpl',

            '/my/'  : 'submission_deadlines',
        }
    
    def switchTab(func, *args):
        def wrapper(self, browser, *args):
            browser.tab(self.sitename)
            return func(self, browser, *args)
        return wrapper
    
    @switchTab
    def probe(self, browser, url):
        browser.get(url)        
        if url in self.htmlcache.keys():
            if self.htmlcache[url] == len(browser.page_source):
                return True
        self.htmlcache[url] = len(browser.page_source)        
        return False
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """    
    
    def sitemapSearch(self, keywords):
        for row in self.sitemap:
            if keywords in row[0]:
                return row
        raise weberror.CallError(3)
    def sitemapSearchAll(self, keywords):
        return [row for row in self.sitemap if keywords in row[0]]
    @switchTab
    def scrapeGrades(self, browser, row):        
        url = self.sitelinks['grade'] + str(71754) #str(row[2])
        print(url)
        # breakpoints
        if self.probe(browser, url):
            # print('cached')
            return self.mycache[self.hashfunc(inspect.stack()[0][3]), frozenset(set(row))]
        # breakpoints        
        if self.debug: print(url)
        browser.get(url)
        soup = bs(browser.page_source, features='lxml')
        result = soup.find('table')
        # breakpoints
        self.mycache[self.hashfunc(inspect.stack()[0][3]), frozenset(set(row))] = result
        # breakpoints
        return result
    
    @cachetools.cached(cache=cachetools.LRUCache(maxsize=128))
    def extractGrade(self, soup):        
        table = webutil.util_HTMLtable2List(soup)        
        return table

    @switchTab
    def scrapeAssignment(self, browser, url):
        # breakpoint
        if self.probe(browser, url):
            print('cached')
            return self.mycache[self.hashfunc(inspect.stack()[0][3], url)]
        # breakpoint
        browser.get(url)
        soup = bs(browser.page_source, features='lxml')
        result = {}   
        section = soup.find('section', {'id':'region-main'})
        try:
            result['summary'] = section.find('div',{'class':'box boxaligncenter submissionsummarytable'}).find('table')
        except:
            pass
        try:
            result['feedback'] = section.find('div',{'class':'box boxaligncenter feedbacktable'}).find('table')
        except:
            pass
        # result['submit'] = section.find('div',{'class':'box generalbox submissionaction'}).prettify()
        # breakpoint
        self.mycache[self.hashfunc(inspect.stack()[0][3], url)] = result
        # breakpoint
        return result

    @cachetools.cached(cache=cachetools.LRUCache(maxsize=128))
    def extractAssignment(self, soup_dict):
        result_dict = {}        
        if 'summary' in soup_dict:            
            table = webutil.util_HTMLtable2List(soup_dict['summary'])
            # table = table[:6]
            result_dict['summary'] = table
        if 'feedback' in soup_dict.keys():            
            table = webutil.util_HTMLtable2List(soup_dict['feedback'])            
            result_dict['feedback'] = table        
        return result_dict
        
    @switchTab
    def parseCourseHTML(self, browser, url):
        # breakpoint
        if self.probe(browser, url):
            print('cached')
            return self.mycache[self.hashfunc(inspect.stack()[0][3], url)]
        # breakpoint
        browser.get(url)
        soup = bs(browser.page_source, features = 'lxml')
        section = soup.find('ul', {'class': 'topics'})
        if not section: raise weberror.ScrapeError(0)
        links = section.find_all('a')    
        content = []
        for each in links:
            filename = ''            
            elem = each.find('span', {'class': 'instancename'})
            elem2 = each.find('span', {'class': 'fp-filename'})
            if elem: filename = elem.decode_contents().split('<span')[0]
            elif elem2: filename = elem2.decode_contents()
            else: filename = each.get_text()
            if each.has_attr('href'):
                link = each['href']
                content.append([filename, urlparse(link)])                
        #breakpoint
        self.mycache[self.hashfunc(inspect.stack()[0][3], url)] = content        
        #breakpoint
        return content


class Portal(BasicPortal):    
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """
    def __init__(self, credential, webscrape_settings=None):
        super().__init__(credential, webscrape_settings)        
        self.cachesize = 128
        if 'cachesize' in webscrape_settings:
            self.cachesize = webscrape_settings['cachesize']
        self.mycache = cachetools.LRUCache(self.cachesize)
        self.hashfunc = cachetools.keys.hashkey
        self.htmlcache = {}
    
    def switchTab(func, *args):
        def wrapper(self, browser, *args):
            browser.tab(self.sitename)
            return func(self, browser, *args)
        return wrapper
    
    @switchTab
    def probe(self, browser, url):
        browser.get(url)        
        if url in self.htmlcache.keys():
            if self.htmlcache[url] == len(browser.page_source):
                return True
        self.htmlcache[url] = len(browser.page_source)
        return False

    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """
    @switchTab
    def findTranscript(self, browser):
        result = {}
        transcriptlink = ''
        for link in self.sitemap:
            if self.sitelinks['grades'] in link:
                transcriptlink = link
        self.printdebug(transcriptlink)
        # breakpoints
        if self.probe(browser, transcriptlink):
            return self.mycache[self.hashfunc(inspect.stack()[0][3])]
        # breakpoints
        browser.get(transcriptlink)
        self.printdebug('stage 1 end')

        framelink = ''
        soup = bs(browser.page_source, features='lxml')        
        for frame in soup.find_all('frame'):
            if frame['name']=='TargetContent' and frame['title']=='Main Content':
                framelink = frame['src']
        self.printdebug(framelink)
        browser.get(framelink)        
        self.printdebug('stage 2 end')
                
        frame = bs(browser.page_source, features = 'lxml')        
        soup2 = frame.find(id='ACE_width')
        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})
        result['Course History'] = webutil.util_soup2List(tables[0])
        result['GPA'] = webutil.util_soup2List(tables[1])
        self.printdebug('stage 3 end')
        #breakpoint
        self.mycache[self.hashfunc(inspect.stack()[0][3])] = result
        #breakpoint
        return result
    
    @switchTab
    def findWeeklySchedule(self, browser, targetdate, starttime, endtime):
        """
        extract the HTML weekly schedule
        date, starttime, endtime, where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format    
        """
        # stage 1: get the frame of weekly schedule    
        weekly_schedule_url = ''
        for link in self.sitemap:
            if self.sitelinks['weekSch'] in link:
                weekly_schedule_url = link                    
        self.printdebug(weekly_schedule_url)
        # breakpoint
        if self.probe(browser, weekly_schedule_url):
            return self.mycache[self.hashfunc(inspect.stack()[0][3], targetdate, starttime, endtime)]
        # breakpoint
        browser.get(weekly_schedule_url)
        soap = bs(browser.page_source, features='lxml')        
        frames = soap.find_all('frame')        
        for each in frames:
            if each['name'] == 'TargetContent':
                weekly_schedule_url = each['src']        
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
        refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL')
        refresh.click()
        
        self.printdebug('stage 2 ends')

        # stage 3: extract the data    
        soup = bs(browser.page_source, features='lxml')
        table = soup.find('table', {"id": "WEEKLY_SCHED_HTMLAREA"})
                
        self.printdebug('stage 3 ends')
        
        # stage 4: post processing
        table['class'] = 'table'
        timeLabels = table.find_all('span', {'class': 'SSSTEXTWEEKLYTIME'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'font-weight-bold'
        timeLabels = table.find_all('span', {'class': 'SSSTEXTWEEKLY'})
        for timeLabel in timeLabels:
            timeLabel.parent['class'] = 'table-warning'

        self.printdebug('stage 4 ends')

        result = table
        # breakpoint
        self.mycache[self.hashfunc(inspect.stack()[0][3], targetdate, starttime, endtime)] = result
        # breakpoint
        return result
    
    @switchTab
    def findInvoice(self, browser):
        result = {}

        # stage 1
        invoicelink = ''
        for link in self.sitemap:
            if self.sitelinks['invoice'] in link:
                invoicelink = link
        self.printdebug(invoicelink)
        # breakpoints
        if self.probe(browser, invoicelink):
            return self.mycache[self.hashfunc(inspect.stack()[0][3])]
        # breakpoints
        browser.get(invoicelink)
        self.printdebug('stage 1 end')

        # stage 2
        framelink = ''
        soup = bs(browser.page_source, features='lxml')
        for frame in soup.find_all('frame'):
            if frame['name']=='TargetContent' and frame['title']=='Main Content':
                framelink = frame['src']
        self.printdebug(framelink)
        browser.get(framelink)
        self.printdebug('stage 2 end')

        # stage 3        
        frame = bs(browser.page_source, features = 'lxml')
        soup2 = frame.find(id='ACE_width')
        tables = soup2.find_all('table', {'class': 'PSLEVEL1GRIDWBO'})                        
        if self.debug: print(len(tables))
        for table in tables:
            if table.find('table',{'class':'PSLEVEL1GRID'}):
                result[table['id'].split('$')[0]] = webutil.util_soup2List(table.find('table',{'class':'PSLEVEL1GRID'}))
        #breakpoint        
        self.mycache[self.hashfunc(inspect.stack()[0][3])] = result
        #breakpoint
        return result
    
    @cachetools.cached(cache=cachetools.LRUCache(maxsize=128))
    def test(self, browser, a,b):
        print(a+b)
        return a+b
    
