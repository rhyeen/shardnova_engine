""" Container for Bootstrapper
"""

from tools.http_requester import HttpRequester
from tools.query_handler import QueryHandler
from scripts.query_maker import QueryMaker

class Bootstrapper(object):
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
        self._query_handler = QueryHandler(environment)

    def _is_test_run(self):
        if not self.environment:
            return False
        return self.environment == 'test'

    def execute(self):
        """ Runs the entire automation.
            See the individual function definitions for more details.
        """
        pass

    def call_mysql_database(self):
        """ Typical method for making MySQL queries and returning responses.
        """
        params = {
            'test_column': 'test',
            'test_other_name': True,
            'test_flag': 999
        }
        # returns the response in Python dict format
        query = QueryMaker.get_test_query
        # optional: only keep if query needs function_args passed in.
        query_function_args = {
            'is_test': self._is_test
        }
        results = self._query_handler.get_query_results(query, params, query_function_args)
        if len(results) <= 0:
            return None
        return results[0]['test_column']
