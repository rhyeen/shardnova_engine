""" Container for UserBootstrapper
"""
from scripts.facades.game import Game
from scripts.interfaces.data_handler.random_string_test_handler import RandomStringTestHandler
from scripts.presenters.console_user import ConsoleUser
from scripts.controllers.interactor import Interactor


class UserBootstrapper(object):
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
        data_hander = RandomStringTestHandler()
        game = Game(data_hander)
        interactor = Interactor(data_hander, game)
        interactor.initialize_game()
        ConsoleUser(interactor)
