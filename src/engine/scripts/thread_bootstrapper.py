""" Container for ThreadBootstrapper
"""
from scripts.facades.game import Game
from scripts.interfaces.data_handler.random_string_test_handler import RandomStringTestHandler
from scripts.presenters.thread_ticker import ThreadTicker
from scripts.presenters.thread_user_controller import ThreadUserController
from scripts.presenters.console_user import ConsoleUser
from scripts.presenters.scripted_user import ScriptedUser
from scripts.controllers.interactor import Interactor
from scripts.controllers.time_keeper import TimeKeeper
from scripts.kill_switch import KillSwitch
from scripts.interfaces.output_handler.console_output_handler import ConsoleOutputHandler


class ThreadBootstrapper(object):
    """ The threadbootstrapper starts up a single console user
        interface and threaded auto ticker.
    """

    def __init__(self, log_manager, environment, test_config=None):
        """ Sets up the class with the given configs
        Args:
            log_manager (LOGMANAGER): For keeping track of tracebacks/logs.
            environment (STR): environment in which the script is running: local, stage, prod, test
            test_config (DICT): replaces real values are integration points with test values to
                ensure repeatability and testability during functional testing.
        """
        self._html_content = None
        self.log_manager = log_manager
        self.test_config = test_config
        self.environment = environment
        self._is_test = self._is_test_run()
        self.__kill_switch = KillSwitch()
        self.__thread_user_controller = None
        data_handler = RandomStringTestHandler()
        game = Game(data_handler, test_config)
        self.__interactor = Interactor(data_handler, game)
        self.__time_keeper = TimeKeeper(game)
        self.__interactor.initialize_game()
        self.__tick_duration = None
        self.__console_tick = False

    def _is_test_run(self):
        if not self.environment:
            return False
        return self.environment == 'test'

    def set_tick_duration(self, tick_duration):
        self.__tick_duration = tick_duration

    def set_console_tick(self):
        self.__console_tick = True

    def set_scripted_controller(self, script_function_name):
        user = self.__interactor.create_phone_user('+0', ConsoleOutputHandler(self.test_config))
        scripted_user = ScriptedUser(self.__interactor, user, self.__kill_switch)
        script_function = scripted_user.get_command_function(script_function_name)
        self.__thread_user_controller = ThreadUserController(script_function)

    def set_console_controller(self):
        console_user = ConsoleUser(self.__interactor, None, self.__kill_switch)
        self.__thread_user_controller = ThreadUserController(console_user.start_console)

    def __get_thread_user_controller(self):
        if not self.__thread_user_controller:
            self.set_console_controller()
        return self.__thread_user_controller

    def execute(self):
        """ Runs the entire automation.
            See the individual function definitions for more details.
        """
        thread_ticker = ThreadTicker(self.__time_keeper, self.__kill_switch)
        if self.__tick_duration:
            thread_ticker.set_duration(self.__tick_duration)
        if self.__console_tick:
            thread_ticker.set_to_console_ticker()
        ticking_thread = thread_ticker.get_thread()
        thread_user_controller = self.__get_thread_user_controller()
        user_thread = thread_user_controller.get_thread()
        try:
            ticking_thread.start()
            user_thread.start()
            ticking_thread.join()
            user_thread.join()
        except KeyboardInterrupt:
            self.__kill_switch.flip_to_kill()
