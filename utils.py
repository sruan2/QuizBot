import os
import sys

class EnoughQuestions(Exception):
   """Base class for other exceptions"""
   pass

def pretty_print(message, mode=None):
    if not mode:
        print('\t\t\t  '+str(message))
    else:
        print('[{}] {:9s}: {}'.format(os.getpid(), mode, str(message)))


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


def update_cache(cache, sender_id, firstname=None, current_qid=None, current_subject=None, begin_uid=None, waiting_for_answer=None, if_explanation_text=None, last_payload=None):
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

    if if_explanation_text != None:
        cache[sender_id]["if_explanation_text"] = if_explanation_text

    if last_payload != None:
        cache[sender_id]["last_payload"] = last_payload
