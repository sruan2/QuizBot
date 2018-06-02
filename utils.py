import os

def pretty_print(message, mode=None):
    if not mode:
        print('\t\t\t  '+message)
    else:
        print('[{}] pid {}: {}'.format(mode, os.getpid(), message))
