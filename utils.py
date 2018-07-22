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
