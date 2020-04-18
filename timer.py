import traceback
import time

import webmaster

webscrape_settings = {    
    'browser': 'FireFox',
    'headless': True,
    'debug': False,
    'initialize-website': 'All',
}

creditential = {
    'username': '',
    'password': '',
}

# test for the initialize-website settings in webscrape_settings

iteration = 5

total_time = 0
for _ in range(iteration):

    start_time = time.time()

    A = webmaster.WebMaster(creditential, webscrape_settings)

    result = A.callMethod('getAssignmentPath', 'COMP3270')    
    
    print(len(result))
    
    del A
    
    total_time += (time.time() - start_time)
    
print(total_time / iteration)

webscrape_settings['initialize-website'] = 'Only Portal'

total_time = 0
for _ in range(iteration):

    start_time = time.time()

    A = webmaster.WebMaster(creditential, webscrape_settings)

    result = A.callMethod('getAssignmentPath', 'COMP3270')    
    
    print(len(result))
    
    del A
    
    total_time += (time.time() - start_time)
    
print(total_time / iteration)

webscrape_settings['initialize-website'] = 'On Demand'

total_time = 0
for _ in range(iteration):

    start_time = time.time()

    A = webmaster.WebMaster(creditential, webscrape_settings)

    result = A.callMethod('getAssignmentPath', 'COMP3270')    
    
    print(len(result))
    
    del A
    
    total_time += (time.time() - start_time)
    
print(total_time / iteration)
