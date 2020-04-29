# README

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
======Report for NewFirefox       ======
|create browser     :True              |
|get url            :True              |
|get page_source    :True              |
|simple wait        :True              |
|advanced wait      :True              |
|create new tab     :True              |
|switch tab         :True              |
|destroy tab        :True              |
|destroy browser    :True              |
========================================
======Test for NewChrome          ======
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
======Report for NewChrome        ======
|create browser     :True              |
|get url            :True              |
|get page_source    :True              |
|simple wait        :True              |
|advanced wait      :True              |
|create new tab     :True              |
|switch tab         :True              |
|destroy tab        :True              |
|destroy browser    :True              |
========================================
======Test for NewEdge            ======
------Test  0: create browser     ------

DevTools listening on ws://127.0.0.1:55405/devtools/browser/f02bc259-e53b-451f-8dae-68582557345d
[14876:33236:0429/204043.575:ERROR:browser_switcher_service.cc(238)] XXX Init()
[14876:33236:0429/204045.217:ERROR:device_event_log_impl.cc(162)] [20:40:45.216] Bluetooth: bluetooth_adapter_winrt.cc:1055 Getting Default Adapter failed.
------Test  1: get url            ------
------Test  2: get page_source    ------
------Test  3: simple wait        ------
------Test  4: advanced wait      ------
------Test  5: create tab         ------
------Test  6: switch tab         ------
------Test  7: destroy tab        ------
------Test  8: destroy browser    ------
========================================
======Report for NewEdge          ======
|create browser     :True              |
|get url            :True              |
|get page_source    :True              |
|simple wait        :True              |
|advanced wait      :True              |
|create new tab     :True              |
|switch tab         :True              |
|destroy tab        :True              |
|destroy browser    :True              |
========================================
```

If any of the browser is not working, you should replace the webdriver with version that compatible to your browser.  

Edge cannot run headless.  Besides, sometimes Edge cannot pass advanced wait.  Please run again to see it continues to fails.  Usually re-run 1 time is enough.  

### 2. Webmaster

Webmaster is the most complicated one, so instead of trying one by one, run `python testground.py in terminal and check if it matches with the followings: 

```
======Test for Web Master         ======
------Test  0: create webmaster   ------
------Test  1: needBrowser        ------
------Test  2: refresh            ------
------Test  3: query              ------
------Test  4: record             ------
------Test  5: terminateThread    ------
------Test  6: destroy webmaster  ------
========================================
======Report for WebMaster        ======
|create webmaster   :True              |
|needBrowser        :True              |
|refresh            :True              |
|query              :True              |
|record             :True              |
|terminateThread    :True              |
|destroy webmaster  :True              |
========================================
```

Any error thrown is considered as failed.  

### 3. Website

Run `python testground.py` and see if there are any problems: 

