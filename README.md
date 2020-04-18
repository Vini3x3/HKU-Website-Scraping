# Component  and Structural Upgrade

##  Cross site Cookies

To take advantage of the cross-site login, two approaches are drafted: 

- Open new tab in browser to reuse the cookies
- Share cookies among browser

The first approach is under test and succeeded.  

## Structural Upgrade

Apart from making the functions complete, it is possible to separate the functions into 3 components to avoid god-class, especially for only Moodle: 

- Trace function call
- Cache management
- Refresh periodically
- Switch tab

Note that the four components are separated between hierarchy: 

- Browser level: incorporate the switch tab function
- Website level: has a component for cache management
- Webmaster level: has a structure for tracing function call and refresh periodically


## Accident

However, the selenium-request is only workable with firefox, thus a big hinder to the loading speed.  Therefore, this version is abandoned, even though all of the code is working in firefox.  

Neither Requestium is considered, as it only works in Chrome, and on top of that, it does not show how it will be faster.  

Besides, the structure is too complicated that we need another structural upgrade.  The 3 level structure if further breakdown into 4 levels.  