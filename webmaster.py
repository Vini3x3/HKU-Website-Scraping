import traceback
import time
import inspect
import csv
import threading

import moodle
import portal
import library
import weberror


"""
What I want to do in webmaster:

- Mode: Initialize all websites, on demand or only login Portal to serve as a basic login? 
- Track: Store the history of calling which function and what arguement, and export / store as a txt / csv file as a result.  
- Cache: Cache called result and reuse when necessary
- Predict: Predict user behaviour by caching new possible commands

In order to incorporate with the new design, the website instance also need to be updated: 
- Common cache: which is for local cache ( website instance cache ), which is for common cache? 
- Load cache: which is loading the cache, which is from new scrape cache? 

LinkCache: expire time, course_id, type, local_id

webscrape_settings = {    
    'browser': 'FireFox',
    'headless': True,
    'debug': False,
    'initialize-website': 'On Demand',
}

initialize-website: 'On Demand', 'Only Portal', 'All'


"""

class WebMaster:
    def __init__(self, credential, websettings):
        
        # storage
        self.credential = credential
        self.websettings = websettings
        self.debug = websettings['debug']
        self.websites = {}
        self.threads = []
        self.record = []
        self.cache = {}
        self.control = {}
        
        # initialization
        self.websites['Portal'] = portal.Portal(credential, websettings)
        self.websites['Library'] = library.Library(credential, websettings)
        self.websites['Moodle'] = moodle.Moodle(credential, websettings)
        
        if self.websettings['initialize-website'] == 'All':
            self.websites['Portal'] = portal.Portal(credential, websettings)
            self.websites['Library'] = library.Library(credential, websettings)
            self.websites['Moodle'] = moodle.Moodle(credential, websettings)
        elif self.websettings['initialize-website'] == 'Only Portal':
            self.websites['Portal'] = portal.Portal(credential, websettings)
        elif self.websettings['initialize-website'] == 'On Demand':
            pass
        else:
            self.websites['Portal'] = portal.Portal(credential, websettings)
            self.websites['Library'] = library.Library(credential, websettings)
            self.websites['Moodle'] = moodle.Moodle(credential, websettings)

        self.collectMethods()
        self.record.append([time.time(), type(self).__name__, '__init__'])
        if self.debug: print('webmaster born')

        # multithreading for stayAlive
        self.mutex = threading.Lock()
        self.terminate_flag = threading.Event()        
        self.keepAliveThread = threading.Thread(target=self.stayAlive)
        self.keepAliveThread.start()

    def __del__(self):        
        self.keepAliveThread.should_abort_immediately=True
        self.keepAliveThread.join()
        if self.debug: print('joint')
        self.record.append([time.time(), type(self).__name__, '__del__'])
        with open('webmaster.csv', 'w', newline='\n') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)            
            for row in self.record:                
                wr.writerow(row)
            myfile.close()
        for each in self.websites:
            del each
        self.cache.clear()
        self.record.clear()
        if self.debug: print('webmaster dead')

    def __str__(self):
        return 'This is a WebMaster instance'

    def wait(self):
        print('waiting')
        time.sleep(10)

    def terminate_thread(self):
        self.terminate_flag.set()
        self.keepAliveThread.join()    
        if self.debug: print('thread ended')
    
    def printMethods(self):
        for key,value in self.control.items():
            print(key,value)

    def createWebsite(self, class_name):
        if class_name == 'Portal':
            self.websites[class_name] = portal.Portal(self.credential, self.websettings)
        elif class_name == 'Moodle':
            self.websites[class_name] = moodle.Moodle(self.credential, self.websettings)
        else:
            self.websites[class_name] = library.Library(self.credential, self.websettings)

    def stayAlive(self):        
        while not self.terminate_flag.is_set():
            self.mutex.acquire()
            for each in self.websites.values():
                each.keepAlive()
            self.mutex.release()
            if self.debug: print('refreshed')
            time.sleep(60)
        
    def executeMethod(self, class_name, method_name, argv):
        if self.debug: print(class_name, method_name, argv)
        if class_name not in self.websites:
            self.createWebsite(class_name)
        func = getattr(self.websites[class_name], method_name)
        # print(len(inspect.signature(func).parameters))
        if len(inspect.signature(func).parameters) == 1:
            if argv!=None:
                result = func(argv)
            else:
                # return 'Arguement Error: require arguement'
                raise(weberror.CallError(2))
        else:
            result = func()
        self.record.append([time.time(), class_name, method_name])
        return result

    def callMethod(self, method_name, argv=None, class_name=''):
        self.mutex.acquire()        

        if self.debug: print(method_name, argv, class_name)

        if method_name in self.control and class_name in self.control[method_name]:
            result = self.executeMethod(class_name, method_name, argv)
            self.mutex.release()
            return result
        else:
            if method_name not in self.control:
                self.mutex.release()
                raise(weberror.CallError(0))
                # return 'Call Error: No such function'
            elif len(self.control[method_name]) != 1:                
                self.mutex.release()
                raise(weberror.CallError(1))
                # return 'Call Error: Ambigious Function Call'                
            else:
                result = self.executeMethod(self.control[method_name][0], method_name, argv)                
                self.mutex.release()
                return result

    def collectMethods(self):
        
        websiteMethodsList = [func for func in dir(moodle.Moodle) if callable(getattr(moodle.Moodle, func))]
        websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]        
        for each in websiteMethodsList:
            if each in self.control:
                self.control[each].append('Moodle')
            else:
                self.control[each] = ['Moodle']
        
        websiteMethodsList = [func for func in dir(portal.Portal) if callable(getattr(portal.Portal, func))]
        websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
        for each in websiteMethodsList:
            if each in self.control:
                self.control[each].append('Portal')
            else:
                self.control[each] = ['Portal']        

        websiteMethodsList = [func for func in dir(library.Library) if callable(getattr(library.Library, func))]
        websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
        for each in websiteMethodsList:
            if each in self.control:
                self.control[each].append('Library')
            else:
                self.control[each] = ['Library']
    
    def moodle_getSiteMap(self):
        sitelinks = self.callMethod('getSiteMap2',class_name='Moodle')
        # for _ in sitelinks:
        #     print(_)
        cache_links = self.callMethod('minimizeStorageInt',sitelinks,class_name='Moodle')
        for _ in cache_links:
            print(_)
        new_dict = {}
        for _ in cache_links:
            new_dict[_[2]] = []
        self.cache['Moodle'] = new_dict    
    
    def moodle_getCourseContent(self, course_id):
        for row in self.cache['Moodle'].keys():
            if row == course_id:
                course_url = self.callMethod('getLink',['abc','course',row],class_name='Moodle')
                content = self.callMethod('parseCourseHTML',course_url,class_name='Moodle')
                self.cache['Moodle'][course_id] = []
                self.cache['Moodle'][course_id] += self.callMethod('minimizeStorageInt',content,class_name='Moodle')
                self.cache['Moodle'][course_id] += self.callMethod('minimizeStorageStr',content,class_name='Moodle')
                return self.moodle_getCacheCourse(course_id)
        raise weberror.CallError(3)

    def moodle_getCacheCourse(self, course_id):
        return self.cache['Moodle'][course_id]

    def moodle_getContentType(self, course_id, content_type):
        if course_id not in self.cache['Moodle'].keys():
            raise weberror.CallError(3)
        else:
            result = []
            if len(self.cache['Moodle'][course_id]) <= 0:
                self.moodle_getCourseContent(course_id)
            for row in self.cache['Moodle'][course_id]:
                if row[1] == content_type:
                    result.append(row)
            return result

        # sitelinks = A.getSiteMap2()
        # cache_links = A.minimizeStorageInt(sitelinks)



    # def callMethod(self, method_name, argv=None, class_name=''):
    #     if class_name in self.control and method_name in self.control[class_name]:
    #         return self.executeMethod(class_name, method_name, argv)
    #     else:
    #         # check if the method is unique
    #         count = 0
    #         corresponding_class = ''
    #         for class_name, func_list in self.control.items():
    #             if method_name in func_list:
    #                 count += 1
    #                 corresponding_class = class_name  
    #         if count > 1:
    #             return 'Arguement Error: ambigious function call'
    #         elif count == 0:
    #             return 'Arguement Error: no such function'
    #         else:
    #             return self.executeMethod(corresponding_class, method_name, argv)
                
    # def collectMethods(self):
    #     websiteMethodsList = [func for func in dir(moodle.Moodle) if callable(getattr(moodle.Moodle, func))]
    #     websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
    #     self.control['Moodle'] = websiteMethodsList
    #     websiteMethodsList = [func for func in dir(portal.Portal) if callable(getattr(portal.Portal, func))]
    #     websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
    #     self.control['Portal'] = websiteMethodsList
    #     websiteMethodsList = [func for func in dir(library.Library) if callable(getattr(library.Library, func))]
    #     websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
    #     self.control['Library'] = websiteMethodsList
        
        # for each in self.websites.values():
        #     websiteMethodsList = [method_name for method_name in dir(each) if callable(getattr(each, method_name))]
        #     websiteMethodsList = [method_name for method_name in websiteMethodsList if method_name[0:2] != '__' and method_name[0:5] != 'util_' ]
        #     self.control[type(each).__name__] = websiteMethodsList