```
D:\jupyterbook\Web Scraping\version\Version 9>python testground.py
======Test for testground         ======
('CCST9010 The Science of Crime Investigation [Section 2B, 2016]', 'https://moodle.hku.hk/course/view.php?id=43519')
('ELEC3245 Control and instrumentation [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=61245')
('ELEC3348 Electronic devices [Section 2A, 2017]', 'https://moodle.hku.hk/course/view.php?id=54483')
('ELEC2242 Introduction to electromagnetic waves and fields [Section 2A, 2017]', 'https://moodle.hku.hk/course/view.php?id=54476')
('ENGG1203_2CD ENGG1203 Introduction to electrical and electronic engineering [2016]', 'https://moodle.hku.hk/course/view.php?id=49291')
('COMP3403 Implementation, testing and maintenance of software systems [Section 2A, 2019]', 'https://moodle.hku.hk/course/view.php?id=71755')
('COMP3359 Artificial Intelligence Applications [Section 2A, 2019]', 'https://moodle.hku.hk/course/view.php?id=71754')
('COMP4801 Final year project [Section FA, 2019]', 'https://moodle.hku.hk/course/view.php?id=68569')
('COMP3356 Robotics [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68567')
('COMP3354 Statistical Learning [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68565')
('COMP3270 Artificial intelligence [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68554')
('STUDENT_TA Student Teaching Assistant [2019]', 'https://moodle.hku.hk/course/view.php?id=67628')
('COMP3412 Internship [Section SA, 2018]', 'https://moodle.hku.hk/course/view.php?id=65856')
('COMP3330 Interactive Mobile Application Design and Programming [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60771')
('COMP3314 Machine learning [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60764')
('COMP3311 Legal aspects of computing [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60762')
('COMP3297 Software engineering [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60760')
('COMP3278 Introduction to database management systems [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60758')
('COMP3250 Design and analysis of algorithms [Section 2B, 2018]', 'https://moodle.hku.hk/course/view.php?id=60753')
('COMP3234 Computer and communication networks [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60750')
('COMP3230 Principles of operating systems [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60747')
('COMP2120 Computer organization [Section 2A, 2017]', 'https://moodle.hku.hk/course/view.php?id=54262')
('COMP2119 Introduction to data structures and algorithms [Section 2B, 2017]', 'https://moodle.hku.hk/course/view.php?id=54260')
('COMP2121 Discrete mathematics [Section 1A, 2017]', 'https://moodle.hku.hk/course/view.php?id=51623')
('CCST9029 Cyberspace Crime: Technology and Ethics [Section 1A, 2016]', 'https://moodle.hku.hk/course/view.php?id=43542')
('CAES9542 Technical English for Computer Science [2019]', 'https://moodle.hku.hk/course/view.php?id=69823')
('CCGL9004 Governance and Democracy in the Age of Globalization [2016]', 'https://moodle.hku.hk/course/view.php?id=48855')
('CENG9001 Practical Chinese for Engineering Students [Section 1B, 2018]', 'https://moodle.hku.hk/course/view.php?id=60304')
('COMP3403 Implementation, testing and maintenance of software systems [Section 2A, 2019]', 'https://moodle.hku.hk/course/view.php?id=71755')
('COMP3403 Implementation, testing and maintenance of software systems [Section 2A, 2019]', 'https://moodle.hku.hk/course/view.php?id=71755')
('COMP3359 Artificial Intelligence Applications [Section 2A, 2019]', 'https://moodle.hku.hk/course/view.php?id=71754')
('COMP4801 Final year project [Section FA, 2019]', 'https://moodle.hku.hk/course/view.php?id=68569')
('COMP3356 Robotics [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68567')
('COMP3354 Statistical Learning [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68565')
('COMP3270 Artificial intelligence [Section 1A, 2019]', 'https://moodle.hku.hk/course/view.php?id=68554')
('COMP3412 Internship [Section SA, 2018]', 'https://moodle.hku.hk/course/view.php?id=65856')
('COMP3330 Interactive Mobile Application Design and Programming [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60771')
('COMP3314 Machine learning [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60764')
('COMP3311 Legal aspects of computing [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60762')
('COMP3297 Software engineering [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60760')
('COMP3278 Introduction to database management systems [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60758')
('COMP3250 Design and analysis of algorithms [Section 2B, 2018]', 'https://moodle.hku.hk/course/view.php?id=60753')
('COMP3234 Computer and communication networks [Section 2A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60750')
('COMP3230 Principles of operating systems [Section 1A, 2018]', 'https://moodle.hku.hk/course/view.php?id=60747')
('COMP2120 Computer organization [Section 2A, 2017]', 'https://moodle.hku.hk/course/view.php?id=54262')
('COMP2119 Introduction to data structures and algorithms [Section 2B, 2017]', 'https://moodle.hku.hk/course/view.php?id=54260')
('COMP2121 Discrete mathematics [Section 1A, 2017]', 'https://moodle.hku.hk/course/view.php?id=51623')
('CAES9542 Technical English for Computer Science [2019]', 'https://moodle.hku.hk/course/view.php?id=69823')
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=929905', 'name': 'Course schedule and weekly topics (as of January 5, 2017)', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=929924', 'name': 'Grade descriptors for written work submissions', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=929925', 'name': 'Grade descriptors for active participation', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=929926', 'name': 'Grade descriptors for presentations', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/turnitintooltwo/view.php?id=992041', 'name': 'Submit your Written Assignment here', 'type': 'Turnitin Assignment 2'}
{'link': 'https://moodle.hku.hk/mod/quiz/view.php?id=1004504', 'name': 'One-minute feedback on the autopsy video', 'type': 'Quiz'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1006125', 'name': 'Lecture 10 - Death Registration &amp; Autopsy', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1006122', 'name': 'Tutorial 9 - Trace evidence', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1008706', 'name': 'Tutorial 10 - Legal analysis', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/questionnaire/view.php?id=1001141', 'name': 'Learning Experience Exit Survey', 'type': 'Questionnaire'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1004492', 'name': 'Lecture 9', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1000169', 'name': 'Lecture 8', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=1000167', 'name': 'Tutorial 8 - Case analysis', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/url/view.php?id=994794', 'name': 'Tutorial 7 - Bloodstain pattern analysis', 'type': 'URL'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=995871', 'name': 'Lecture 7 - Cybercrime', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=995946', 'name': 'Mid-Semester Assignment (30%)', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/forum/view.php?id=990608', 'name': 'MID-SEMESTER ASSIGNMENT (30%)', 'type': 'Forum'}
{'link': 'https://moodle.hku.hk/mod/url/view.php?id=990574', 'name': 'Tutorial 6 - Fingerprint', 'type': 'URL'}
{'link': 'https://moodle.hku.hk/mod/questionnaire/view.php?id=990646', 'name': 'Tutorial 6 - Submission of fingerprint examination results', 'type': 'Questionnaire'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=992304', 'name': 'Tutorial 6 - Fingerprint', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=988682', 'name': 'Lecture 5', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=989759', 'name': 'Tutorial 5 - Case analysis', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=982006', 'name': 'Lecture 4', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=985245', 'name': 'Tutorial 4', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=979026', 'name': 'Lecture 3', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=979028', 'name': 'Tutorial 3', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=973025', 'name': 'Lecture 2', 'type': 'File'}
{'link': '', 'name': 'Tutorial 2', 'type': 'File'}
{'link': '', 'name': 'Tutorial 2', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=974647', 'name': 'Tutorial 2', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=969887', 'name': 'Lecture 1', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=969889', 'name': 'Tutorial 1', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/questionnaire/view.php?id=929895', 'name': 'Learning experience survey', 'type': 'Questionnaire'}
{'link': 'https://moodle.hku.hk/mod/forum/view.php?id=930073', 'name': '[Discussion forum] What has brought you to this course?', 'type': ''}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=944963', 'name': 'Required reading: Chapter 1: Forensic Science', 'type': 'File'}
{'link': 'https://moodle.hku.hk/mod/resource/view.php?id=944967', 'name': 'Required reading: Chapter 2: The stakeholders in forensic science', 'type': 'File'}
{'link': '', 'name': 'Group 1 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 2 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 3 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 4 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 5 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 6 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 7 discussion forum', 'type': ''}
{'link': 'https://moodle.hku.hk/mod/forum/view.php?id=929990', 'name': 'Group 8 discussion forum', 'type': ''}
{'link': '', 'name': 'Group 9 discussion forum', 'type': ''}
screenshot1588163841.00976250.5016448454722007.png
{'name': 'Final Report is due', 'link': 'https://moodle.hku.hk/mod/assign/view.php?id=1777980', 'time': '4 May, 00:00'}
{'name': 'Group Final Report (if applicable) is due', 'link': 'https://moodle.hku.hk/mod/assign/view.php?id=1777982', 'time': '4 May, 00:00'}
{'name': 'Source code and Documentation (if applicable) is due', 'link': 'https://moodle.hku.hk/mod/assign/view.php?id=1777983', 'time': '4 May, 00:00'}
{'name': 'Black Box Testing Part 1.1 submission is due', 'link': 'https://moodle.hku.hk/mod/assign/view.php?id=1780013', 'time': '8 May, 23:59'}
TOTAL_DUE
CHRGS_DUE
SSF_SS_BIHDR_VW
Z_BILLPAYH2_TBL
CRSE_HIST
GRID_GPA
ACCT_ACTIVITY
POST_PAY
<table cellpadding="2" cellspacing="0" class="table" id="WEEKLY_SCHED_HTMLAREA" summary="Weekly Schedule" width="100%">
 <colgroup align="center" span="1" valign="middle" width="9%">
 </colgroup>
 <colgroup align="center" span="7" valign="middle" width="13%">
 </colgroup>
 <tbody>
  <tr>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Time
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Monday
    <br/>
    20 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Tuesday
    <br/>
    21 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Wednesday
    <br/>
    22 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Thursday
    <br/>
    23 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Friday
    <br/>
    24 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Saturday
    <br/>
    25 Jan
   </th>
   <th align="center" class="PSLEVEL3GRIDODDROW" scope="col">
    Sunday
    <br/>
    26 Jan
   </th>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     8:00AM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     9:00AM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" style="color:rgb(0,0,0);background-color:rgb(182,209,146);text-align: center;">
    <span class="" style="color:rgb(0,0,0);background-color:rgb(182,209,146);">
     COMP 3359 - 2A
     <br/>
     --
     <br/>
     9:30AM - 10:20AM
     <br/>
     Chow Yei Ching Building CBC
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW" rowspan="4" style="color:rgb(0,0,0);background-color:rgb(182,209,146);text-align: center;">
    <span class="" style="color:rgb(0,0,0);background-color:rgb(182,209,146);">
     COMP 3359 - 2A
     <br/>
     --
     <br/>
     9:30AM - 11:20AM
     <br/>
     Chow Yei Ching Building CBC
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     10:00AM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     11:00AM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     12:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     1:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     2:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     3:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     4:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW" rowspan="4" style="color:rgb(0,0,0);background-color:rgb(182,209,146);text-align: center;">
    <span class="" style="color:rgb(0,0,0);background-color:rgb(182,209,146);">
     COMP 3403 - 2A
     <br/>
     --
     <br/>
     4:30PM - 6:20PM
     <br/>
     Chow Yei Ching Building CBC
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     5:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     6:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     7:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     8:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     9:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="2" scope="row">
    <span class="">
     10:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
  <tr>
   <td class="PSLEVEL3GRIDODDROW" rowspan="1" scope="row">
    <span class="">
     11:00PM
    </span>
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
   <td class="PSLEVEL3GRIDODDROW">
   </td>
  </tr>
 </tbody>
</table>
[{'course': 'COMP 3359 - 2A', 'date': '21 Jan', 'dow': 'Tuesday', 'time': '9:30AM - 10:20AM', 'location': 'Chow Yei Ching Building CBC'}, {'course': 'COMP 3359 - 2A', 'date': '24 Jan', 'dow': 'Friday', 'time': '9:30AM - 11:20AM', 'location': 'Chow Yei Ching Building CBC'}, {'course': 'COMP 3403 - 2A', 'date': '21
Jan', 'dow': 'Tuesday', 'time': '4:30PM - 6:20PM', 'location': 'Chow Yei Ching Building CBC'}]
```

