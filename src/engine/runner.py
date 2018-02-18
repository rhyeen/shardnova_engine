""" Container for starting runner
"""
import argparse
from scripts.thread_bootstrapper import ThreadBootstrapper
from tools.log_manager import LogManager


def get_args():
    description = ('Runs the Shardnova Backend Engine')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-e',
                        '--environment',
                        default='local',
                        help='environment in which the script is running: local, stage, prod, test')
    parser.add_argument('-s',
                        '--script',
                        default=None,
                        help='user script function name. Default will set to console user.')
    parser.add_argument('-t',
                        '--tick',
                        default=None,
                        help='How many milliseconds is the tick. Default is game default (60000).  May also set to "console" to control ticks via input.')
    parsed = parser.parse_args()
    environment = parsed.environment
    script = parsed.script
    tick = parsed.tick
    return environment, script, tick


def main():
    """ Begins the series of events necessary for the runner
    """
    log_manager = None
    try:
        environment, script, tick = get_args()
        log_manager = LogManager(script_id='Engine',
                                 project_id='Shardnova',
                                 environment=environment)
        bootstrapper = ThreadBootstrapper(log_manager, environment)
        # @DEBUG:
        script = 'basic_commands'
        tick = 'console'
        if script is not None:
            bootstrapper.set_scripted_controller(script)
        if tick == 'console':
            bootstrapper.set_console_tick()
        elif tick is not None:
            bootstrapper.set_tick_duration(tick / 1000)
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
