from myutil.testsuit import testsuit3 as testsuit
from myscraper.webmaster import WebMaster

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
    result = webmaster.query('Moodle', 'scrape_course_content', 'https://moodle.hku.hk/course/view.php?id=43519')
    for _ in result: print(_)
    result = webmaster.query('Moodle', 'scrape_course_preview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
    print(result)
    result = webmaster.query('Moodle', 'scrape_deadlines')
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


# webmaster = WebMaster(credential, webscrape_settings)
webmaster = WebMaster(credential['username'], credential['password'])
testground(webmaster)
webmaster.cancel()



