from seleniumrequests import Chrome

browser = Chrome()
try:
    print(browser)
    r  = browser.request('get','http://info.cern.ch/')
    print(r.text)    
except:    
    print('chrome not working')
finally:
    browser.quit()