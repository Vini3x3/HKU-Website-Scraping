import traceback
import time

import website
import moodle
import portal

webscrape_settings = {    
    'browser': 'FireFox',
    'headless': True,
    'debug': False,
}

creditential = {
    'username': '',
    'password': '',
}

A = moodle.Moodle(creditential, webscrape_settings)
try:
    # """
    # submit assignemnt via file manager plugin
    # """
    # submits = A.getAssignmentPath('COMP3330')
    # print(submits[0])
    # A.submit_file(submits[0][1], ['C:\\Users\\vince\\Downloads\\error.png'])
    # """
    # submit assignemnt via turnitin
    # """
    # submits = A.getAssignmentPath('CAES9542')
    # print(submits[0])
    # A.submit_file(submits[0][1], 'C:\\Users\\vince\\Downloads\\error.png')
    # """
    # Get course file in a course
    # """
    # files = A.course_page_files('ELEC3241')    
    # A.downloadFile(files[0][1])

    # time = 10*60
    # while time>0:
    #     A.keepAlive()
    
    # """
    # Get course assignmet, quiz results
    # """
    table = A.getGrades('COMP3270') 
    print(table)

except:
    traceback.print_exc()
finally:
    del A

# B = portal.Portal(creditential, webscrape_settings)
# try:
    # """
    # get weekly schedule
    # """
    # schedule = B.findWeeklySchedule(['25/01/2020','8:00AM','11:00PM'])
    # print(schedule)
    # """
    # get student GPA
    # """
    # table = B.getStudentGPA()
    # print(table)
    # """
    # get student Course Grades
    # """
    # table = B.getStudentCourseGrades()
    # print(table)
    # """
    # get student invoice
    # """
    # table = B.getInvoices()
    # print(table)
    
# except:
#     traceback.print_exc()
# finally:
#     del B
