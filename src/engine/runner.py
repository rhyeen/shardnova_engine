""" Container for starting runner
"""
import argparse

from scripts.tick_bootstrapper import TickBootstrapper
from scripts.user_bootstrapper import UserBootstrapper
from scripts.thread_bootstrapper import ThreadBootstrapper
from tools.log_manager import LogManager


def get_args():
    description = ('Runs the Shardnova Backend Engine')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e',
                        '--environment',
                        default='local',
                        help='environment in which the script is running: local, stage, prod, test')
    parser.add_argument('-i',
                        '--interface',
                        default='thread',
                        help='type of console to run: thread, time, user')
    parsed = parser.parse_args()
    environment = parsed.environment
    interface = parsed.interface
    return environment, interface


def main():
    """ Begins the series of events necessary for the runner
    """
    log_manager = None
    try:
        environment, interface = get_args()
        log_manager = LogManager(script_id='Engine',
                                 project_id='Shardnova',
                                 environment=environment)
        if interface == 'thread':
            bootstrapper = ThreadBootstrapper(log_manager, environment)
        elif interface == 'time':
            bootstrapper = TickBootstrapper(log_manager, environment)
        elif interface == 'user':
            bootstrapper = UserBootstrapper(log_manager, environment)
        else:
            raise ValueError('Invalid interface: {0}'.format(interface))
        bootstrapper.execute()
        log_manager.record_cached_logs()
    except KeyboardInterrupt:
        exit()
    except:
        if log_manager:
            # @NOTE: If there are any non-kill logs cached, flush them so that we have them, but
            # they are isolated from the kill log message.
            log_manager.record_cached_logs()
            log_manager.cache_log(add_traceback=True, alert=True)
            log_manager.record_cached_logs(message_id='Fatal Error', message_type='ERROR')
        raise


""" Initial setup
"""
main()
