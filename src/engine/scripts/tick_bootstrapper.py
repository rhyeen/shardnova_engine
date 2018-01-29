""" Container for TickBootstrapper
"""
from scripts.facades.game import Game
from scripts.interfaces.data_handler.random_string_test_handler import RandomStringTestHandler
from scripts.presenters.console_ticker import ConsoleTicker
from scripts.controllers.interactor import Interactor
from scripts.controllers.time_keeper import TimeKeeper


class TickBootstrapper(object):
    """ Class definition
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

    def _is_test_run(self):
        if not self.environment:
            return False
        return self.environment == 'test'

    def execute(self):
        """ Runs the entire automation.
            See the individual function definitions for more details.
        """
        game = Game()
        data_hander = RandomStringTestHandler()
        interactor = Interactor(data_hander, game)
        interactor.initialize_game()
        time_keeper = TimeKeeper(game)
        console_ticker = ConsoleTicker()
        console_ticker.start_console(time_keeper)
