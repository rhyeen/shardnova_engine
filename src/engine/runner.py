""" Container for starting runner
"""
import argparse

from scripts.bootstrapper import Bootstrapper
from tools.log_manager import LogManager


def get_config():
    description = ('Runs the Shardnova Backend Engine')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e',
                        '--environment',
                        default='local',
                        help='environment in which the script is running: local, stage, prod, test')
    parsed = parser.parse_args()
    environment = parsed.environment
    return environment


def main():
    """ Begins the series of events necessary for the runner
    """
    log_manager = None
    try:
        config, environment = get_config()
        log_manager = LogManager(script_id='Enginer',
                                 project_id='Shardnova',
                                 environment=environment)
        bootstrapper = Bootstrapper(log_manager, environment)
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
