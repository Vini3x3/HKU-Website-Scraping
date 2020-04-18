from bs4 import BeautifulSoup as bs
from selenium import webdriver

import traceback
import time

# login-logout-setup module

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
    result = []
    browser.get(webscrape_settings['exitpage'])
    soap = bs(browser.page_source, features='lxml')
    for link in soap.find_all("a"):
        if link['href'][0:4] == 'http':
            result.append(link['href'])
    return result

# weekly schedule module