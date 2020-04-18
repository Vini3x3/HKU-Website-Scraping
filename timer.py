import traceback
import time

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

iteration = 20

A = moodle.Moodle(creditential, webscrape_settings)
total_time = 0
for _ in range(iteration):
    start_time = time.time()

    result = A.course_page_files('COMP2121')
    
    total_time += (time.time() - start_time)
    print(len(result))
    
print(total_time / iteration)
del A