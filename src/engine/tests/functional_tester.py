import abc
import traceback


class FunctionalTester(object):
    """ Abstraction for generating reports.  See root-level functional_test.py for an example of
        how to inherit it.

        Functional tester handles errors and reports on them in the console.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config, log_manager, print_to_console=True):
        self.config = config
        self.log_manager = log_manager
        self.show_print = print_to_console
        self.test_count = 0
        if self.show_print:
            print('\n\n' + self.make_bold('Running tests...'))

    def teardown(self, fail_message):
        """ Call after each test ends.
        """
        self.print_test_results(fail_message)

    def finish(self):
        """ Call after all tests have finished.
        """
        if self.show_print:
            print(self.make_bold('Tests completed'))

    def print_test_results(self, fail_message):
        """ Prints the test results to the console.
        """
        if self.show_print:
            self.test_count += 1
            if not fail_message:
                print(self.make_bold_green('Test ' + str(self.test_count) + ' successful.'))
            else:
                print(self.make_bold_red('Test ' + str(self.test_count) + ' failed:'))
                print(self.make_bold_red(fail_message))
                print(self.make_bold_red('For a more detailed analysis,'
                                         ' debug Test {0}'.format(self.test_count)))

    @staticmethod
    def make_bold_red(text):
        """ Returns the string colored with bold red.
        """
        return '\033[91m' + text + '\033[0m'

    @staticmethod
    def make_bold_green(text):
        """ Returns the string colored with bold green.
        """
        return '\033[92m' + text + '\033[0m'

    @staticmethod
    def make_bold(text):
        """ Returns the string colored with underline.
        """
        return '\033[4m' + text + '\033[0m'

    def run_test(self, test_function, test_function_args=None):
        """ Call to run a given test_function with the given list of test_function_args.
        """
        fail_message = None
        try:
            test_function(test_function_args)
        except:
            fail_message = traceback.format_exc()

        self.teardown(fail_message)

