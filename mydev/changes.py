from myscraper.webmanager import *

class MoodleManager(BasicMoodleManager):
    pass
    
class PortalManager(BasicPortalManager):
    pass

def SiteManager(credential, webscrape_settings):
        manager_list = ['Moodle','Portal']
        if not webscrape_settings:
            raise weberror.CallError(2)
        elif not isinstance(webscrape_settings, dict):
            raise weberror.CallError(3)
        elif 'site' not in webscrape_settings.keys():
            raise weberror.CallError(4)
        elif webscrape_settings['site'] not in manager_list:
            raise weberror.CallError(3)
        else:
            klass = globals()[webscrape_settings['site']+'Manager']
            return klass(credential, webscrape_settings)

# def SiteManager(credential, webscrape_settings):
#     browser_list = ['Chrome', 'Firefox', 'Edge']
#     if webscrape_settings == None:
#         raise weberror.CallError(1)
#     elif not isinstance(webscrape_settings, dict):
#         raise weberror.CallError(3)
#     elif 'browser' not in webscrape_settings.keys():
#         raise weberror.CallError(4)
#     elif webscrape_settings['browser'] not in browser_list:
#         raise weberror.CallError(3)
#     else:
#         klass = globals()['New' + webscrape_settings['browser']]
#         return klass(webscrape_settings)      