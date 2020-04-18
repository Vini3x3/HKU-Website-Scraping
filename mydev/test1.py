from functools import lru_cache
import functools
import threading
# class A:    
#     @lru_cache(5)
#     def foo(self):
#         print('Executing foo...')
#     def bar(self):
#         self.foo.cache_clear()

# a = A()
# a.foo()
# a.foo()
# a.bar()
# a.foo()

import cachetools

class A:
    def __init__(self):        
        self.mycache = cachetools.LRUCache(maxsize=32)
        self.mylock = threading.RLock()
    
    def browsercache(key=cachetools.keys.hashkey):
        def decorator(function):
            def wrapper(self, browser, *args):  
                tempKey = key(function.__name__, *args)
                templock = self.mylock
                if tempKey not in self.mycache:
                    try:
                        if templock:
                            with templock:
                                self.mycache[tempKey] = function(self, browser, *args)
                        else:
                            self.mycache[tempKey] = function(self, browser, *args)
                    except ValueError:
                        pass  # value too large                    
                return self.mycache[tempKey]
            return wrapper
        return decorator
    
    @browsercache(key=cachetools.keys.hashkey)    
    def foo(self, browser):
        print('Executing foo...')
    def bar(self):        
        self.mycache.clear()
    # def info(self):
    #     for _ in [method_name for method_name in dir(self.foo) if callable(getattr(self.foo, method_name))]:
    #         print(_)
    

a = A()
a.foo('B')
a.foo('B')
a.bar()
a.foo('B')
