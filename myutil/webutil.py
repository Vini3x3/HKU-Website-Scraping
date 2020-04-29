from time import sleep
from bs4 import BeautifulSoup as bs
from myutil import weberror


def util_universal_hku_login(browser, username, password):
    input_username = browser.find_element_by_id('username')
    input_username.send_keys(username)
    input_password = browser.find_element_by_id('password')
    input_password.send_keys(password)
    input_password.submit()
    # browser.wait(1)


def util_getELEMfromProperties(selenium_object, tag_name, feature_dict):
    """
    This function is for getting the selenium object from other properties.  
    the selenium_boject is a selenium object, get from self.browser or self.browser.find('......')
    the feature_dict is like {'class': 'abc'} that for BS4
    the tag_name is a string of the tag name of the target element
    """
    targets = selenium_object.find_elements_by_tag_name(tag_name)        
    
    for target in targets:
        match = True
        for key, value in feature_dict.items():
            if match:   
                if target.get_attribute(key) != value:
                    match = False
        if match:
            return target


def util_HTMLtable2List(soup):
    def rowelem(elem):
        rows = elem.find_all('tr')
        rows = [tr.find_all(['td','th']) for tr in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                rows[i][j] = rows[i][j].get_text().replace(u'\xa0', u' ').replace('\n', '').strip()
        return rows
    thead = soup.find('thead')
    result = []
    if thead:
        # trs = thead.find_all('tr')
        # row = [tr.find_all(['td','th']) for tr in trs]
        # row = [each.get_text() for each in row]
        # result += row
        result += rowelem(thead)
    tbody = soup.find('tbody')
    if tbody:
        result += rowelem(tbody)
        # trs = tbody.find_all('tr')
        # result += [tr.find_all(['td','th']) for tr in trs]

        # row = [tr.find_all(['td','th']) for tr in trs]
        # row = [each.get_text() for each in row]
        # result += row
    if not thead and not tbody:
        result += rowelem(soup)
        # trs = soup.find_all('tr')        
        # result += [tr.find_all(['td','th']) for tr in trs]
    return result


def util_soup2List(soup):
    def rowelem(elem):
        rows = elem.find_all('tr')
        rows = [tr.find_all(['td','th']) for tr in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                rows[i][j] = rows[i][j].get_text().replace(u'\xa0', u' ').replace('\n', '').strip()
        return rows
    thead = soup.find('thead')
    result = []
    if thead:
        result += rowelem(thead)
    tbody = soup.find('tbody')
    if tbody:
        result += rowelem(tbody)        
    if not thead and not tbody:
        result += rowelem(soup)        
    return result