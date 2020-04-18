import traceback

import webmaster

webscrape_settings = {    
    'browser': 'FireFox',
    'headless': True,
    'debug': False,
    'initialize-website': 'On Demand',
}

creditential = {
    'username': '',
    'password': '',
}

A = webmaster.WebMaster(creditential, webscrape_settings)
try:
    # A.wait()
    # A.printMethods()
    # result = A.callMethod('findWeeklySchedule', argv = ['25/01/2020','8:00AM','11:00PM'])
    # print(result)
    # result = A.callMethod('findWeeklySchedule', argv = ['25/01/2020','8:00AM','11:00PM'], class_name='Portal')
    # print(result)
    # result = A.callMethod('getSiteMap', class_name='Moodle')
    # for _ in result:
    #     print(_)
    # print(result)
    # result = A.callMethod('getSiteMap')
    # print(result)
    # result = A.callMethod('findWeeklySchedule')
    # print(result)
    # result = A.callMethod('ABC')
    # print(result)
    # result = A.callMethod('getGrades', 'COMP3270')
    # print(result)
    # result = A.callMethod('getAssignmentPath', 'COMP3270')
    # print(result)
    # A.stayAlive()
    A.moodle_getSiteMap()
    # url = A.moodle_getCourseLink(60758)
    # print(url)
    # if len(url) > 0:
        # cache = A.moodle_getCourseContent(url)
        # for _ in cache:
        #     print(_)
    # A.moodle_getCourseContent(60758)
    # cache = A.moodle_getCacheCourse(60758)
    # for _ in cache:
    #     print(_)
    print('======')
    cache = A.moodle_getContentType(60758, 'submit_file_upload')
    for _ in cache:
        print(_)
    cache = A.moodle_getContentType(60758, 'submit_turnitin')
    for _ in cache:
        print(_)
    
except:
    traceback.print_exc()
finally:
    A.terminate_thread()
    del A


# A = webmaster.WebMaster(creditential, webscrape_settings)
# try:
#     func_name = input('Function?')
#     argv = input('Arguement?')
#     class_name = input('Class?')
#     if argv == '':
#         argv = None
#     while func_name != '__del__':
#         if argv:
#             result = A.callMethod(func_name, argv, class_name=class_name)        
#         else:
#             result = A.callMethod(func_name, class_name=class_name)        
#         print(result)
#         # print(func_name)
#         # print(argv)
#         func_name = input('Function?')
#         argv = input('Arguement?')
#         class_name = input('Class?')
#         if argv == '':
#             argv = None
# finally:
#     A.terminate_thread()
#     del A