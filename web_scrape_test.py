import selenium
import requests
from bs4 import BeautifulSoup as bs
import requests_html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def signin(browser, creditential, webscrape_settings):
    """
    input a browser object and sign in
    """
    browser.get(webscrape_settings['homepage'])

    username = browser.find_element_by_id('username')
    username.send_keys(creditential['username'])
    password = browser.find_element_by_id('password')
    password.send_keys(creditential['password'])
    password.submit()
    time.sleep(1)

def exit(browser, webscrape_settings):
    """
    exit by inputing a browser object
    """
    browser.get(webscrape_settings['exitpage'])
    signout = browser.find_element_by_link_text('Sign out')
    signout.click()
    browser.quit()

def getPortalLinks(browser, webscrape_settings):
    list = []
    browser.get(webscrape_settings['exitpage'])
    soap = bs(browser.page_source, features='lxml')
    for link in soap.find_all("a"):
        if link['href'][0:4] == 'http':
            list.append(link['href'])
    return list

def findWeeklySchedule(browser, webscrape_settings, portal_links):
    weekly_schedule_url = ''
    for link in portal_links:
        if webscrape_settings['weekSchpage'] in link:
            weekly_schedule_url = link
    print(weekly_schedule_url)
    firefoxBrowser.get(weekly_schedule_url)
    print(firefoxBrowser.page_source)

    soap = bs(firefoxBrowser.page_source, features='lxml')
    frame = soap.find('frame')
    # for each in frame:
    #     # if each['name'] == 'TargetContent':
    #     #     print(each['src'])
    #     print(each['src'])


    # table = soap.find(id='WEEKLY_SCHED_HTMLAREA')
    # print(table)
    # tables = soap.find('table')
    # for each in tables:
    #     print(each['class'])
    # return tables

# WEEKLY_SCHED_HTMLAREA

webscrape_settings = {
    'homepage': 'https://hkuportal.hku.hk/login.html',
    'exitpage': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/EMPL/h/?tab=DEFAULT',
    'weekSchpage': 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W',
    'driver': 'C:\\Users\\vince\\AppData\\Local\\Temp\\geckodriver-v0.26.0-win64\\geckodriver.exe'
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
portal_links = getPortalLinks(firefoxBrowser, webscrape_settings)

# soap = bs(firefoxBrowser.page_source, features='lxml')
# weekly_schedule_url = ''
# for link in soap.find_all("a"):
#     if 'https://sis-eportal.hku.hk/psp/ptlprod/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W' in link['href']:
#         weekly_schedule_url = link['href']
# firefoxBrowser.get(weekly_schedule_url)

# print('got weekly schedule')
table = findWeeklySchedule(firefoxBrowser, webscrape_settings, portal_links)
print(table)
"""
end scraping
"""
exit(firefoxBrowser, webscrape_settings)
print('===exit ed===')