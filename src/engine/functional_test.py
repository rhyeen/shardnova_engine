""" Container for starting functional tests
"""
import argparse
import json
import os

from tests.functional_tester import FunctionalTester
from tests.mysql_manipulator import MysqlManipulator
from tests.functional_test_populator import FunctionalTestPopulator
from tests.blank_log_manager import BlankLogManager

from scripts.sync_bootstrapper import SyncBootstrapper


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

    def __init__(self, log_manager, environment, game_file, print_to_console=True):
        super(MyFunctionalTester, self).__init__(log_manager, print_to_console)
        self._mysql_manipulator = MysqlManipulator(environment)
        self.environment = environment
        self.game_file = game_file
        self.bootstrapper = None

    def _setup(self, tables):
        for table in tables:
            table_name = table['table_name']
            if 'drop' not in table or not table['drop']:
                self._mysql_manipulator.clear_table(table_name)
            else:
                try:
                    self._mysql_manipulator.drop_table(table_name)
                except:
                    pass  # no table to drop
        for table in tables:
            if 'entries' not in table:
                continue
            entries = table['entries']
            table_name = table['table_name']
            self._mysql_manipulator.add_dict_entries_to_table(table_name, entries)

    def get_bootstrapper(self, game_file, test_config):
        return SyncBootstrapper(self.log_manager,
                                self.environment,
                                game_file,
                                test_config)

    def test_in_system_courses(self):
        self.run_test(self._test_in_system_courses)

    def _test_in_system_courses(self, args=None):
        test_config = {
            'preserve_output': True
        }
        self.bootstrapper = self.get_bootstrapper(self.game_file, test_config)
        output_records = self.__get_output_records()
        assert(len(output_records) == 1)
        self.__get_command('set_course')(0)
        assert(len(output_records) == 2)
        self.__tick()
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 3)
        self.__get_command('get_map')()
        assert (len(output_records) == 4)
        self.__get_command('set_course')(3)
        assert (len(output_records) == 5)
        self.__tick()
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 6)

    def __tick(self):
        self.bootstrapper.time_keeper.tick()

    def __get_output_records(self):
        return self.bootstrapper.user.output_handler.output_records

    def __get_command(self, command_call):
        return self.bootstrapper.user_commands.get_command_function(command_call)


def run_tests(functional_test):
    """ All test cases should be ran in here for organization.
    """
    functional_test.test_in_system_courses()


def get_args():
    description = ('Functional testing.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e',
                        '--environment',
                        default='test',
                        help='environment in which the script is running: local, stage, prod, test')
    parsed = parser.parse_args()
    environment = parsed.environment
    return environment


def get_game_file(environment):
    environment_mapping = {
        'test': '../config/test/game.json'
    }
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    game_file = json.load(open(environment_mapping[environment]))
    return game_file


def main():
    """ Begins each functional test
    """
    # @NOTE: we use a shell log_manager here since we want don't want to log testing errors.
    environment = get_args()
    game_file = get_game_file(environment)
    log_manager = BlankLogManager()
    functional_test = MyFunctionalTester(log_manager, environment, game_file)
    run_tests(functional_test)
    functional_test.finish()


""" Initial setup
"""
main()
