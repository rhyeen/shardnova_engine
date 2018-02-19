""" Container for ThreadTicker
"""
import threading
import time


def tick(time_keeper):
    time_keeper.tick()


class ThreadTicker(object):

    def __init__(self, time_keeper, kill_switch, tick_duration=60):
        self.__time_keeper = time_keeper
        self.__kill_switch = kill_switch
        self.__is_console_tick = False
        self.__tick_duration = tick_duration
        self.__thread_worker = None

    def get_thread(self):
        self.__thread_worker = ThreadWorker(self.__tick_duration,
                                            tick,
                                            self.__time_keeper,
                                            self.__kill_switch,
                                            self.__is_console_tick)
        return self.__thread_worker

    def set_tick_duration(self, tick_duration):
        self.__tick_duration = tick_duration

    def set_to_console_ticker(self):
        self.__is_console_tick = True


class ThreadWorker(threading.Thread):

    def __init__(self, delay, work_function, work_function_args, kill_switch, is_console_tick):
        threading.Thread.__init__(self)
        self.__delay = delay
        self.__work_function = work_function
        self.__work_function_args = work_function_args
        self.__kill_switch = kill_switch
        self.__is_console_tick = is_console_tick

    def run(self):
        if not self.__is_console_tick:
            do_timed_work(self.__delay, self.__work_function, self.__work_function_args, self.__kill_switch)
        else:
            do_input_work(self.__work_function, self.__work_function_args, self.__kill_switch)


def do_timed_work(delay, work_function, work_function_args, kill_switch):
    while not kill_switch.should_kill():
        work_function(work_function_args)
        time.sleep(delay)


def do_input_work(work_function, work_function_args, kill_switch):
    while not kill_switch.should_kill():
        _ = input('>>')
        print('Tick...')
        work_function(work_function_args)
