""" Container for starting functional tests
"""
import os
import json
import argparse

from tests.functional_tester import FunctionalTester
from tests.mysql_manipulator import MysqlManipulator
from tests.functional_test_populator import FunctionalTestPopulator
from tests.blank_log_manager import BlankLogManager

from scripts.bootstrapper import Bootstrapper


""" Possible considerations when testings:
    DONE:
        List of tests that are completed by the functional test
    TODO:
        List of tests that still need to be performed
    OUT-OF-SCOPE:
        List of tests that would be nice, but are out of scope.  Consider doing manual tests.
    INTEGRATION TESTING:
        List of tests that the integration testing should account for, with Bootstrapper in mind.
"""


class MyFunctionalTester(FunctionalTester):
    """ Run this automation to start your functional tests.  Test should be:
        + repeatable
        + verifiable
        + robust
        + isolated to its own environment
        + all of the above without the developer doing anything except starting the tests.

        To do this, functional tests should take a few precautions:
        REPEATABLE & ISOLATED:
        + test tables should end in '_test'
            + the test table is cleared before running a test and populated with pre-test data
        + test files should be in '/test' sub-directory
            + the test files are cleared before running a test and populated with pre-test data
        + internal API calls should either be mocked out using `test_config` or have a test flag
            that can be passed in
        + public API calls should be mocked out using `test_config`
        + random-like variables should be replaced with variables from `test_config`. For example:
            + random number generators should either be given a seed or replaced
            + datetime.now() should be replaced
        VERIFIABLE:
        + after running the automation under test, check:
            + tables that would be modified
            + files that would be modified
            + Qualtrics survey responses, mailing lists, users, etc. that would be modified
        ROBUST:
        + keep a running list of all possible special cases to test at the top of the document,
            even if you don't have time to test them all, you know it's a goal to reach for.
            + this also lets you know what tests you still need to create, and where you may have
                weaknesses in your coverage
    """

    def __init__(self, log_manager, environment, print_to_console=True):
        super(MyFunctionalTester, self).__init__(log_manager, print_to_console)
        self._mysql_manipulator = MysqlManipulator()
        self.environment = environment

    def _setup(self, tables):
        for table in tables:
            table_name = table['table_name']
            if 'drop' not in table or not table['drop']:
                self._mysql_manipulator.clear_table(table_name)
            else:
                try:
                    self._mysql_manipulator.drop_table(table_name)
                except:
                    pass # no table to drop
        for table in tables:
            if 'entries' not in table:
                continue
            entries = table['entries']
            table_name = table['table_name']
            self._mysql_manipulator.add_dict_entries_to_table(table_name, entries)

    def _run_automation(self, test_config):
        my_starting_class = Bootstrapper(self.log_manager,
                                         self.environment,
                                         test_config)
        my_starting_class.execute()

    def test_something(self):
        self.run_test(self._test_something)

    def _test_something(self, args=None):
        # prepare to populate database tables
        populate_tables = []
        entries = FunctionalTestPopulator.get_test_table_entries()
        table = {
            'table_name': 'test_table',
            'entries': entries
        }
        populate_tables.append(table)

        test_config = {
            'something_externally_controlled_data': [
                'like_datetimes',
                'or_api_calls'
            ]
        }

        # Start your script
        self._run_automation(test_config)

        # Script has finished, now verify outgoing data
        # Such as tables that are affected
        results = self._mysql_manipulator.get_table_entries('test_table')
        assert len(results) == 2
        single_result = results[1]
        assert single_result['some_column'] == 'test'


def run_tests(functional_test):
    """ All test cases should be ran in here for organization.
    """
    functional_test.test_something()


def get_config():
    """ Retrieves the config from the arguments passed in.  Default is config/config_test.json
    """
    description = ('Functional testing.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e',
                        '--environment',
                        default='test',
                        help='environment in which the script is running: local, stage, prod, test')
    parsed = parser.parse_args()
    environment = parsed.environment
    return environment


def main():
    """ Begins each functional test
    """
    # @NOTE: we use a shell log_manager here since we want don't want to log testing errors.
    environment = get_config()
    log_manager = BlankLogManager()
    functional_test = MyFunctionalTester(log_manager, environment)
    run_tests(functional_test)
    functional_test.finish()

""" Initial setup
"""
main()
