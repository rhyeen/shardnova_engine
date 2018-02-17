""" Container for ThreadTicker
"""
import threading
import time


def tick(time_keeper):
    print('Tick...')
    time_keeper.tick()


class ThreadTicker(object):

    def __init__(self, time_keeper, kill_switch):
        self.__time_keeper = time_keeper
        self.__kill_switch = kill_switch
        self.__thread_worker = ThreadWorker(3, tick, self.__time_keeper, self.__kill_switch)

    def get_thread(self):
        return self.__thread_worker


class ThreadWorker(threading.Thread):

    def __init__(self, delay, work_function, work_function_args, kill_switch):
        threading.Thread.__init__(self)
        self.__delay = delay
        self.__work_function = work_function
        self.__work_function_args = work_function_args
        self.__kill_switch = kill_switch

    def run(self):
        do_work(self.__delay, self.__work_function, self.__work_function_args, self.__kill_switch)


def do_work(delay, work_function, work_function_args, kill_switch):
    while not kill_switch.should_kill():
        work_function(work_function_args)
        time.sleep(delay)
