""" Container for ThreadConsoleUser
"""
import threading
from scripts.presenters.console_user import ConsoleUser


class ThreadConsoleUser(object):

    def __init__(self, interactor, kill_switch, user=None):
        self.__kill_switch = kill_switch
        self.__console_user = ConsoleUser(interactor)
        self.__thread_worker = ThreadWorker(self.__console_user, self.__kill_switch)

    def get_thread(self):
        return self.__thread_worker


class ThreadWorker(threading.Thread):

    def __init__(self, console_user, kill_switch):
        threading.Thread.__init__(self)
        self.__console_user = console_user
        self.__kill_switch = kill_switch

    def run(self):
        do_work(self.__console_user, self.__kill_switch)


def do_work(console_user, kill_switch):
    while not kill_switch.should_kill():
        console_user.start_console()
