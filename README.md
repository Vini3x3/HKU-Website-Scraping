# Pythonic and Structural Upgrade

In order to make things more pythonic, this version adopts PEP-8 standards.   

To make things better and more maintainable, there are 2 points to be upgraded in this version: 

- `webmaster.py` : extend from`thread.timer` instead of containing a thread
- `HKUSites.py`: use decorator for probing and caching

To make it easier to understand the restructure of `webmaster.py`, below is the skeleton / simplified version: 

```python
import time
import threading


class RepeatingTimer(threading.Timer):
    def __init__(self, interval, function=None, *args, **kwargs):
        super().__init__(interval, function, *args, **kwargs)
        self.function = self.core_function
        self.lock = threading.Lock()
        self.resource = 'resource'

    def atomic(function):
        def wrapper(self, *args, **kwargs):
            self.lock.acquire()
            result = function(self, *args, **kwargs)
            self.lock.release()
            return result
        return wrapper

    @atomic
    def core_function(self):
        print('core_function with {}'.format(self.resource))

    @atomic
    def external_function(self, msg):
        print('external_function with {}'.format(self.resource))
        print(msg)

    def run(self):
        while not self.finished.is_set():
            self.function()
            self.finished.wait(self.interval)

if __name__ == '__main__':
    t = RepeatingTimer(3)
    t.start()
    time.sleep(3)
    t.external_function('hello world')
    time.sleep(4)
    t.cancel()
```

the result is as following: 

```
D:\jupyterbook\Notification\main>python testground.py
core_function with resource
external_function with resource
hello world
core_function with resource
core_function with resource
```

This shows that the extension can simplify the design of `webmaster` and `notemaster`.  



