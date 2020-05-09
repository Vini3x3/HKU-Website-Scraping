from myutil.testsuit import testsuit3 as testsuit
from myscraper.webmaster import WebMaster
from time import sleep
from tabulate import tabulate

import abc

credential = {
    'username': '',
    'password': '',
}


@testsuit.log('field', 'testground')
@testsuit.errorTest
def testground(webmaster):
    result = webmaster.query('Moodle', 'find_course_by_keywords', 'comp')
    print(result)
    result = webmaster.query('Moodle', 'find_all_courses_by_keywords', 'comp')
    for _ in result: print(_)
    result = webmaster.query('Moodle', 'find_page_preview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
    print(result)
    result = webmaster.query('Moodle', 'find_deadlines')
    for _ in result: print(_)
    result = webmaster.query('Portal', 'find_invoice')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'find_transcript')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'find_account_activity')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'find_receipt')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'display_weekly_sch', '25/01/2020')
    print(result)
    result = webmaster.query('Portal', 'find_weekly_sch', '25/01/2020')
    print(tabulate(result, headers='keys'))
    result = webmaster.query('Moodle', 'find_course_contents',
                             'Computer and Communication Networks', ['URL', 'Assignment'], search=[['problem-set']], quota=-2
                             )
    print(tabulate(result, headers='keys'))


webmaster = WebMaster(credential['username'], credential['password'], verbose=0, headless=True)
testground(webmaster)

# print(result)
# print(tabulate(result, headers='keys'))
# print(tabulate(result, headers='firstrow'))

# get WebMaster history
records = webmaster.get_record()

# not in use
webmaster.cancel()



