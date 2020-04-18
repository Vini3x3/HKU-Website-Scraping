# Fully Functioned Structural Upgrade

After give up Request API, I rewrote the things so that it is in OOP and optimized structure compare to before.  Below is divided into 4 parts: Dependencies, What are they, How to use and how to test.  

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
    readme.md
    testground.py
    testNativeBrowser.py
    tests.py
    testwebmanager.py
    mydev/
        changes.py
        changes2.py
        __init__.py
    myengine/
        chromedriver.exe
        geckodriver.exe
        MicrosoftWebDriver.exe
    myscraper/
        HKUSites.py
        NativeBrowser.py
        webmanager.py
        webmaster.py
        __init__.py
    myutil/
        testsuit.py
        weberror.py
        webutil.py
        __init__.py
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
- webmanager.py: managver of the website of HKU
- webmaster.py: webmaster that controlls all the things

### mydev

- changes.py: Things will be changed in future

---

Through this structure, I expect the future release only change the mydev/changes.py.  

## How to use

The testcase are good examples on how to use them.  In general, you **should** only use webmaster with credentials.  (see testground.py).  

### Default Scenario

1. import library

   ```python
   from myscraper.webmaster import WebMaster
   ```
   
2. define your credentials

   ```python
   credential = {
       'username': 'username',
       'password': 'password',
   }
   ```

3. make a webmaster instance

   ```python
   B = WebMaster(credential)
   ```

4. query it and get a result

   ```python
   result = B.query('Moodle', 'getSiteMap')
   ```

   

5. terminate the thread when no longer in use

   ```python
   B.terminateThread()
   ```

### Other usage

- Get the record of the webmaster

  ```python
  for line in B.getRecord():
     print(line)
  ```

  Result:

  ```verilog
  [ 2020-04-06 20:31:36.576511 ] Moodle               > getSiteMap           : 
  ```

  This is the called website, called function and called function arguments in string format.  

### Other settings

You can pass a webscrape_settings into the webmaster like this: 

```python
webscrape_settings = {
    # 'option name': option value,
    'verbose': 3,
}
B = WebMaster(credential, webscrape_settings)
```

Below is a list of options: 

- `verbose` ==Integer==: the depth of debugging level you want to see, 3 is enough to see all.  
- `headless`==Boolean==: if False, then turn off headless mode and show browser screen
- `initialize-website`==String==: 3 options: 'All', 'Only Portal' and 'On Demand'
- `browser` ==String==: 3 options: 'Chrome', 'Firefox' and 'Edge'

## How to test

You should run 3 tests to see is all level are working together.  

### 1. NativeBrowser

run testNativeBrowser.py, and you should get the following result: 

```
PS D:\jupyterbook\Web Scraping\version\Version 5> python .\testNativeBrowser.py
======Test for NewFirefox          ======
------Test  0: create browser      ------
------Test  1: get url             ------
------Test  2: get page_source     ------
------Test  3: simple wait         ------
------Test  4: advanced wait       ------
------Test  5: create tab          ------
------Test  6: switch tab          ------
------Test  7: destroy tab         ------
------Test  8: destroy browser     ------
=========================================
======Report for NewFirefox        ======
|create browser      :True              |
|get url             :True              |
|get page_source     :True              |
|simple wait         :True              |
|advanced wait       :True              |
|create new tab      :True              |
|switch tab          :True              |
|destroy tab         :True              |
|destroy browser     :True              |
=========================================
======Test for NewChrome           ======
------Test  0: create browser      ------
------Test  1: get url             ------
------Test  2: get page_source     ------
------Test  3: simple wait         ------
------Test  4: advanced wait       ------
------Test  5: create tab          ------
------Test  6: switch tab          ------
------Test  7: destroy tab         ------
------Test  8: destroy browser     ------
=========================================
======Report for NewChrome         ======
|create browser      :True              |
|get url             :True              |
|get page_source     :True              |
|simple wait         :True              |
|advanced wait       :True              |
|create new tab      :True              |
|switch tab          :True              |
|destroy tab         :True              |
|destroy browser     :True              |
=========================================
======Test for NewEdge             ======
------Test  0: create browser      ------

DevTools listening on ws://127.0.0.1:56062/devtools/browser/a1c36d63-09ef-4baa-821e-d0196092e0d3
------Test  1: get url             ------
------Test  2: get page_source     ------
------Test  3: simple wait         ------
------Test  4: advanced wait       ------
------Test  5: create tab          ------
------Test  6: switch tab          ------
------Test  7: destroy tab         ------
------Test  8: destroy browser     ------
=========================================
======Report for NewEdge           ======
|create browser      :True              |
|get url             :True              |
|get page_source     :True              |
|simple wait         :True              |
|advanced wait       :True              |
|create new tab      :True              |
|switch tab          :True              |
|destroy tab         :True              |
|destroy browser     :True              |
=========================================
```

