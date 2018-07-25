import os
import sys


def pretty_print(message, mode=None):
    if not mode:
        print('\t\t\t  '+str(message))
    else:
        print('[{}] {:9s}: {}'.format(os.getpid(), mode, str(message)))


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


def update_cache(cache, sender_id, firstname=None, current_qid=None, current_subject=None, begin_uid=None, waiting_for_answer=None):
    if firstname != None:
        cache[sender_id]["firstname"] = firstname

    if current_qid != None:
        cache[sender_id]["current_qid"] = current_qid

    if current_subject != None:
        cache[sender_id]["current_subject"] = current_subject

    if begin_uid != None:
        cache[sender_id]["begin_uid"] = begin_uid

    if waiting_for_answer != None:
        cache[sender_id]["waiting_for_answer"] = waiting_for_answer
