from notification.stalenotemaster import NoteMaster
from myscraper.webmaster import WebMaster
from time import time, sleep

from myutil.testsuit import testsuit3 as testsuit

credential = {
    'username': '',
    'password': '',
}

# webmaster = WebMaster(credential, {'initialize-website': 'On Demand', 'verbose': 0, 'headless': True})
webmaster = WebMaster(credential)
notemaster = NoteMaster(webmaster, verbose=0)

try:
    for i in range(5):
        notices = notemaster.check(webmaster)
        for notice in notices:
            print(notice['msg'])
        sleep(5)
finally:
    webmaster.terminateThread()
