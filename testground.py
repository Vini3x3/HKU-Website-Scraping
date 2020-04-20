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
    result = webmaster.query('Moodle','getSiteMap')
    for _ in result:
        print(_)
    result = webmaster.query('Moodle','findAllCoursesByKeywords', 'comp')
    for _ in result:
        print(_)

    result = webmaster.query('Moodle', 'scrapeCourseContents', 'https://moodle.hku.hk/course/view.php?id=43519')
    print(result)
    result = webmaster.query('Moodle', 'scrapeCourseContentPreview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
    print(result)
    result = webmaster.query('Portal', 'findInvoice')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'findTranscript')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'findAccountActivity')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'findReceipt')
    for key in result.keys():
        print(key)
    result = webmaster.query('Portal', 'findWeeklySchedule', '25/01/2020', '8:00AM', '11:00PM')
    print(result)


# webmaster = WebMaster(credential, webscrape_settings)
webmaster = WebMaster(credential)
testground(webmaster)
webmaster.terminateThread()


