# testground5

import selenium
import requests
from bs4 import BeautifulSoup as bs
import requests_html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import traceback

# from selenium.webdriver.firefox.options import Options

# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib as plt

import time

def makeBrowser(webscrape_settings):
    """
    return a driver object, call 'driver'
    """
    # return selenium.webdriver.Firefox(executable_path=webscrape_settings['driver'])
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('-headless')
    return selenium.webdriver.Firefox(executable_path=webscrape_settings['driver'], options=options)

def universal_hku_login(browser, crediential, webscrape_settings):
    username = browser.find_element_by_id('username')
    username.send_keys(creditential['username'])
    password = browser.find_element_by_id('password')
    password.send_keys(creditential['password'])
    password.submit()
    time.sleep(1)    

def signin(browser, creditential, webscrape_settings):
    """
    input a browser object and sign in
    """
    browser.get(webscrape_settings['homepage'])
    universal_hku_login(browser, creditential, webscrape_settings)
    

def exit(browser, webscrape_settings):
    """
    exit by inputing a browser object
    """
    browser.get(webscrape_settings['exitpage'])
    signout = browser.find_element_by_link_text('Sign out')
    signout.click()
    browser.quit()

def getPortalLinks(browser, webscrape_settings):
    result = []
    browser.get(webscrape_settings['exitpage'])
    soap = bs(browser.page_source, features='lxml')
    for link in soap.find_all("a"):
        if link['href'][0:4] == 'http':
            result.append(link['href'])
    return result

def findWeeklySchedule(browser, webscrape_settings, portal_links, argv):
    """
    extract the HTML weekly schedule
    argv = [date, starttime, endtime], where date is in 'dd/mm/yyyy' string format, and time is '8:00AM' format    
    """    
    container = []
    result = []
    # stage 1: get the frame of weekly schedule    
    weekly_schedule_url = ''
    for link in portal_links:
        if webscrape_settings['weekSchpage'] in link:
            weekly_schedule_url = link
    browser.get(weekly_schedule_url)
    soap = bs(browser.page_source, features='lxml')
    frames = soap.find_all('frame')
    # print(len(frames))
    for each in frames:
        if each['name'] == 'TargetContent':
            weekly_schedule_url = each['src']
    browser.get(weekly_schedule_url)
    print('stage 1 ends')

    # stage 2: select the right week and time range
    date = browser.find_element_by_id('DERIVED_CLASS_S_START_DT')
    date.clear()
    date.send_keys(argv[0])
    start_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_START')    
    start_time.clear()
    start_time.send_keys(argv[1])
    end_time = browser.find_element_by_id('DERIVED_CLASS_S_MEETING_TIME_END')
    end_time.clear()
    end_time.send_keys(argv[2])
    refresh = browser.find_element_by_id('DERIVED_CLASS_S_SSR_REFRESH_CAL')
    refresh.click()
    print('stage 2 ends')

    # stage 3: extract the data    
    soup = bs(browser.page_source, features='lxml')    
    table = soup.find('table', {"id": "WEEKLY_SCHED_HTMLAREA"})    
    print(table.prettify())
    # print(len(table.find_all('th')))
    # print(len(table.find_all('td')))
    # for each in table.find_all('td'):
    #     if each.decode_contents().strip() != '':
    #         if not each.find('span').decode_contents().strip()[0].isdigit():
    #             container.append(each.find('span').decode_contents().strip())
    # for each in container:
    #     result.append(each.split('<br/>'))    
    # for each in result:
    #     each.pop(1)
    
    print('stage 3 ends')
    # return result
    # return table.decode_contents()

def moodle_login(browser, webscrape_settings, creditential):
    browser.get(webscrape_settings['moodle_login'])
    browser.find_element_by_id('login-nav-btn').click()
    time.sleep(1)
    if browser.current_url == 'https://moodle.hku.hk/' or browser.current_url == 'https://moodle.hku.hk':
        return
    else:
        if browser.current_url == 'https://moodle.hku.hk/login/index.php':
            browser.get('https://moodle.hku.hk/login/index.php?authCAS=CAS')
            universal_hku_login(browser, creditential, webscrape_settings)
        elif browser.current_url == 'https://moodle.hku.hk/login/index.php?authCAS=CAS':
            universal_hku_login(browser, creditential, webscrape_settings)
        else:    
            print(browser.current_url)            

