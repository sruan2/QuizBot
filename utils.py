import os

def pretty_print(message, mode):
    if not mode:
        print('\t\t\t\t'+message)
    else:
        print('[{}] pid {}: {}'.format(mode, os.getpid(), message))
