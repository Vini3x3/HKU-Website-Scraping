from myutil.testsuit import testsuit3 as testsuit
from myscraper.webmaster import WebMaster
from time import sleep
from tabulate import tabulate

credential = {
    'username': '',
    'password': '',
}

webscrape_settings = {
    # 'browser': 'Edge',
    # 'headless': False,
    # 'verbose': 3,
    # 'initialize-website': 'All',
}


@testsuit.log('field', 'testground')
@testsuit.errorTest
def testground(webmaster):
    result = webmaster.query('Moodle', 'get_sitemap')
    for _ in result:
        print(_)
    result = webmaster.query('Moodle', 'find_course_by_keywords', 'comp')
    print(result)
    result = webmaster.query('Moodle', 'find_all_courses_by_keywords', 'comp')
    for _ in result: print(_)
    result = webmaster.query('Moodle', 'find_course_contents', 'https://moodle.hku.hk/course/view.php?id=43519')
    for _ in result: print(_)
    result = webmaster.query('Moodle', 'scrape_course_preview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
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
    result = webmaster.query('Portal', 'display_weekly_schedule', '25/01/2020', '8:00AM', '11:00PM')
    print(result)
    result = webmaster.query('Portal', 'find_weekly_sch', '25/01/2020', '8:00AM', '11:00PM')
    print(result)



@testsuit.timedTest(repeat=1)
def test_1(webmaster):
    result = webmaster.query('Moodle', 'find_course_contents', 'crime investigation')
    # result = webmaster.query('Moodle', 'find_deadlines')
    print(len(result))

# webmaster = WebMaster(credential, webscrape_settings)
webmaster = WebMaster(credential['username'], credential['password'], verbose=0)
# testground(webmaster)

# create WebMaster
# webmaster = WebMaster('username', 'password')

# use WebMaster
# result = webmaster.query('Moodle', 'find_deadlines')
# print(test_1(webmaster))
result = webmaster.query('Moodle', 'find_course_contents',
                         'Computer and Communication Networks', ['URL', 'Assignment'], search=[['problem-set']], quota=-2
                         )
# print(len(result))
# result = webmaster.query('Moodle', 'find_deadlines')
# result = webmaster.query('Moodle', 'test', 'https://moodle.hku.hk/course/view.php?id=43519')

# result = webmaster.query('Portal', 'find_weekly_sch', '25/04/2020')
# print(result)
print(tabulate(result, headers='keys'))

# get WebMaster history
records = webmaster.get_record()

# not in use
webmaster.cancel()


