""" Container for ThreadUserController
"""
import threading


class ThreadUserController(object):

    def __init__(self, control_function, kill_switch):
        self.__kill_switch = kill_switch
        self.__thread_worker = ThreadWorker(control_function, self.__kill_switch)

    def get_thread(self):
        return self.__thread_worker


class ThreadWorker(threading.Thread):

    def __init__(self, control_function, kill_switch):
        threading.Thread.__init__(self)
        self.__control_function = control_function
        self.__kill_switch = kill_switch

    def run(self):
        do_work(self.__control_function, self.__kill_switch)


def do_work(script_command, kill_switch):
    script_command(kill_switch)
