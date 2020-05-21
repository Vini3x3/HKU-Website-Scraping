# Finalized Version

[TOC]

## Dependencies

```python
# Default libraries
import time
import inspect
import threading
import datetime
import traceback
import re
# Need Install
import cachetools
import bs4
import lxml
import selenium
```

### Techniques

list of techniques used in the project

- distributing packages
- decorator
- multithreading
- caching

---

list of optimization used

- design pattern
- logging and verbose
- test suite

## What are they

Below is the file structure of this release / version:

```
./
    folderTree.py
    README.md
    testground.py
    testNativeBrowser.py
    testWebMaster.py
    myengine/
        chromedriver.exe
        geckodriver.exe
        MicrosoftWebDriver.exe
    myscraper/
        HKUSites.py
        NativeBrowser.py
        webmaster.py
    myutil/
        testsuit.py
        weberror.py
        webutil.py
```

As we can see a big restructure was performed.  Below is the details of each part:

### myutil

- weberror.py: the web error that used in the below packages
- webutil.py: useful functions that often used
- testsuit.py: testing classes that help testing

### myengine

- chromedriver.exe: webdriver of Chrome
- geckodriver.exe: webdriver of Firefox
- MicrosoftWebDriver.exe: webdriver of Edge

### myscraper

- NativeBrowser.py: selenium browser upgraded
- HKUSites.py: websites of HKU
- webmaster.py: webmaster that controlls all the things

---

## How to use

The testcase are good examples on how to use them.  In general, you **should** only use webmaster with credentials.  (see testground.py).  

### Default Scenario

1. import library

   ```python
   from myscraper.webmaster import WebMaster
   ```

3. make a webmaster instance

   ```python
   B = WebMaster(username='username', password='password')
   ```

4. query it and get a result

   ```python
   result = B.query('Moodle', 'get_sitemap')
   ```



5. terminate the thread when no longer in use

   ```python
   B.cancel()
   ```

### Other usage

- Get the record of the webmaster

  ```python
  for line in B.get_record():
     print(line)
  ```

  Result:

  ```verilog
  [ 2020-04-06 20:31:36.576511 ] Moodle               > get_sitemap           :
  ```

  This is the called website, called function and called function arguments in string format.  

### Other settings

You can pass other settings into the webmaster like this:

```python
B = WebMaster(username='username', password='password', verbose=2)
```

Below is a list of options:

- `verbose` ==Integer==: the depth of debugging level you want to see, 3 is enough to see all.  
- `headless`==Boolean==: if False, then turn off headless mode and show browser screen
- `init_setting`==String==: 3 options: 'All', 'Only Portal' and 'On Demand'
- `browser_name` ==String==: 3 options: 'Chrome', 'Firefox' and 'Edge'
- `options`: browser options in `list`
- `path`: browser path

## Functionalities

| Name                         | Site   | Input                                                        | Output                                                   | Usage                                  |
| ---------------------------- | ------ | ------------------------------------------------------------ | -------------------------------------------------------- | -------------------------------------- |
| get_sitemap                  | Moodle | None                                                         | list of tuples, `('name','link')`                        | get the accessible course of the user  |
| find_course_by_keywords      | Moodle | string                                                       | tuple, `('name', 'link')`                                | search course by keywords              |
| find_all_courses_by_keywords | Moodle | string                                                       | list of tuples, `('name','link')`                        | search courses by keywords             |
| scrape_course_contents       | Moodle | string                                                       | list of dict, `{'link', 'name','type'}`                  | get the content of the course          |
| scrape_course_preview        | Moodle | string                                                       | filename of screenshot of the main content               | get the preview of the course content  |
| scrape_deadlines             | Moodle | None                                                         | list of dict, `{'name','link', 'time'}`                  | get the list of deadlines              |
| get_site_map                 | Portal | None                                                         | list of tuples, `('name','link')`                        | list of links in the sidemenu          |
| display_weekly_schedule      | Portal | targetdate, starttime, endtime (string in dd/mm/yyyy format) | HTML string of the timetable                             | get the weekly schedule of the user    |
| find_weekly_sch              | Portal | targetdate, starttime, endtime (string in dd/mm/yyyy format) | list of dictionary `{'course','date','dow','time','loc}` | get the parsed weekly schedule of user |
| find_transcript              | Portal | None                                                         | dictionary with list of list (table)                     | get information of that page           |
| find_invoice                 | Portal | None                                                         | dictionary with list of list (table)                     | get information of that page           |
| find_receipt                 | Portal | None                                                         | dictionary with list of list (table)                     | get information of that page           |
| find_account_activity        | Portal | None                                                         | dictionary with list of list (table)                     | get information of that page           |

## How to test

These files are created for testing:

- `testBrowser.py`: test the functionalities of `NativeBrowser.py`
- `testWebMaster.py`: test the functionalities of `WebMaster.py`
- `testground.py`: testing the functionalities of `HKUSites.py`

You should test with the above order.  

To run the test file, simple command `python <filename>`

### 1. NativeBrowser

run  `python testNativeBrowser.py` in terminal and you should get the following result:

```
D:\jupyterbook\Web Scraping\version\Version 9>python testNativeBrowser.py
======Test for NewFirefox         ======
------Test  0: create browser     ------
------Test  1: get url            ------
------Test  2: get page_source    ------
------Test  3: simple wait        ------
------Test  4: advanced wait      ------
------Test  5: create tab         ------
------Test  6: switch tab         ------
------Test  7: destroy tab        ------
------Test  8: destroy browser    ------
========================================

- Use sematic python class annotations
- remove browser cache functions
- add advanced selected HTML function for better parser caching
