from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as BY

import time

import website
import weberror

class Moodle(website.Website):

    """
    Base Class Function
    """
    
    def __init__(self, credential, webscrape_settings):
        self.credential = credential
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
            'resource'              : 'https://moodle.hku.hk/mod/resource/view.php?id=',
            'submit_file_upload'    : 'https://moodle.hku.hk/mod/assign/view.php?id=',
            'submit_turnitin'       : 'https://moodle.hku.hk/mod/turnitintooltwo/view.php?id=',
            'url'                   : 'https://moodle.hku.hk/mod/url/view.php?id=',            
            'forum'                 : 'https://moodle.hku.hk/mod/forum/view.php?id=',            
            'quiz'                  : 'https://moodle.hku.hk/mod/quiz/view.php?id=',
            'questionnaire'         : 'https://moodle.hku.hk/mod/questionnaire/view.php?id=',
            'folder'                : 'https://moodle.hku.hk/mod/folder/view.php?id=',
            'page'                  : 'https://moodle.hku.hk/mod/page/view.php?id=',
            'choice'                : 'https://moodle.hku.hk/mod/choice/view.php?id=',
            'feedback'              : 'https://moodle.hku.hk/mod/feedback/view.php?id=',

            

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
        return 'This is a Moodle Instance'

    def login(self):
        self.browser.get(self.sitelinks['login'])
        self.browser.find_element_by_id('login-nav-btn').click()
        time.sleep(1)
        if self.browser.current_url == self.sitelinks['home'] or self.browser.current_url == self.sitelinks['home']+'/':
            return
        else:
            if self.browser.current_url == self.sitelinks['login_sublink_2']:
                self.browser.get(self.sitelinks['login_sublink_1'])
                self.util_universal_hku_login(self.browser, self.credential)
            elif self.browser.current_url == self.sitelinks['login_sublink_1']:
                self.util_universal_hku_login(self.browser, self.credential)
            else:    
                print(self.browser.current_url)

    def logout(self):
        time.sleep(1)
        exit_link = ''
        r = self.browser.request('GET', self.sitelinks['home'])
        soap = bs(r.text, features='lxml')
        menu = soap.find('ul',{'id':'action-menu-0-menu'})    
        elem_as = menu.find_all('a')
        links = [elem_a['href'] for elem_a in elem_as]    
        for link in links:        
            if self.sitelinks['logout'] in link:
                exit_link = link
        self.browser.get(exit_link)
        return    
    
    def getSiteMap(self):        
        r = self.browser.request('GET', self.sitelinks['home'])
        soup = bs(r.text, features = 'lxml')
        course_tab = soup.find_all('div', {'class': 'block_course_list block list_block'})[0]
        course_tab = course_tab.find('ul',{'class': 'unlist'})
        elem_as = course_tab.find_all('a')
        links = [(elem_a.decode_contents().split('/>')[1], elem_a['href']) for elem_a in elem_as]        
        return links

    def getSiteMap2(self):        
        r = self.browser.request('GET', self.sitelinks['home'])
        soup = bs(r.text, features = 'lxml')
        course_tab = soup.find_all('div', {'class': 'block_course_list block list_block'})[0]
        course_tab = course_tab.find('ul',{'class': 'unlist'})
        elem_as = course_tab.find_all('a')
        links = [[elem_a.decode_contents().split('/>')[1], 'course', elem_a['href']] for elem_a in elem_as]        
        return links

    def keepAlive(self):
        self.browser.get(self.sitelinks['home'])        
    
    """
    Extra Function
    """

    def course_page_files(self, course_code):
        for name, link in self.sitemap:
            if course_code in name:
                self.browser.get(link)
                r = self.browser.request('GET', link)
                soup = bs(r.text, features='lxml')
                main = soup.find('section', {'id': 'region-main'})
                elem_as = main.find_all('a')

                files = []
                for elem_a in elem_as:
                    if self.sitelinks['resource'] in elem_a['href']:
                        # filename = elem_a.find('span', {'class': 'instancename'}).decode_contents().split('<span')[0]
                        filename = elem_a.find('span', {'class': 'instancename'}).get_text()
                        link = elem_a['href']
                        files.append((filename, link))
                return files
            
        # print('cannot find the course')
        raise weberror.ScrapeError(1)        

    def getAssignmentPath(self, course_code):
        course_url = ''        
        assignment_list = []
        for name, link in self.sitemap:
            if course_code in name:
                course_url = link                
        if course_url != '':
            # self.browser.get(course_url)
            r = self.browser.request('GET', course_url)
            soap = bs(r.text, features='lxml')            
            for elem_a in soap.find_all('a'):
                if self.sitelinks['submit_file_upload'] in elem_a['href'] or self.sitelinks['submit_turnitin'] in elem_a['href']:
                    name = elem_a.get_text()
                    assignment_list.append((name, elem_a['href']))
            return assignment_list
        else:            
            raise weberror.ScrapeError(1)

    def getGrades(self, course_code):
        for each in self.sitemap:
            if course_code in each[0]:                
                url = self.sitelinks['grade'] + each[1][each[1].find('?id=') + len('?id='):]                
                r = self.browser.request('GET', url)                
                soup = bs(r.text, features='lxml')
                return soup.find('table').prettify()
        # return 'cannot found course'
        raise weberror.ScrapeError(1)

    def findCourseLink(self, course_code):
        possible_links = []
        for name, link in self.sitemap:
            if course_code in name:
                possible_links.append(link)                
        return possible_links

    def parseCourseHTML(self, url):
        r = self.browser.request('GET', url)
        soup = bs(r.text, features = 'lxml')
        section = soup.find('section', {'id': 'region-main'})
        if not section: raise weberror.ScrapeError(0)
        links = section.find_all('a')
        if not section: raise weberror.ScrapeError(0)
        files = []
        for each in links:            
            filename = ''
            row = []
            elem = each.find('span', {'class': 'instancename'})            
            elem2 = each.find('span', {'class': 'fp-filename'})
            if elem: filename = elem.decode_contents().split('<span')[0]
            if elem2: filename = elem2.decode_contents()
            link = each['href']
            for key,value in self.sitelinks.items():
                if value in link:
                    row = [filename, key, link]
            if len(row) > 0: files.append(row) # filter empty row
        return files
    
    def minimizeStorageInt(self, list_of_links):
        cache_links = []
        resource_id = ''
        for each in list_of_links:
            if '#' not in each[1] and each[1] != 'help' and each[1] != 'force_download':
                resource_id = int(each[2][len(self.sitelinks[each[1]]):])
                cache_links.append([each[0],each[1],resource_id])
        return cache_links
    def minimizeStorageStr(self, list_of_links):
        cache_links = []   
        post_link = ''
        for each in list_of_links:
            if each[1] == 'force_download':
                post_link = each[2][len(self.sitelinks[each[1]]):]
                cache_links.append([each[0],each[1],post_link])
        return cache_links

    def getLink(self, row):
        return self.sitelinks[row[1]] + str(row[2])


    """
    Abandoned Function
    """

    def downloadFile(self, url):
        self.browser.get(url)    

    # def submit_file(self, url, file_path):
    #     if 'assign' in url:
    #         self.assign_submit_file(url, file_path)
    #     elif 'turnitintooltwo' in url:
    #         self.turnitin_submit_file(url, file_path)
    #     else:
    #         print('unknwon submit file method')
    #         return
    
    # def assign_submit_file(self, url, file_pathes):
    #     if self.debug:
    #         print("""
    #         -------Welcome to function assign_submit_file-------
    #         This is an exciting funciton that makes many confused.  
    #         Highly dynamic javascript and wait runs here.  
    #         The ride is here now.  Catch anything that can save you.  
    #         ----------------
    #         """)

    #     self.browser.get(url)

    #     """
    #     Step 1: open the Submission Box by clicking 'edit submission'
    #     """
    #     # self.browser.find_element_by_xpath("//input[@type='submit']").click()

    #     wait = WebDriverWait(self.browser, 2)
    #     wait.until(EC.element_to_be_clickable((BY.XPATH, "//input[@type='submit']"))).click()

    #     if self.debug:
    #         print("""
    #         -------Step 1 Finish-------
    #         Get out of the boat and land on the box.  
    #         You should be in the submission box now.    
    #         ----------------
    #         """)
        
    #     """
    #     Step 2: locate the file submission box
    #     """

    #     time.sleep(2)
    #     filemanager = self.browser.find_element_by_id('fitem_id_files_filemanager')
    #     while not filemanager:
    #         time.sleep(2)
    #         filemanager = self.browser.find_element_by_id('fitem_id_files_filemanager')        
    #     # wait = WebDriverWait(self.browser, 2)
    #     # filemanager = wait.until(EC.visibility_of_element_located((BY.ID, 'fitem_id_files_filemanager')))

    #     if self.debug:
    #         print("""
    #         -------Step 2 Finish-------
    #         Welcome to the file manager.  
    #         You got it.  
    #         Sometimes you go to the wrong place and cannot find it.      
    #         Just like the train station 10 1/2 in the King Station in Harry Potter.  
    #         ----------------
    #         """)

    #     """
    #     Step 3: If there is existing file in the file manager, delete them all.  
    #     """
    #     soup1 = bs(filemanager.get_attribute('innerHTML'), features='lxml')
    #     context_menus = soup1.find_all('div',{'class': 'fp-file fp-hascontextmenu'})
    #     print('checking existing files in file manager')
    #     if len(context_menus) > 0:
    #         print('removing existing files in file manager')
    #         for each in context_menus:
    #             # print(each.prettify())
    #             print(each['id'])

    #             if self.debug:
    #                 if not self.browser.find_element_by_id(each['id']):
    #                     print('cannot find files with class fp-file fp-hascontextmenu even it / they exist(s)')
    #                     return

    #             self.browser.find_element_by_id(each['id']).click()
    #             button_1 = self.util_getELEMfromProperties(self.browser, 'button', {'class': 'fp-file-delete', 'innerHTML': 'Delete'})

    #             if self.debug:
    #                 if not button_1:                       
    #                     print('cannot find button 1')
    #                     return

    #             button_1.click()

    #             button_2 = self.util_getELEMfromProperties(self.browser, 'button', {'class': 'fp-dlg-butconfirm btn-primary btn', 'innerHTML': 'OK'})

    #             if self.debug:
    #                 if not button_2:                       
    #                     print('cannot find button 2')
    #                     return

    #             button_2.click()

    #     if self.debug:
    #         print("""
    #         -------Step 3 Finish-------
    #         This is Hogwarts.  Where you learn Magic about computers.  
    #         This is the place where you can see no files left in the file manager.  
    #         However, it is not easy to submit file.  
    #         You need to click the 'Add File' button and then fill in the form, but many fails at finding the button.  
    #         Add oil! This is one of the famous 'quiz' in Hogwarts! 
    #         ----------------
    #         """)
    #     """
    #     Step 4: Submit file by clicking the button 'add file' and fill in the form
    #     """
    #     print('submiting files to file manager')
    #     if len(file_pathes)>0:
    #         for file_path in file_pathes:
    #             button_3 = self.util_getELEMfromProperties(self.browser, 'a', {'title': 'Add...', 'role': 'button'})

    #             if self.debug:
    #                 if not button_3:
    #                     print('cannot find button 3')
    #                     return

    #             button_3.click()

    #             if self.debug:
    #                 if not self.browser.find_element_by_xpath("//input[@name='repo_upload_file']"):
    #                     print('cannot find the input type = file')
    #                     return

    #             self.browser.find_element_by_xpath("//input[@name='repo_upload_file']").send_keys(file_path)
    #             button_4 = self.util_getELEMfromProperties(self.browser, 'button', {'class': 'fp-upload-btn btn-primary btn', 'innerHTML': 'Upload this file'})

    #             if self.debug:
    #                 if not button_4:
    #                     print('cannot find button 4')
    #                     return

    #             button_4.click()

    #             if self.debug:
    #                 if not self.browser.find_element_by_id('id_submitbutton'):
    #                     print('cannot find button with id=id_submitbutton')
    #                     return

    #             self.browser.find_element_by_id('id_submitbutton').click()            
            
    #         if self.debug:
    #             print("""
    #             -------Step 4 Finish-------
    #             Congrats! You finish the quiz! 
    #             Now you can get of here and take some rest now.  
    #             ----------------
    #             """)
    #             print('----------------END OF FUNCTION assign_submit_file----------------')
            
    #     else:
    #         if self.debug:
    #             print('no file path')
    #         return

    # def turnitin_submit_file(self, url, file_path):
    #     self.browser.get(url)
    #     links = self.browser.find_elements_by_tag_name('a')
    #     # print(len(links))
    #     for each in links:
    #     #     if 'https://moodle.hku.hk/mod/turnitintooltwo/view.php?id=' in each.get_attribute('href') and 'do=submitpaper&view_context=box_solid' in each.get_attribute('href'):
    #     #         print(each.get_attribute('innerHTML'))

    #         if 'upload_' in each.get_attribute('id'):
    #             print(each.get_attribute('innerHTML'))    

    
        