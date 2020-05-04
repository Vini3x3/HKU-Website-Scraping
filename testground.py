from myutil.testsuit import testsuit3 as testsuit
from myscraper.webmaster import WebMaster

from tabulate import tabulate


credential = {
    'username': '',
    'password': '',
}

webscrape_settings = {
    # 'browser': 'Edge',
    # 'headless': False,
    'verbose': 2,
    # 'initialize-website': 'All',
}


@testsuit.log('field', 'testground')
@testsuit.errorTest
def testground(webmaster):
    # result = webmaster.query('Moodle','getSiteMap')
    # for _ in result:
    #     print(_)
    # result = webmaster.query('Moodle','findAllCoursesByKeywords', 'Network')
    # print(result)
    # for _ in result:
    #     print(_)
    #
    # result = webmaster.query('Moodle', 'scrapeCourseContents', 'https://moodle.hku.hk/course/view.php?id=43519')
    # print(result)
    # result = webmaster.query('Moodle', 'scrapeCourseContentPreview', 'https://moodle.hku.hk/mod/assign/view.php?id=1738380')
    # print(result)
    # result = webmaster.query('Moodle', 'scrapeDeadlines')
    # for _ in result: print(_)
    # result = webmaster.query('Portal', 'findInvoice')
    # for key in result.keys():
    #     print(key)
    # print('hi')
    # result = webmaster.query('Portal', 'findTranscript')
    # for key in result.keys():
    #     print(key)
    # print('hi')
    # result = webmaster.query('Portal', 'findAccountActivity')
    # for key in result.keys():
    #     print(key)
    # print('hi')
    # result = webmaster.query('Portal', 'findReceipt')
    # for key in result.keys():
    #     print(key)
    # print('hi')
    result = webmaster.query('Portal', 'findWeeklySchedule', '10/09/2020', '8:00AM', '11:00PM')
    print(result)
    # result = webmaster.query('Portal', 'findWeeklySch', '25/01/2020', '8:00AM', '11:00PM')
    # print(len(result))
    # result = webmaster.query('Moodle', 'findCourseContent', 'Implementation', ': ', ['File'], -1, False, False)
    # for _ in result: print(_)
    # result = webmaster.query('Moodle', 'scrapeCourseContents', 'https://moodle.hku.hk/course/view.php?id=43519')
    # for _ in result:
    #     print(_)
    # 'scrapeCourseContents'
    # 'findCourseContents'
    # result = webmaster.query('Portal', 'findTable', ['GRID_GPA', 'Z_BILLPAYH2_TBL', 'TOTAL_DUE'])
    # for key in result:
    #     print(key)
    # result = webmaster.query('Moodle', 'scrapeFolder', 'https://moodle.hku.hk/mod/folder/view.php?id=1375828')
    # result = webmaster.query('Moodle', 'findCourseContents', 'https://moodle.hku.hk/course/view.php?id=68567')

    # result = webmaster.query('Moodle', 'superSearch', 'COMP3234',
    #                          {
    #                              'file_keywords': [['slide', 'chapter', 'lecture'], ['transport'], ['TCP']],
    #                              'type': ['File'],
    #                              'quota': -2,
    #                              'exact': False
    #                          }
    #                          )
    # print(tabulate(result, headers='keys'))


# webmaster = WebMaster(credential, webscrape_settings)
webmaster = WebMaster(credential)
testground(webmaster)
webmaster.terminateThread()

