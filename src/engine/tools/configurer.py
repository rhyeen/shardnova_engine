""" Container for ConfigExtractor
"""
import os
import pymysql.cursors
import dns.resolver

class Configurer(object):
    """ Extracts config information from a provided config file and from environmental variables,
        and provides that information to the caller in a consistent format.
        Some methods perform tasks dealing with the config object (like connecting to a db).
    """

    @staticmethod
    def check_config_object(config):
        """ Checks the config object to ensure it has the needed properties.
        Args:
            config (DICT): File should have the following format:
            {
                "automation_options": {
                    "is_test": <is this a functional test> OPTIONAL, // will alter db/SFTP files
                },
                ... /* other possiblities */
            }
        Raises:
            ValueError if no config object is passed in
            Exception if not a valid config object
        """
        if not config:
            raise ValueError('config parameter is required')
        if 'automation_options' not in config:
            raise Exception('config requires an "automation_options" property')

    @staticmethod
    def connect_mysql(config, alt_env_vars=None):
        """ Configures MySQL object, starts a connection on that object
            and returns it.
        Args:
            config (DICT): if the environment variables do not exist (e.g. a local environment
                outside of Docker), it will use the defaults in this config instead.  config should
                have the following format:
                {
                    "db_options": {
                        "host": "www.test.com",
                        "user": "test_user",
                        "password": "1234pass",
                        "database": "test_brand"
                    }
                }
            alt_env_vars (DICT, optional): this method assumes the following mapping
                of environment variables:
                    'host': 'MYSQL_HOST',
                    'user': 'MYSQL_USER',
                    'password': 'MYSQL_PASSWORD',
                    'database': 'MYSQL_DATABASE'
                if this mapping is not true, another mapping can be provided here.  The mapping
                should follow the format:
                {
                    'mysql': {
                        'host': 'MYSQL_HOST',
                        'user': 'MYSQL_USER',
                        'password': 'MYSQL_PASSWORD',
                        'database': 'MYSQL_DATABASE'
                    }
                }
        Raises:
            Exception: If environment variables and config cannot create a mysql connection, an
            exception will be raised.
        """
        environment_vars = Configurer._get_mysql_env_vars(alt_env_vars)
        host, user, password, database = Configurer._get_mysql_options(config, environment_vars)
        port = dns.resolver.query(host, 'SRV').response.answer[0].items[0].port
        mysql = pymysql.connect(host=host,
                                user=user,
                                passwd=password,
                                db=database,
                                port=port,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        return mysql

    @staticmethod
    def _get_mysql_env_vars(alt_env_vars=None):
        if alt_env_vars:
            return alt_env_vars
        return {
            'mysql': {
                'host': 'MYSQL_HOST',
                'user': 'MYSQL_USER',
                'password': 'MYSQL_PASSWORD',
                'database': 'MYSQL_DATABASE'
            }
        }

    @staticmethod
    def _get_mysql_options(config, environment_vars):
        if Configurer._should_get_mysql_options_from_env_var(environment_vars):
            return Configurer._get_mysql_options_from_env_var(environment_vars)
        else:
            return Configurer._get_mysql_options_from_config(config)

    @staticmethod
    def _should_get_mysql_options_from_env_var(environment_vars):
        host_key = environment_vars['mysql']['host']
        return host_key in os.environ

    @staticmethod
    def _get_mysql_options_from_env_var(environment_vars):
        host_key = environment_vars['mysql']['host']
        user_key = environment_vars['mysql']['user']
        password_key = environment_vars['mysql']['password']
        database_key = environment_vars['mysql']['database']
        host = os.environ[host_key]
        user = os.environ[user_key]
        password = os.environ[password_key]
        database = os.environ[database_key]
        return host, user, password, database

    @staticmethod
    def _get_mysql_options_from_config(config):
        """ Uses the config file's data if the environment is not setup.  Should only be for
            local testing outside of the docker container.
        """
        if 'db_options' not in config:
            raise Exception('config requires a "db_options" property for dev configuration')
        host = config['db_options']['host']
        user = config['db_options']['user']
        password = config['db_options']['password']
        database = config['db_options']['db']
        return host, user, password, database

    @staticmethod
    def get_test_flag(config):
        """ Returns True is is_test is specified in the config object
        """
        if not 'is_test' in config['automation_options']:
            return False
        if config['automation_options']['is_test']:
            return True
        return False

    @staticmethod
    def get_file_options(config, file_options_key):
        """ Returns the file options defined in config for the given file_options_key
        Raises:
            Exception: if the file_options_key'ed dict does not contain 'file_name', 'extension',
            and 'directory'.
        """
        if not 'file_options' in config:
            raise Exception('config requires a "file_options" property')
        if not file_options_key in config['file_options']:
            raise Exception('config["file_options"] requires a property under file_options_key')
        file_options = config['file_options'][file_options_key]
        if 'file_name' not in file_options:
            raise Exception('config["file_options"][file_options_key] '
                            'requires a "file_name" property')
        if 'extension' not in file_options:
            raise Exception('config["file_options"][file_options_key] '
                            'requires a "extension" property')
        if 'directory' not in file_options:
            raise Exception('config["file_options"][file_options_key] '
                            'requires a "directory" property')
        return file_options

    @staticmethod
    def get_email_options(config, email_options_key):
        """ Returns the email options defined in config for the given email_options_key
        Raises:
            Exception: if the email_options_key'ed dict does not contain 'recipient_list',
            and 'sent_from', or if 'recipient_list' is not a list, and 'sent_from' is not a string.
        """
        if not 'email_options' in config:
            raise Exception('config requires an "email_options" property')
        if not email_options_key in config['email_options']:
            raise Exception('config["email_options"] requires a property under email_options_key')
        email_options = config['email_options'][email_options_key]
        if 'recipient_list' not in email_options:
            raise Exception('config["email_options"][email_options_key] '
                            'requires a "recipient_list" property')
        if 'sent_from' not in email_options:
            raise Exception('config["email_options"][email_options_key] '
                            'requires a "sent_from" property')
        if not isinstance(email_options['recipient_list'], list):
            raise Exception('config["email_options"][email_options_key]["recipient_list"] '
                            'should be an array of email addresses')
        if len(email_options['recipient_list']) <= 0:
            raise Exception('config["email_options"][email_options_key]["recipient_list"] '
                            'requires at least one email address')
        if not isinstance(email_options['sent_from'], basestring):
            raise Exception('config["email_options"][email_options_key]["sent_from"] '
                            'should be an email addresses')
        return email_options

    @staticmethod
    def get_sftp_options(config, alt_env_vars=None, force_config=False):
        """ Returns a dict extracted from config that is used for SFTP.
        Args:
            config (DICT): if the environment variables do not exist (e.g. a local environment
                outside of Docker), it will use the defaults in this config instead.  config should
                have the following format:
                {
                    "db_options": {
                        "host": "www.test.com",
                        "user": "test_user",
                        "password": "1234pass",
                        "database": "test_brand"
                    }
                }
            alt_env_vars (DICT, optional): this method assumes the following mapping
                of environment variables:
                    'host': 'MYSQL_HOST',
                    'user': 'MYSQL_USER',
                    'password': 'MYSQL_PASSWORD',
                    'database': 'MYSQL_DATABASE'
                if this mapping is not true, another mapping can be provided here.  The mapping
                should follow the format:
                {
                    'mysql': {
                        'host': 'MYSQL_HOST',
                        'user': 'MYSQL_USER',
                        'password': 'MYSQL_PASSWORD',
                        'database': 'MYSQL_DATABASE'
                    }
                }
            force_config (BOOLEAN, optional): if true, environment variables will not be used: only
                config will be used.
        Raises:
            Exception: if not a valid config object
        """
        environment_vars = Configurer._get_sftp_env_vars(alt_env_vars)
        host, user, password, port = Configurer._get_sftp_options(config, environment_vars, force_config)
        return {
            "host": host,
            "user": user,
            "password": password,
            "port": port
        }

    @staticmethod
    def _get_sftp_env_vars(alt_env_vars=None):
        if alt_env_vars:
            return alt_env_vars
        return {
            'sftp': {
                'host': 'SFTP_HOST',
                'user': 'SFTP_USER',
                'password': 'SFTP_PASSWORD'
            }
        }

    @staticmethod
    def _get_sftp_options(config, environment_vars, force_config=False):
        if Configurer._should_get_sftp_options_from_env_var(environment_vars, force_config):
            return Configurer._get_sftp_options_from_env_var(environment_vars)
        else:
            return Configurer._get_sftp_options_from_config(config)

    @staticmethod
    def _should_get_sftp_options_from_env_var(environment_vars, force_config=False):
        host_key = environment_vars['sftp']['host']
        return not force_config and host_key in os.environ

    @staticmethod
    def _get_sftp_options_from_env_var(environment_vars):
        host_key = environment_vars['sftp']['host']
        user_key = environment_vars['sftp']['user']
        password_key = environment_vars['sftp']['password']
        host = os.environ[host_key]
        port = dns.resolver.query(host, 'SRV').response.answer[0].items[0].port
        password = os.environ[password_key]
        user = os.environ[user_key]
        return host, user, password, port

    @staticmethod
    def _get_sftp_options_from_config(config):
        """ Uses the config file's data if the environment is not setup.  Should only be for
            local testing outside of the docker container.
        """
        if 'sftp_options' not in config:
            raise Exception('config requires a "sftp_options" property for dev configuration')
        host = config['sftp_options']['host']
        try:
            port = dns.resolver.query(host, 'SRV').response.answer[0].items[0].port
        except:
            port = 22
        user = config['sftp_options']['user']
        password = config['sftp_options']['password']
        return host, user, password, port

    @staticmethod
    def get_api_token(config, api_token_variable):
        """ Returns the environment defined by api_token_variable, if it's defined.
            Otherwise, it returns the config defined api_token.
        """
        if not api_token_variable:
            api_token_variable = 'API_TOKEN'
        return Configurer.get_env_var(config, api_token_variable)

    @staticmethod
    def get_data_center(config, data_center_variable=None):
        """ Returns the environment defined by data_center_variable, if it's defined.
            Otherwise, it returns the config defined data_center.
        """
        if not data_center_variable:
            data_center_variable = 'DATACENTER'
        return Configurer.get_env_var(config, data_center_variable)

    @staticmethod
    def get_env_var(config, env_var_key):
        """ Returns the environment variable defined by env_var_key, if it's defined.
            Otherwise, it returns the config defined env_var_key.
        Raises:
            ValueError: if not found in either location
        """
        if not env_var_key:
            raise ValueError('env_var_key is required to be set')
        if env_var_key in os.environ:
            return os.environ[env_var_key]
        # Uses the config file's data if the environment is not setup.  Should only be for
        # local testing outside of the docker container
        if env_var_key not in config:
            raise ValueError('Cannot find {0} in the config file nor an environment variable'
                             .format(env_var_key))
        return config[env_var_key]
