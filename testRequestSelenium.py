from selenium.webdriver import Chrome, ChromeOptions
import requests
from time import time, sleep
from myutil import webutil
import bs4

options = ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser = Chrome(options=options, executable_path='myengine\chromedriver')

credential = {
    'username': '',
    'password': ''
}

sitelinks = {
    'home': 'https://moodle.hku.hk',
    'login': 'http://moodle.hku.hk/login',
    'login_sublink_1': 'https://moodle.hku.hk/login/index.php?authCAS=CAS',
    'login_sublink_2': 'https://moodle.hku.hk/login/index.php',
    'logout': 'https://moodle.hku.hk/login/logout.php?sesskey=',
    'deadlines': 'https://moodle.hku.hk/my/?myoverviewtab=timeline',
}

#  moodle_page = 'https://moodle.hku.hk/course/view.php?id=68569'
moodle_page = 'https://moodle.hku.hk/mod/forum/discuss.php?d=532106'

# login procedure

browser.get(sitelinks['login'])
browser.find_element_by_id('login-nav-btn').click()
sleep(1)
print('branch')
if browser.current_url == sitelinks['home'] or browser.current_url == sitelinks['home'] + '/':
    print('end case 1')
else:
    if browser.current_url == sitelinks['login_sublink_2']:
        browser.get(sitelinks['login_sublink_1'])
        webutil.util_universal_hku_login(browser, credential)
        print('end case 2')
    elif browser.current_url == sitelinks['login_sublink_1']:
        webutil.util_universal_hku_login(browser, credential)
        print('end case 3')
    else:
        print('end case error')
        print(browser.current_url)

sleep(2)

browser.get(moodle_page)
actual_title = browser.title
print(actual_title)

html_1 = browser.page_source

# transfer cookies
pass_cookies = {}
for cookie in browser.get_cookies():
    pass_cookies[cookie['name']] = cookie['value']

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'referer': 'https://hkuportal.hku.hk/login.html'
}

"""
# requests trial
for _ in range(20):
    r = requests.get(moodle_page, cookies = pass_cookies, headers = headers)
    soup = bs4.BeautifulSoup(r.text, features='lxml')
    requests_title = soup.title.string
    print(requests_title)
#  if requests_title != actual_title:
"""

r = requests.get(moodle_page, cookies = pass_cookies, headers = headers)
html_2 = r.text

# print(html_1)
# print('===')
# print(html_2)

soup_1 = bs4.BeautifulSoup(html_1, features='lxml')
result_1 = soup_1.find_all('div', class_="posting fullpost")[1].text
print(result_1)

soup_2 = bs4.BeautifulSoup(html_2, features='lxml')
result_2 = soup_1.find_all('div', class_="posting fullpost")[1].text
print(result_2)



browser.quit()

