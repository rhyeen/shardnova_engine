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

    def test_external_u_turn(self):
        """ Setting course, then setting a new course in opposite direction,
            past the original source.
        """
        self.run_test(self._test_external_u_turn)

    def _test_external_u_turn(self, args=None):
        test_config = {
            'preserve_output': True,
            'silence_output': True
        }
        self.bootstrapper = self.get_bootstrapper(self.game_file, test_config)
        output_records = self.__get_output_records()
        assert(len(output_records) == 1)
        assert(output_records[0] == 'Welcome to Shardnova!\nType any command to continue.')
        # star <-5-> planet <-4-> starting factory <-3-> beacon
        # drone starts at starting factory, set course to star
        # ProbeDrone: distance traveled per tick: 2
        # ProbeDrone: fuel per distance: 0.2
        self.__get_command('set_course')(0)
        assert (len(output_records) == 2)
        assert('On course to: Star: starS' in output_records[1])
        assert('1.8/20.0 fuel' in output_records[1])
        assert('9.0 pu' in output_records[1])
        assert('ETA: 5 ticks' in output_records[1])
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__get_command('check_course')()
        assert (len(output_records) == 3)
        assert('On course to: Star: starS' in output_records[2])
        assert('Fuel remaining: 18.4' in output_records[2])
        assert('Distance remaining: 1.0 pu' in output_records[2])
        assert('ETA: 1 ticks' in output_records[2])
        self.__get_command('get_map')()
        assert (len(output_records) == 4)
        assert('Galaxy: galaxyS' in output_records[3])
        assert('Sector: sectorS' in output_records[3])
        assert('System: systemS' in output_records[3])
        assert('0: Star: starS' in output_records[3])
        assert('1: Planet: planetS' in output_records[3])
        assert('1: Planet: planetS' in output_records[3])
        assert('2: startingFactoryS' in output_records[3])
        assert('3: Beacon: beaconS' in output_records[3])
        assert('On course from startingFactoryS to Star: starS' in output_records[3])
        self.__get_command('set_course')(3)
        assert (len(output_records) == 5)
        assert ('On course to: Beacon: beaconS' in output_records[4])
        assert ('2.2/18.4 fuel' in output_records[4])
        assert ('11.0 pu' in output_records[4])
        assert ('ETA: 6 ticks' in output_records[4])
        self.__tick()
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 6)
        assert ('On course to: Beacon: beaconS' in output_records[5])
        assert ('Fuel remaining: 17.6' in output_records[5])
        assert ('Distance remaining: 7.0 pu' in output_records[5])
        assert ('ETA: 4 ticks' in output_records[5])

    def test_internal_u_turn(self):
        """ Setting course, then setting a new course in opposite direction,
            but not past the original source.
        """
        self.run_test(self._test_internal_u_turn)

    def _test_internal_u_turn(self, args=None):
        test_config = {
            'preserve_output': True,
            'silence_output': True
        }
        self.bootstrapper = self.get_bootstrapper(self.game_file, test_config)
        output_records = self.__get_output_records()
        assert(len(output_records) == 1)
        assert(output_records[0] == 'Welcome to Shardnova!\nType any command to continue.')
        # star <-5-> planet <-4-> starting factory <-3-> beacon
        # drone starts at starting factory, set course to star
        # ProbeDrone: distance traveled per tick: 2
        # ProbeDrone: fuel per distance: 0.2
        self.__get_command('set_course')(0)
        assert (len(output_records) == 2)
        assert('On course to: Star: starS' in output_records[1])
        assert('1.8/20.0 fuel' in output_records[1])
        assert('9.0 pu' in output_records[1])
        assert('ETA: 5 ticks' in output_records[1])
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__tick()  # 2pu, 0.4 fuel
        self.__get_command('check_course')()
        assert (len(output_records) == 3)
        assert('On course to: Star: starS' in output_records[2])
        assert('Fuel remaining: 18.4' in output_records[2])
        assert('Distance remaining: 1.0 pu' in output_records[2])
        assert('ETA: 1 ticks' in output_records[2])
        self.__get_command('set_course')(1)
        assert (len(output_records) == 4)
        assert ('On course to: Planet: planetS' in output_records[3])
        assert ('0.8/18.4 fuel' in output_records[3])
        assert ('4.0 pu' in output_records[3])
        assert ('ETA: 2 ticks' in output_records[3])
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 5)
        assert ('On course to: Planet: planetS' in output_records[4])
        assert ('Fuel remaining: 18.0' in output_records[4])
        assert ('Distance remaining: 2.0 pu' in output_records[4])
        assert ('ETA: 1 ticks' in output_records[4])
        self.__tick()
        assert (len(output_records) == 6)
        assert ('reached Planet: planetS' in output_records[5])
        self.__get_command('check_course')()
        assert (len(output_records) == 7)
        assert (output_records[6] == 'No directive set.')

    def test_further_ahead_course(self):
        """ New course further than original course, and new course in same direction.
        """
        self.run_test(self._test_further_ahead_course)

    def _test_further_ahead_course(self, args=None):
        test_config = {
            'preserve_output': True,
            'silence_output': True
        }
        self.bootstrapper = self.get_bootstrapper(self.game_file, test_config)
        output_records = self.__get_output_records()
        assert(len(output_records) == 1)
        assert(output_records[0] == 'Welcome to Shardnova!\nType any command to continue.')
        # star <-5-> planet <-4-> starting factory <-3-> beacon
        # drone starts at starting factory, set course to star
        # ProbeDrone: distance traveled per tick: 2
        # ProbeDrone: fuel per distance: 0.2
        self.__get_command('set_course')(1)
        assert (len(output_records) == 2)
        assert('On course to: Planet: planetS' in output_records[1])
        assert('0.8/20.0 fuel' in output_records[1])
        assert('4.0 pu' in output_records[1])
        assert('ETA: 2 ticks' in output_records[1])
        self.__tick()  # 2pu, 0.4 fuel
        self.__get_command('check_course')()
        assert (len(output_records) == 3)
        assert('On course to: Planet: planetS' in output_records[2])
        assert('Fuel remaining: 19.6' in output_records[2])
        assert('Distance remaining: 2.0 pu' in output_records[2])
        assert('ETA: 1 ticks' in output_records[2])
        self.__get_command('set_course')(0)
        assert (len(output_records) == 4)
        assert ('On course to: Star: starS' in output_records[3])
        assert ('1.4/19.6 fuel' in output_records[3])
        assert ('7.0 pu' in output_records[3])
        assert ('ETA: 4 ticks' in output_records[3])
        self.__tick()
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 5)
        assert ('On course to: Star: starS' in output_records[4])
        assert ('Fuel remaining: 18.8' in output_records[4])
        assert ('Distance remaining: 3.0 pu' in output_records[4])
        assert ('ETA: 2 ticks' in output_records[4])

    def test_cutting_course_short(self):
        """ Original course further than new course, and new course in same direction.
        """
        self.run_test(self._test_cutting_course_short)

    def _test_cutting_course_short(self, args=None):
        test_config = {
            'preserve_output': True,
            'silence_output': True
        }
        self.bootstrapper = self.get_bootstrapper(self.game_file, test_config)
        output_records = self.__get_output_records()
        assert(len(output_records) == 1)
        assert(output_records[0] == 'Welcome to Shardnova!\nType any command to continue.')
        # star <-5-> planet <-4-> starting factory <-3-> beacon
        # drone starts at starting factory, set course to star
        # ProbeDrone: distance traveled per tick: 2
        # ProbeDrone: fuel per distance: 0.2
        self.__get_command('set_course')(0)
        assert (len(output_records) == 2)
        assert ('On course to: Star: starS' in output_records[1])
        assert ('1.8/20.0 fuel' in output_records[1])
        assert ('9.0 pu' in output_records[1])
        assert ('ETA: 5 ticks' in output_records[1])
        self.__tick()  # 2pu, 0.4 fuel
        self.__get_command('check_course')()
        assert (len(output_records) == 3)
        assert('On course to: Star: starS' in output_records[2])
        assert('Fuel remaining: 19.6' in output_records[2])
        assert('Distance remaining: 7.0 pu' in output_records[2])
        assert('ETA: 4 ticks' in output_records[2])
        self.__get_command('set_course')(1)
        assert (len(output_records) == 4)
        assert ('On course to: Planet: planetS' in output_records[3])
        assert ('0.4/19.6 fuel' in output_records[3])
        assert ('2.0 pu' in output_records[3])
        assert ('ETA: 1 ticks' in output_records[3])
        self.__tick()
        assert (len(output_records) == 5)
        assert ('reached Planet: planetS' in output_records[4])
        self.__tick()
        self.__get_command('check_course')()
        assert (len(output_records) == 6)
        assert (output_records[5] == 'No directive set.')
        self.__get_command('get_map')()
        assert (len(output_records) == 7)
        assert ('Currently orbiting Planet: planetS' in output_records[6])

    def __tick(self):
        self.bootstrapper.time_keeper.tick()

    def __get_output_records(self):
        return self.bootstrapper.user.output_handler.output_records

    def __get_command(self, command_call):
        return self.bootstrapper.user_commands.get_command_function(command_call)


def run_tests(functional_test):
    """ All test cases should be ran in here for organization.
    """
    functional_test.test_external_u_turn()
    functional_test.test_internal_u_turn()
    functional_test.test_further_ahead_course()
    functional_test.test_cutting_course_short()


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
