from time import time

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
