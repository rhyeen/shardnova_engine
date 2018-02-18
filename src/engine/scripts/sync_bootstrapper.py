""" Container for SyncBootstrapper
"""
from scripts.facades.game import Game
from scripts.interfaces.data_handler.random_string_test_handler import RandomStringTestHandler
from scripts.presenters.scripted_user import ScriptedUser
from scripts.controllers.interactor import Interactor
from scripts.controllers.time_keeper import TimeKeeper
from scripts.interfaces.output_handler.console_output_handler import ConsoleOutputHandler


class SyncBootstrapper(object):
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
        data_handler = RandomStringTestHandler()
        game = Game(data_handler)
        self.__interactor = Interactor(data_handler, game)
        self.time_keeper = TimeKeeper(game)
        self.__interactor.initialize_game()
        self.user = self.__interactor.create_phone_user('+0', ConsoleOutputHandler(test_config))
        self.user_commands = ScriptedUser(self.__interactor, self.user)

    def _is_test_run(self):
        if not self.environment:
            return False
        return self.environment == 'test'
