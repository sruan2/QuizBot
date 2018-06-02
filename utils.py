import os

def pretty_print(message, mode=None):
    if not mode:
        print('\t\t\t  '+message)
    else:
        print('[{}] {:9s}: {}'.format(os.getpid(), mode, message))