def moodle_signout(browser, webscrape_settings):
    exit_link = ''
    browser.get(webscrape_settings['moodle_home'])
    soap = bs(browser.page_source, features='lxml')    
    menu = soap.find('ul',{'id':'action-menu-0-menu'})    
    elem_as = menu.find_all('a')
    links = [elem_a['href'] for elem_a in elem_as]    
    for link in links:
        # print(link)
        if 'https://moodle.hku.hk/login/logout.php?sesskey=' in link:
            exit_link = link
    browser.get(exit_link)
    return

def moodle_course_links(browser, webscrape_settings):
    browser.get(webscrape_settings['moodle_home'])
    soup = bs(browser.page_source, features = 'lxml')
    course_tab = soup.find_all('div', {'class': 'block_course_list block list_block'})[0]
    course_tab = course_tab.find('ul',{'class': 'unlist'})
    elem_as = course_tab.find_all('a')
    links = [(elem_a.decode_contents().split('/>')[1], elem_a['href']) for elem_a in elem_as]
    return links

def moodle_course_page_files(borwser, webscrape_settings, links, course_code):    
    for name, link in links:
        if course_code in name:
            borwser.get(link)
            soup = bs(borwser.page_source, features='lxml')
            main = soup.find('section', {'id': 'region-main'})
            elem_as = main.find_all('a')
            # links = [elem_a['href'] for elem_a in elem_as]
            # files = [link for link in links if 'https://moodle.hku.hk/mod/resource/view.php?' in link]

            files = []
            for elem_a in elem_as:
                if 'https://moodle.hku.hk/mod/resource/view.php?' in elem_a['href']:
                    filename = elem_a.find('span', {'class': 'instancename'}).decode_contents().split('<span')[0]
                    link = elem_a['href']
                    files.append((filename, link))                       
            # for file_ in files:
            #     print(file_)
            return files
        
    print('cannot find the course')
    return

webscrape_settings = {
    'homepage': 'https://hkuportal.hku.hk/login.html',
    'exitpage': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
    'weekSchpage': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W',
    'driver': 'C:\\Users\\vince\\AppData\\Local\\Temp\\geckodriver-v0.26.0-win64\\geckodriver.exe',
    'moodle_login': 'http://moodle.hku.hk/login',
    'moodle_home': 'https://moodle.hku.hk'
}

creditential = {
    'username': '',
    'password': '',
}

portal_links = []

# firefoxBrowser = selenium.webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
firefoxBrowser = makeBrowser(webscrape_settings)
print('===made===')
signin(firefoxBrowser, creditential, webscrape_settings)
print('===signin ed===')

"""
start scraping
"""
try:
    portal_links = getPortalLinks(firefoxBrowser, webscrape_settings)
    # table = findWeeklySchedule(firefoxBrowser, webscrape_settings, portal_links, ['25/01/2020','8:00AM','11:00PM'])
    moodle_login(firefoxBrowser, webscrape_settings, creditential)    
    links = moodle_course_links(firefoxBrowser, webscrape_settings)
    for coursename, courselink in links:
        print(coursename)
        print(courselink)
    files = moodle_course_page_files(firefoxBrowser, webscrape_settings, links, 'ELEC3245')
    for filename, filepath in files:
        print(filename)
        print(filepath)
    # time.sleep(10)
    moodle_signout(firefoxBrowser, webscrape_settings)
    
        
    
except Exception: 
    traceback.print_exc()
"""
end scraping
"""
exit(firefoxBrowser, webscrape_settings)
print('===exit ed===')


# firefoxBrowser = makeBrowser(webscrape_settings)
# print('===made===')
# moodle_login(firefoxBrowser, webscrape_settings, creditential)    
# print('===signin ed===')

# """
# start scraping
# """
# try:   
#     links = moodle_course_links(firefoxBrowser, webscrape_settings)
#     if links:
#         for coursename, courselink in links:
#             print(coursename)
#             print(courselink)
#     else:
#         print('nothing')
#     files = moodle_course_page_files(firefoxBrowser, webscrape_settings, links, 'ELEC3245')
#     if files:
#         for filename, filepath in files:
#             print(filename)
#             print(filepath)   
#     else:
#         print('nothing')
    
# except Exception: 
#     traceback.print_exc()
# """
# end scraping
# """
# moodle_signout(firefoxBrowser, webscrape_settings)
# print('===exit ed===')