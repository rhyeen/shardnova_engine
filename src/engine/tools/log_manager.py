""" Container for Log Manager
"""
import os
import datetime
import json
import random
import string
import time
import traceback

from tools.query_handler import QueryHandler

class LogManager(object):
    """ See README.md
    """
    constants = {
        'buffer_limit': 100
    }

    def __init__(self,
                 script_id,
                 project_id,
                 environment,
                 log_table='log'):
        """ Sets up the class with the given arguments
        Args:
            script_id (STR): Name of the parent script that logged.
            project_id (STR): Name of the project which triggered the log.
            routing_key (STR): Routing key of the team that will receive alerts
            environment (STR): environment in which the script is running: local, stage, prod, test
            log_table (STR): Table to log to
        """
        self.tracebacks = None
        self.tracebacks_metadata = None
        self.script_id = script_id
        self.project_id = project_id
        self.environment = environment
        self._log_table = log_table
        self.query_handler = QueryHandler(environment)
        self._reset_tracebacks()

    def _reset_tracebacks(self):
        self.tracebacks_metadata = {
            'private_alert': {
                'count': 0
            },
            'private_log': {
                'count': 0
            },
            'public_alert': {
                'count': 0
            },
            'public_log': {
                'count': 0
            }
        }
        self.tracebacks = {
            'private_alert': [],
            'private_log': [],
            'public_alert': [],
            'public_log': []
        }

    def log(self, message_id, message_type, message, private=False, alert=False):
        """ Records log.  More than likely, you'll want to instead cache_log(),
            then record_cahced_logs() at the end of your script to avoid alert fatigue.
        Args:
            message_id (STR): Log entry's title. A developer defined ID.
            message_type (STR): ERROR, WARN, UPDATE, METRICS, INFO or TEST (can be others)
            message (STR): Message to be logged
            private (BOOLEAN, optional): Flag indicating if sensitive information is in log
            alert (BOOLEAN, optional): Flag indicating if a alert should be sent
        """
        log_id = self._generate_log_id()
        params = {
            'log_id': log_id,
            'project_id': self.project_id,
            'script_id': self.script_id,
            'message_id': message_id,
            'message_type': message_type,
            'message': message
        }
        query_function_args = {
            'table': self._log_table
        }
        try:
            self.query_handler.get_query_results(self._get_log_query, params, query_function_args)
        except:
            entity_id = self._generate_entity_id(message_id)
            print('Failed to establish connection to log_manager db for {0}'.format(entity_id))
            # @TODO: handle alert stream
        log = self._construct_log_message(log_id, message_id, message_type, message, private)
        # Send to stdout for Sumo to pick up
        if not self._is_local_run():
            print(log)
        if self._should_send_alert(alert):
            # @TODO: handle alert stream
            pass

    def _generate_entity_id(self, message_id):
        return '{0} :: {1} :: {2}'.format(self.project_id, self.script_id, message_id)

    def _should_send_alert(self, alert):
        if not alert:
            return False
        return not self._is_local_run()

    def cache_log(self, message=None, add_traceback=False, private=False, alert=False):
        """ Adds the message from the raised exception to the list of tracebacks.
        Args:
            message (STR): Message to be logged.  If no message is given, add_traceback needs to
                be True so that at least the traceback is logged.  If a message is given and
                add_traceback is True, then message + traceback is logged.
            add_traceback (BOOLEAN, optional): Flag indicating if traceback should be included
                in log message
            private (BOOLEAN, optional): Flag indicating if sensitive information is in log
            alert (BOOLEAN, optional): Flag indicating if a alert should be sent
        """
        # @NOTE: nothing to report.
        if message is None and not add_traceback:
            return
        if message is None and add_traceback:
            traceback_str = traceback.format_exc()
        elif add_traceback:
            traceback_str = 'MESSAGE: {0} + TRACEBACK: {1}'.format(message, traceback.format_exc())
        else:
            traceback_str = message
        if 'KeyboardInterrupt' in traceback_str:
            return
        tracebacks, tracebacks_metadata = self._get_traceback_set(private, alert)
        if len(tracebacks) <= self.constants['buffer_limit']:
            tracebacks.append(traceback_str)
        tracebacks_metadata['count'] += 1
        if self._is_local_run():
            print(traceback_str)

    def _is_local_run(self):
        local_environments = [
            'test',
            'local',
            'dev'
        ]
        if not self.environment:
            return False
        return self.environment in local_environments

    def _get_traceback_set(self, private, alert):
        key = ''
        if private:
            key += 'private'
        else:
            key += 'public'
        if alert:
            key += '_alert'
        else:
            key += '_log'
        return self.tracebacks[key], self.tracebacks_metadata[key]

    def record_cached_logs(self, message_id='cached', message_type='WARN', traceback_limit=5):
        """ Records the cached logs
        Args:
            message_id (STR): Log entry's title. A developer defined ID.
            message_type (STR): ERROR, WARN, UPDATE, METRICS, INFO or TEST (can be others)
            traceback_limit (INT, optional):  Number of tracebacks to enter into the log
        """
        self._record_cached_logs(message_id, message_type, traceback_limit, True, True)
        self._record_cached_logs(message_id, message_type, traceback_limit, False, True)
        self._record_cached_logs(message_id, message_type, traceback_limit, True, False)
        self._record_cached_logs(message_id, message_type, traceback_limit, False, False)

    def _record_cached_logs(self, message_id, message_type, traceback_limit, private, alert):
        tracebacks, tracebacks_metadata = self._get_traceback_set(private, alert)
        if len(tracebacks) <= 0:
            return
        tracebacks = tracebacks[:]
        total_tracebacks = tracebacks_metadata['count']
        if total_tracebacks > traceback_limit:
            tracebacks = tracebacks[:traceback_limit]
            message = ('Showing {0}/{1} traceback messages'
                       .format(traceback_limit, total_tracebacks))
            tracebacks.insert(0, message)
        tracebacks_str = ('\n\n').join(tracebacks)
        self.log(message_id, message_type, tracebacks_str, private, alert)
        self._reset_tracebacks()

    @staticmethod
    def _get_log_query(query_function_args):
        """ Query for inserting into the log table
        """
        query = ('INSERT INTO {0} (`log_id`, `project_id`, `script_id`, `message_type`, '
                 '`message_id`, `message`, `datetime`) VALUES '
                 '(%(log_id)s, %(project_id)s, %(script_id)s, %(message_type)s, '
                 '%(message_id)s, %(message)s, now())')
        return {
            'query': query,
            'table': query_function_args['table']
        }

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

