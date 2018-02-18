""" Container for ThreadUserController
"""
import threading


class ThreadUserController(object):

    def __init__(self, control_function):
        self.__thread_worker = ThreadWorker(control_function)

    def get_thread(self):
        return self.__thread_worker


class ThreadWorker(threading.Thread):

    def __init__(self, control_function):
        threading.Thread.__init__(self)
        self.__control_function = control_function

    def run(self):
        do_work(self.__control_function)


def do_work(script_command):
    script_command()
