import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
# from SelenRe import Firefox, Chrome
from seleniumrequests import Firefox, Edge, Chrome

# browser = selenium.webdriver.Edge()

browser = Edge()
print('success')
browser.quit()