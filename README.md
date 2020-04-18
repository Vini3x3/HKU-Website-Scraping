# Webmaster

Use a master program to manage the `Website` instance.  

Below techniques are involved in this manager: 

- Indirect control - call method of instance by name, check callable methods in instance
- Multithreading - `keepAlive()` for every 3 minutes
- Detect `last-modified` - check for last update of webpage
- Caching - cache for unmodified and searched result
- Tracking - track for user behaviour

On top of that, there is a guarantee of all the `Website` instance have the same set of base class method.  

On the other hand, more utility methods are implemented in `Website` class to reduce the import library in higher-level files: 

- `WaitUntil()` - implement  `selenium.webdriver.support.ui import WebDriverWait`, `from selenium.webdriver.support import expected_conditions as EC` and `from selenium.webdriver.common.by import By as BY`

Therefore, the import library should be like this: 

| Class File         | Library                                                      |
| ------------------ | ------------------------------------------------------------ |
| Website            | from bs4 import BeautifulSoup as bs                          |
|                    | from selenium import webdriver                               |
|                    | from selenium.webdriver.support.ui import WebDriverWait      |
|                    | from selenium.webdriver.support import expected_conditions as EC |
|                    | from selenium.webdriver.common.by import By as BY            |
|                    | from seleniumrequests import Firefox                         |
|                    | from seleniumrequests import Chrome                          |
| Derives of Website | from bs4 import BeautifulSoup as bs                          |
|                    | import website                                               |
|                    | import traceback                                             |
| Webmaster          | import Portal, Moodle, Library, ...                          |
|                    | import traceback                                             |



