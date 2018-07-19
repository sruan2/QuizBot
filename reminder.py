from threading import Timer
import message
from time import *
from utils import *

class RepeatedTimer(object):
    def __init__(self, offset, interval, function, *args, **kwargs):
        self.offset     = offset
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self._timer     = None
        self._offset_timer = None
        self.offset_time()

    def offset_time(self):
        pretty_print('Reminder offsets at ' + strftime("%Y-%m-%d %H:%M:%S", localtime()), mode='Reminder')
        self._offset_timer = Timer(self.offset, self.offset_run)
        self._offset_timer.start()

    def offset_run(self):
        self.function(*self.args, **self.kwargs)
        self.start()

    def _run(self):
        self.function(*self.args, **self.kwargs)
        self.stop()
        self.start()

    def start(self):
        pretty_print('RepeatedTimer starts', mode='Reminder')
        self._timer = Timer(self.interval, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()
