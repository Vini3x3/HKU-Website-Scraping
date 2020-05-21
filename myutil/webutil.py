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


def util_soup2list(soup):
    def row_elem(elem):
        rows = elem.find_all('tr')
        rows = [tr.find_all(['td','th']) for tr in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                rows[i][j] = rows[i][j].get_text().replace(u'\xa0', u' ').replace('\n', '').strip()
        return rows
    thead = soup.find('thead')
    result = []
    if thead:
        result += row_elem(thead)
    tbody = soup.find('tbody')
    if tbody:
        result += row_elem(tbody)
    if not thead and not tbody:
        result += row_elem(soup)
    return result


def util_list_search(search_list, quota=0, exact=False):
    if quota != 0:
        if exact:
            # adjust the quota
            if 0 < quota <= len(search_list):
                adjusted_quota = quota - 1
            elif len(search_list) < quota:
                adjusted_quota = len(search_list)
            elif -1 * len(search_list) < quota < 0:
                adjusted_quota = quota
            elif quota < -1 * len(search_list):
                adjusted_quota = -1 * len(search_list)
            else: # input = 0
                return
            # output
            return search_list[adjusted_quota]
        else:
            # adjust the quota
            if 0 < quota <= len(search_list):
                adjusted_quota = quota
            elif len(search_list) < quota:
                adjusted_quota = len(search_list)
            elif -1 * len(search_list) < quota < 0:
                adjusted_quota = quota
            elif quota < -1 * len(search_list):
                adjusted_quota = -1 * len(search_list)
            else: # input = 0
                return []
            # output
            if 0 < adjusted_quota <= len(search_list):
                return search_list[0:adjusted_quota]
            else:
                result = []
                for i in range(len(search_list) - 1, len(search_list) + adjusted_quota - 1, -1):
                    # print(i)
                    result.append(search_list[i])
                return result
    else:
        return search_list
