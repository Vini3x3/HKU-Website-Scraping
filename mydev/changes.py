from myscraper.webmanager import *

import cachetools

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

class MoodleManager(BasicMoodleManager):    
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """
       
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """
    def __init___(self, credential, webscrape_settings):
        super().__init__(credential, webscrape_settings)
        self.contenttype = {
            '/help.php'                     : 'help',
            '/pluginfile.php'               : 'force_download',

            '/grade/report/index.php'       : 'grade',
            '/course/view.php'              : 'course',
            '/user/index.php'               : 'contact',
            '/user/view.php'                : 'user',
            '/mod/resource/view.php'        : 'resource',
            '/mod/assign/view.php'          : 'submit_file_upload',
            '/mod/turnitintooltwo/view.php' : 'submit_turnitin',
            '/mod/url/view.php'             : 'url',
            '/mod/page/view.php'            : 'page',
            '/mod/forum/view.php'           : 'forum',
            '/mod/forum/discuss.php'        : 'discussion',
            '/mod/quiz/view.php'            : 'quiz',   
            '/mod/folder/view.php'          : 'folder',
            '/mod/questionnaire/view.php'   : 'questionnaire',
            '/mod/choice/view.php'          : 'choice',     
            '/mod/choicegroup/view.php'     : 'choicegroup',
            '/mod/lti/view.php'             : 'lti',
            '/mod/feedback/view.php'        : 'feedback',
            '/mod/vpl/view.php'             : 'vpl',

            '/my/'                          : 'submission_deadlines',
        }
        
    
class PortalManager(BasicPortalManager):
    """
    -------------------------------------
    | To be add into base template      |
    -------------------------------------
    """ 
    
    """
    -------------------------------------
    | Extensions                        |
    -------------------------------------
    """




