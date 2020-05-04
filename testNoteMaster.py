from notification.notemaster import NoteMaster
from myscraper.webmaster import WebMaster
from time import time, sleep

from myutil.testsuit import testsuit3 as testsuit

# credential = {
#     'username': 'u3537502',
#     'password': 'YourMother62329197',
# }

credential = {
    'username': 'approach',
    'password': '123456789yht',
}

# webmaster = WebMaster(credential, {'initialize-website': 'On Demand', 'verbose': 0, 'headless': True})
webmaster = WebMaster(credential)
notemaster = NoteMaster(interval=2, verbose=1)

try:
    # notemaster.add_default_notifiers(webmaster)
    # notemaster.add_notifier('simple_alarm_strategy', webmaster, delay=2, range=2)
    # notemaster.add_notifier('moodle_deadline_strategy', webmaster, delay=4, range=2)
    # notemaster.add_notifier('portal_next_lesson_strategy', webmaster, delay=6, range=2)
    # notemaster.add_notifier('portal_get_invoice_strategy', webmaster, delay=2, range=2)
    # notemaster.add_notifier('moodle_course_updated', webmaster, delay=2, range=2)
    print('start')
    notemaster.start(webmaster)
    sleep(7)
finally:
    notemaster.cancel()
    webmaster.terminateThread()
