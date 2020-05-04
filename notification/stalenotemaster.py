from notification import HKUNotifier
from time import time, sleep
import inspect
from datetime import datetime


class NoteMaster:
    """
    -------------------------------------
    | Object Basics                     |
    -------------------------------------
    """
    def __init__(self, webmaster, verbose=0):
        # settings
        self.notifiers = []
        self.notices = []
        self.start_time = 0

        # copy arguments
        self.verbose = verbose

        # initialize
        self.add_default_notifiers(webmaster)
        self.start_time = time()

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def print_debug(self, msg):
        if self.verbose > 0: print('[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))

    def debug(function):
        def wrapper(self, *args, **kwargs):
            if self.verbose > 0: print(
                '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, function.__name__, 'begin')
            )
            result = function(self, *args, **kwargs)
            if self.verbose > 0: print(
                '[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, function.__name__, 'end')
            )
            return result
        return wrapper

    # additional function for non-threading
    @debug
    def check(self, webmaster):
        if self.has_notice():
            return self.handle_notice()
        else:
            return []

    @debug
    def add_notifier(self, notifier_strategy, webmaster, delay=0, range=600):
        self.print_debug(notifier_strategy + str(delay) + str(range))
        self.notices.extend(getattr(HKUNotifier, notifier_strategy)(webmaster, delay=delay, range=range))

    @debug
    def clear_notice(self):
        self.notices.clear()

    @debug
    def has_notice(self):
        # print(self.notices)
        return len(self.notices) > 0

    @debug
    def handle_notice(self):
        self.print_debug(len(self.notices))
        alarms = []
        for notice in self.notices:
            if notice['type'] == 'relative':
                if notice['delay'] > time() - self.start_time > notice['delay'] - notice['range'] or notice['delay'] < time() - self.start_time:
                    alarms.append(notice)
            elif notice['type'] == 'absolute':
                if notice['time'] > time() > notice['time'] - notice['range']:
                    alarms.append(notice)
        for alarm in alarms:
            # print(alarm['msg'])
            self.notices.remove(alarm)
        return alarms


    """
    -------------------------------------
    | Application                       |
    -------------------------------------
    """

    @debug
    def add_default_notifiers(self, webmaster):
        list_of_notifiers = [
            ['moodle_deadline_strategy', 0, 600],
            ['portal_next_lesson_strategy', 0, 600],
            ['portal_get_invoice_strategy', 600, 600],
        ]
        for row in list_of_notifiers:
            self.add_notifier(row[0], webmaster, delay=row[1], range=row[2])

