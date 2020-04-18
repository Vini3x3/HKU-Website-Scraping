from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time

driverpath = r'C:\\Users\\vince\\AppData\\Local\\Temp\\geckodriver-v0.26.0-win64\\geckodriver.exe'
usernameStr = '' # fill up
passwordStr = '' # fill up

url = 'https://hkuportal.hku.hk/login.html'


try:
    fireFoxOptions = webdriver.FirefoxOptions()
    browser = webdriver.Firefox(options=fireFoxOptions, executable_path=driverpath)
    browser.get(url)

    username = browser.find_element_by_id('username')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('password')
    password.send_keys(passwordStr)
    password.submit()
    time.sleep(1)
    # print(browser.page_source)
    for cookie in browser.get_cookies():
        print(cookie['name'])

    print('success login')

    links = browser.find_element_by_link_text('Sign out')
    print(links.get_attribute('innerHTML'))
    links.click()
    browser.quit()

finally:
    try:
        brower.close()
    except:
        pass