from threading import Timer
from message import *
from time import *
from datetime import datetime
from utils import *
from database import show_users_newly_added

class RepeatedTimer(object):
    def __init__(self, interval, template_conversation, mysql):
        self.offset = self.get_offset_time(20, 00, 00)
        self.interval = interval
        self.mysql = mysql
        self.is_running = False
        self._timer = None
        self._offset_timer = None
        self.reminder = Reminder(template_conversation, mysql)
        self.offset_time()

    def offset_time(self):
        pretty_print('Reminder offsets at ' +
                     strftime("%Y-%m-%d %H:%M:%S", localtime()), mode='Reminder')
        self._offset_timer = Timer(self.offset, self.offset_run)
        self._offset_timer.start()

    def offset_run(self):
        active_list = show_users_newly_added(self.mysql)
        self.reminder.send_reminder(active_list)
        self.start()

    def _run(self):
        active_list = show_users_newly_added(self.mysql)
        self.reminder.send_reminder(active_list)
        self.stop()
        self.start()

    def start(self):
        pretty_print('RepeatedTimer starts', mode='Reminder')
        self._timer = Timer(self.interval, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()

    def get_offset_time(self, hour, minute, second):
        FMT = "%Y-%m-%d %H:%M:%S"
        cur_time = localtime()

        _year = cur_time.tm_year
        _mon = cur_time.tm_mon
        _mday = cur_time.tm_mday
        _hour = hour
        _min = minute
        _sec = second
        _wday = cur_time.tm_wday
        _yday = cur_time.tm_yday
        _isdst = cur_time.tm_isdst

        cur_time = strftime(FMT, cur_time)
        offset_time = strftime(FMT, (_year, _mon, _mday, _hour, _min, _sec, _wday, _yday, _isdst))
        tdelta = datetime.strptime(offset_time, FMT) - datetime.strptime(cur_time, FMT)

        return tdelta.seconds


class Reminder(object):
    def __init__(self, template_conversation, mysql):
        self.users = {}
        self.template_conversation = template_conversation
        self.mysql = mysql

    def send_reminder(self, user_list):
        '''
            This function sends a reminder to the specified recipient.
                Args:
                    list: a list of user ids to which the reminder is sent

                Returns:
                    None
        '''
        for recipient_id, user_name in user_list:
            if recipient_id not in self.users:
                self.users[recipient_id] = 0
            if self.users[recipient_id] < 7:
                self.users[recipient_id] += 1
                send_format_quick_reply_text(self.mysql, recipient_id, self.template_conversation, "REMINDER", user_name)
                print("[QUIZBOT] PID " + str(os.getpid())+": Sent Reminder To " + str(user_name) +
                      " With ID " + str(recipient_id) + " At " + strftime("%Y-%m-%d %H:%M:%S", localtime()))
