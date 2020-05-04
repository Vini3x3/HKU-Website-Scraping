from notification import HKUNotifier
from time import time, sleep
import inspect
import threading
from datetime import datetime


class NoteMaster(threading.Timer):
    """
    -------------------------------------
    | Thread Basics                     |
    -------------------------------------
    """
    def __init__(self, interval=600, function=None, verbose=0):
        super().__init__(interval, function)
        self.function = self.core_function
        self.start_time = 0

        # settings
        self.notifiers = []
        self.notices = []

        # copy arguments
        self.verbose = verbose

    def start(self, webmaster):
        self.start_time = time()
        self.add_default_notifiers(webmaster)
        super().start()

    def run(self):
        while not self.finished.is_set():
            self.function()
            self.finished.wait(self.interval)

    """
    -------------------------------------
    | Core Development                  |
    -------------------------------------
    """

    def core_function(self):
        self.print_debug('begin')
        if self.has_notice():
            self.handle_notice()
        self.print_debug('end')

    def print_debug(self, msg):
        if self.verbose > 0: print('[ {} ] {:20} > {:20} : {}'.format(datetime.now(), self.__class__.__name__, inspect.stack()[1][3], msg))

    def add_notifier(self, notifier_strategy, webmaster, delay=0, range=600):
        self.print_debug('begin')
        self.print_debug(notifier_strategy + str(delay) + str(range))
        self.notices.extend(getattr(HKUNotifier, notifier_strategy)(webmaster, delay=delay, range=range))
        self.print_debug('end')

    def clear_notice(self):
        self.notices.clear()

    def has_notice(self):
        print(self.notices)
        return len(self.notices) > 0

    def handle_notice(self):
        self.print_debug('begin')
        self.print_debug(len(self.notices))
        alarms = []
        for notice in self.notices:
            if notice['type'] == 'relative':
                if notice['delay'] < time() - self.start_time < notice['delay'] + notice['range']:
                    alarms.append(notice)
            elif notice['type'] == 'absolute':
                if notice['time'] < time() < notice['time'] + notice['range']:
                    alarms.append(notice)
        for alarm in alarms:
            print(alarm['msg'])
            self.notices.remove(alarm)
        self.print_debug('end')

    """
    -------------------------------------
    | Application                       |
    -------------------------------------
    """

    def add_default_notifiers(self, webmaster):
        list_of_notifiers = [
            ['moodle_deadline_strategy', 0, 600],
            ['portal_next_lesson_strategy', 0, 600],
            ['portal_get_invoice_strategy', 600, 600],
        ]
        for row in list_of_notifiers:
            self.add_notifier(row[0], webmaster, delay=row[1], range=row[2])

