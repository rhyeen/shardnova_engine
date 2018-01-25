""" Container for Log Manager
"""
import datetime
import json
import random
import string
import time
import traceback

class BlankLogManager(object):
    """ See README.md
    """

    def __init__(self,
                 script_id=None,
                 project_id=None,
                 environment=None,
                 log_table='log'):
        """ Sets up the class with the given arguments
        Args:
            script_id (STR): Name of the parent script that logged.
            project_id (STR): Name of the project which triggered the log.
            environment (STR): environment in which the script is running: local, stage, prod, test
            log_table (STR): Table to log to
        """
        self.script_id = script_id
        self.project_id = project_id
        self.environment = environment
        self._log_table = log_table

    def log(self, message_id, message_type, message, private=False, alert=True):
        """ Records log
        Args:
            message_id (STR): Log entry's title. A developer defined ID.
            message_type (STR): ERROR, WARN, UPDATE, METRICS, INFO or TEST (can be others)
            message (STR): Message to be logged
            private (BOOLEAN, optional): Flag indicating if sensitive information is in log
            alert (BOOLEAN, optional): Flag indicating if a alert should be sent
        """
        log_id = self._generate_log_id()
        log = self._construct_log_message(log_id, message_id, message_type, message, private)
        print(log)

    @staticmethod
    def cache_log(message=None, add_traceback=False, private=False, alert=True):
        """ Adds the message from the raised exception to the list of tracebacks.
        Args:
            message (STR): Message to be logged
            add_traceback (BOOLEAN, optional): Flag indicating if traceback should be included
                in log message
            private (BOOLEAN, optional): Flag indicating if sensitive information is in log
            alert (BOOLEAN, optional): Flag indicating if a alert should be sent
        """
        if add_traceback:
            traceback_str = 'MESSAGE: {0} + TRACEBACK: {1}'.format(message, traceback.format_exc())
        else:
            traceback_str = message
        if 'KeyboardInterrupt' in traceback_str:
            return
        print(traceback_str)

    def record_cached_logs(self, message_id='test', message_type='TEST', traceback_limit=5):
        """ Records the cached logs
        Args:
            message_id (STR): Log entry's title. A developer defined ID.
            message_type (STR): ERROR, WARN, UPDATE, METRICS, INFO or TEST (can be others)
            traceback_limit (INT, optional):  Number of tracebacks to enter into the log
        """
        pass

    def _construct_log_message(self, log_id, message_id, message_type, message, private=False):
        """ Constructs a log message
        Args:
            log_id (STR): Uniquely generated id of this log
            message_id (STR): Log entry's title. A developer defined ID.
            message_type (STR): ERROR, WARN, UPDATE, METRICS, INFO or TEST (can be others)
            message (STR): Message to be logged
            private (BOOLEAN, optional): Flag indicating if sensitive information is in log
        """
        log_properties = {}
        log_properties['log_id'] = log_id
        log_properties['script_id'] = self.script_id
        log_properties['project_id'] = self.project_id
        log_properties['message_id'] = message_id
        log_properties['message_type'] = message_type
        if not private:
            log_properties['message'] = message
        return json.dumps(log_properties)

    @staticmethod
    def _generate_log_id():
        """ Generates a log id of the form "YYMMDDHHmmSSxxxxxx" where YYMMDDHHmmSS
            is the current date and xxxxxx is a randomly generated string
        """
        log_id = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d%H%M%S')
        alphanumeric_choices = string.ascii_lowercase + string.ascii_uppercase + string.digits
        log_id += ''.join(random.choice(alphanumeric_choices) for _ in range(6))
        return log_id

