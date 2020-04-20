from time import time
from traceback import print_exc

# frameinfo = getframeinfo(currentframe())

# print(frameinfo.filename, frameinfo.lineno)

"""testsuit1"""
"""Extend the class to perform the test"""

class testsuit:
    """Util Functions"""
    def __init__(self):
        self.formatstyle = {
            'field'     : '======Test for {:19}======',
            'test'      : '------Test {:2}: {:19}------',
            'warn'      : '------Warn {:2}: {:19}------',
            'log'       : '------Log :{:23}------',
            'report'    : '======Report for {:17}======',
            'result'    : '|{:19}:{:18}|',
            'slimsep'   : '-'*40,
            'doublesep' : '='*40,
        }
    
    def test(self, *args):
        try:
            self.testground(*args)
        except:        
            self.errorhandler(*args)
        finally:
            self.endtest(*args)

    def compileTest(self, *args):
        try:
            self.testground(*args)
        except:
            return False
        return True
    
    def timedTest(self, *args, repeat=1):
        try:
            start_time = time()
            for _ in range(repeat):
                self.testground(*args)
            end_time = time()
        except:
            return -1
        return end_time - start_time

    def log(self, formattype, *args):
        if formattype in self.formatstyle.keys():
            print(self.formatstyle[formattype].format(*args))

    """Open For Extension"""
    def testground(self, *args):
        pass

    def errorhandler(self, *args):
        pass

    def endtest(self, *args):
        pass

"""testsuit2"""
"""Just construct the object and pass function as argument to test"""

class testsuit2:
    """Util Functions"""
    def __init__(self):
        self.formatstyle = {
            'field'     : '======Test for {:19}======',
            'test'      : '------Test {:2}: {:19}------',
            'warn'      : '------Warn {:2}: {:19}------',
            'log'       : '------Log :{:23}------',
            'report'    : '======Report for {:17}======',
            'result'    : '|{:19}:{:18}|',
            'slimsep'   : '-'*40,
            'doublesep' : '='*40,
        }
    
    def test(self, *args, testground, errorhandler, endtest):
        try:
            testground(*args)
        except:        
            errorhandler(*args)
        finally:
            endtest(*args)
    
    def compileTest(self, *args, testground):
        try:
            testground(*args)
        except:
            return False
        return True
    
    def timedTest(self, *args, repeat=1, testground):
        try:
            start_time = time()
            for _ in range(repeat):
                testground(*args)
            end_time = time()
        except:
            return -1
        return end_time - start_time

    def log(self, formattype, *args):
        if formattype in self.formatstyle.keys():
            print(self.formatstyle[formattype].format(*args))

"""testsuit3"""
"""Use decorator to test"""

def compileTest(func, *args):
    def wrapper(*args):
        try:
            func(*args)
        except:   
            return False        
        return True        
    return wrapper
def timedTest(repeat=1):
    def real_decorator(function):
        def wrapper(*args):
            try:
                start_time = time()
                for _ in range(repeat):
                    function(*args)
                end_time = time()
            except:
                return -1            
            return end_time - start_time
        return wrapper
    return real_decorator
def errorTest(func, *args):
    def wrapper(*args):
        try:
            func(*args)
        except:   
            print_exc()
    return wrapper
def log(formattype, tab=None, msg=None):
    def real_decorator(function):
        def wrapper(*args):
            formatstyle = {
                'field'     : '======Test for {:19}======',
                'test'      : '------Test {:2}: {:19}------',
                'warn'      : '------Warn {:2}: {:19}------',
                'log'       : '------Log :{:23}------',
                'report'    : '======Report for {:17}======',
                'result'    : '|{:19}:{:18}|',
                'slimsep'   : '-'*40,
                'doublesep' : '='*40,
            }
            if formattype in formatstyle.keys():
                print(formatstyle[formattype].format(tab, msg))
            return function(*args)
        return wrapper
    return real_decorator

def test(testground, errorhandler, endtest, *args):
    def wrapper(errorhandler, endtest, *args):
        try:
            testground(*args)
        except:            
            errorhandler(*args)
        finally:
            endtest(*args)
    return wrapper
def printlog(formattype, tab=None, msg=None):
    formatstyle = {
        'field'     : '======Test for {:19}======',
        'test'      : '------Test {:2}: {:19}------',
        'warn'      : '------Warn {:2}: {:19}------',
        'log'       : '------Log :{:23}------',
        'report'    : '======Report for {:17}======',
        'result'    : '|{:19}:{:18}|',
        'slimsep'   : '-'*40,
        'doublesep' : '='*40,
    }
    if formattype in formatstyle.keys():
        print(formatstyle[formattype].format(tab, msg))
def defaultpass(*args):
    pass

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def test(self):
        returns = self.inittest()
        if isinstance(returns, tuple):
            argument = list(returns)
        elif returns == None:
            argument = None
        else:
            argument = returns
        try:
            data = self.testground(argument)
            if data != None:                
                self.validate(data)
        except:
            self.errorhandler(argument)
        finally:
            self.endtest(argument)

testsuit3 = dotdict({
    # decorators
    'compileTest': compileTest,
    'timedTest': timedTest,
    'errorTest': errorTest,
    'log': log,    
    # attr functions
    'inittest': defaultpass,
    'testground': defaultpass,
    'errorhandler': defaultpass,
    'validate': defaultpass,
    'endtest': defaultpass,
    # direct fucntions
    'printlog': printlog,
})
