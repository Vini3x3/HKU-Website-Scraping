from bs4 import BeautifulSoup as bs
from selenium import webdriver

import traceback
import time

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