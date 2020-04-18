from SelenRe import Firefox, Chrome, NewFirefox
# from seleniumrequests import Firefox, Chrome
import traceback
# from selenium import webdriver

webscrape_settings = {
    'debug': True,
    # 'options': ['--headless'],
}
browser = NewFirefox(webscrape_settings)
# browser = Firefox()
try:
    print(browser)

    r  = browser.request('get','http://info.cern.ch/')
    print(r.text)

    print(browser.current_url)
    browser.get('http://info.cern.ch/')
    browser.wait(2)
    print(browser.current_url)
    As = browser.find_elements_by_tag_name('a')
    text_list = []
    href_list = []
    for each in As: 
        text_list.append(each.text)
        href_list.append(each.get_attribute('href'))
    for i in range(len(text_list)):
        browser.tab(text_list[i],href_list[i])
        
    browser.wait(10)
    browser.untab('Browse the first website')
    browser.wait(10)
    browser.tab('Learn about the birth of the web')
    browser.wait(10)
    browser.tab(0)
    browser.wait(10)
    browser.test()
except:
    traceback.print_exc()
finally:
    browser.quit()