If any of the browser is not working, you should replace the webdriver with version that compatible to your browser.  

Edge cannot run headless.  Besides, sometimes Edge cannot pass advanced wait.  Please run again to see it continues to fails.  Usually re-run 1 time is enough.  

### 2. Webmanager

run testWebManager.py, and you should get the following result: 

```
PS D:\jupyterbook\Web Scraping\version\Version 5> python .\testwebmanager.py
0.7947165966033936
```

This is the time for scraping a sitemap.  

However, if the following happens: 

1. The time is exceeding 9 seconds

   This means the caching function is not working.  

2. Throw weberror

   This means the scrape function is not working.  

### 3. Webmaster

Webmaster is the most complicated one, so instead of trying one by one, run testground.py and check if the log is same as below except the timestamp and command: 

```verilog
PS D:\jupyterbook\Web Scraping\version\Version 5> python .\testground.py
[ 2020-04-07 13:45:30.777451 ] WebMaster            > createBrowser        : start
[ 2020-04-07 13:45:35.898718 ] WebMaster            > createBrowser        : end
[ 2020-04-07 13:45:35.900717 ] WebMaster            > initWebsiteManager   : start
[ 2020-04-07 13:45:35.903714 ] WebMaster            > initWebsiteManager   : Only Portal
[ 2020-04-07 13:45:35.905714 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:35.908712 ] WebMaster            > createWebsiteManager : start
[ 2020-04-07 13:45:35.911709 ] WebMaster            > createWebsiteManager : Portal
[ 2020-04-07 13:45:35.914708 ] PortalManager        > __init__             : finish super init
[ 2020-04-07 13:45:35.911709 ] WebMaster            > createWebsiteManager : Portal
[ 2020-04-07 13:45:35.914708 ] PortalManager        > __init__             : finish super init
[ 2020-04-07 13:45:35.918705 ] PortalManager        > __init__             : finish website init
[ 2020-04-07 13:45:35.921703 ] PortalManager        > start                : start
[ 2020-04-07 13:45:35.925720 ] Portal               > start                : start
[ 2020-04-07 13:45:39.976392 ] Portal               > login                : start
[ 2020-04-07 13:45:42.256177 ] Portal               > login                : end
[ 2020-04-07 13:45:42.264172 ] Portal               > start                : end
[ 2020-04-07 13:45:42.269170 ] PortalManager        > start                : end
[ 2020-04-07 13:45:42.272167 ] WebMaster            > createWebsiteManager : end
[ 2020-04-07 13:45:42.282161 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:42.285159 ] WebMaster            > initWebsiteManager   : end
[ 2020-04-07 13:45:42.294155 ] WebMaster            > initThread           : start
[ 2020-04-07 13:45:42.297152 ] WebMaster            > initThread           : end
[ 2020-04-07 13:45:42.297152 ] WebMaster            > stayAlive            : start
[ 2020-04-07 13:45:42.300149 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:42.309145 ] WebMaster            > createWebsiteManager : start
[ 2020-04-07 13:45:42.312143 ] WebMaster            > createWebsiteManager : Moodle
[ 2020-04-07 13:45:42.322136 ] MoodleManager        > __init__             : finish super init
[ 2020-04-07 13:45:42.326133 ] MoodleManager        > __init__             : finish website init
[ 2020-04-07 13:45:42.337129 ] MoodleManager        > start                : start
[ 2020-04-07 13:45:42.351119 ] Moodle               > start                : start
[ 2020-04-07 13:45:46.666096 ] Moodle               > login                : start
[ 2020-04-07 13:45:50.061960 ] Moodle               > login                : branch
[ 2020-04-07 13:45:50.100931 ] Moodle               > login                : end case 1
[ 2020-04-07 13:45:50.117921 ] Moodle               > getSiteMap           : start
[ 2020-04-07 13:45:50.966673 ] Moodle               > getSiteMap           : find box
[ 2020-04-07 13:45:50.970668 ] Moodle               > getSiteMap           : end
[ 2020-04-07 13:45:50.979663 ] Moodle               > start                : end
[ 2020-04-07 13:45:50.987659 ] MoodleManager        > start                : end
[ 2020-04-07 13:45:50.990657 ] WebMaster            > createWebsiteManager : end
[ 2020-04-07 13:45:50.993656 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:51.001649 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:51.004647 ] MoodleManager        > scrape               : call function
[ 2020-04-07 13:45:51.009645 ] Moodle               > getSiteMap           : start
[ 2020-04-07 13:45:51.929194 ] Moodle               > getSiteMap           : find box
[ 2020-04-07 13:45:51.934191 ] Moodle               > getSiteMap           : end
[ 2020-04-07 13:45:51.942184 ] MoodleManager        > scrape               : end
[ 2020-04-07 13:45:51.946183 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:51.949488 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:51.951498 ] WebMaster            > test                 : hello world
[ 2020-04-07 13:45:51.954067 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:51.956068 ] WebMaster            > terminateThread      : start
[ 2020-04-07 13:45:51.956068 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:51.963065 ] PortalManager        > refresh              : start
[ 2020-04-07 13:45:51.967061 ] Portal               > keepAlive            : start
[ 2020-04-07 13:45:52.522739 ] Portal               > keepAlive            : end
[ 2020-04-07 13:45:52.526737 ] PortalManager        > refresh              : end
[ 2020-04-07 13:45:52.536730 ] MoodleManager        > refresh              : start
[ 2020-04-07 13:45:52.540727 ] Moodle               > keepAlive            : start
[ 2020-04-07 13:45:53.346493 ] Moodle               > keepAlive            : end
[ 2020-04-07 13:45:53.351490 ] MoodleManager        > refresh              : end
[ 2020-04-07 13:45:53.360484 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:53.363481 ] WebMaster            > stayAlive            : end
[ 2020-04-07 13:45:53.366480 ] WebMaster            > terminateThread      : end
[ 2020-04-07 13:45:53.368479 ] WebMaster            > __del__              : start
[ 2020-04-07 13:45:53.375474 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:53.378473 ] WebMaster            > deleteWebsiteManager : start
[ 2020-04-07 13:45:53.380472 ] PortalManager        > destroy              : start
[ 2020-04-07 13:45:53.389465 ] Portal               > destroy              : start
[ 2020-04-07 13:45:53.404458 ] Portal               > logout               : start
[ 2020-04-07 13:45:54.061077 ] Portal               > logout               : end
[ 2020-04-07 13:45:54.114045 ] Portal               > destroy              : end
[ 2020-04-07 13:45:54.118043 ] PortalManager        > destroy              : end
[ 2020-04-07 13:45:54.121040 ] WebMaster            > deleteWebsiteManager : end
[ 2020-04-07 13:45:54.123038 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:54.125037 ] WebMaster            > wrapper              : start
[ 2020-04-07 13:45:54.128037 ] WebMaster            > deleteWebsiteManager : start
[ 2020-04-07 13:45:54.136031 ] MoodleManager        > destroy              : start
[ 2020-04-07 13:45:54.139029 ] Moodle               > destroy              : start
[ 2020-04-07 13:45:54.155020 ] Moodle               > logout               : start
[ 2020-04-07 13:45:55.539275 ] Moodle               > logout               : end
[ 2020-04-07 13:45:55.561260 ] Moodle               > destroy              : end
[ 2020-04-07 13:45:55.564259 ] MoodleManager        > destroy              : end
[ 2020-04-07 13:45:55.567257 ] WebMaster            > deleteWebsiteManager : end
[ 2020-04-07 13:45:55.577251 ] WebMaster            > wrapper              : end
[ 2020-04-07 13:45:57.653775 ] WebMaster            > __del__              : end
```

Any error thrown is considered as failed.  

