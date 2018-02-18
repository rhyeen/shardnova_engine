""" Container for QueryHandler
"""
import os
from time import sleep
import pymysql.cursors

class QueryHandler(object):
    """ Handles the oddities of mysqldb such as multistatement transactions, auto commits, and
        retry logic when connection goes down.
    """

    def __init__(self, environment, mysql=None):
        """ Sets up the class with the given environment
        Args:
            environment (STR): environment in which the script is running: local, stage, prod, test
        """
        self.environment = environment
        self._is_test = self._is_test_run()
        if mysql:
            self.mysql = mysql
        else:
            self.mysql = self._connect_mysql()

    def _is_test_run(self):
        if not self.environment:
            return False
        return self.environment == 'test'

    def _connect_mysql(self):
        """ Configures MySQL object, starts a connection on that object
            and returns it.
        Raises:
            Exception: If environment variables and config cannot create a mysql connection, an
            exception will be raised.
        """
        host, user, password, database, port = self._get_mysql_options()
        mysql = pymysql.connect(host=host,
                                user=user,
                                passwd=password,
                                db=database,
                                port=port,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        return mysql

    def _get_mysql_options(self):
        return self._get_mysql_options_from_env_var()

    @staticmethod
    def _get_mysql_options_from_env_var():
        host = os.environ['MYSQL_HOST']
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        database = os.environ['MYSQL_DATABASE']
        port = int(os.environ['MYSQL_PORT'])
        return host, user, password, database, port


    def get_query_results(self, query_function, params=None, query_function_args=None):
        """ Returns the results of the returned query_dict generated from the given query_function
            Results are passed back as dict.
            If query_function results in a multistatement transaction, the transaction is handled
            one statement at a time.
            If the mysql_db connection has timed out, it will reconnect.
            The transaction will forcefully be committed.
        Args:
            query_function (FUNCTION): a function that has zero or one parameter. If one parameter,
                the given query_function_args is a passed.  The function must return a dict of the
                format:
                {
                    'table': table,  # optional property. If given, assumes query has a ready `{0}`
                        or `{}` contained in the string to replace with the table.
                    'query': query  # query string
                }
        Raises:
            Exception: if a statement in a multistatement transaction fails, an error of the
            failure is given with additional information about what part of the transaction
            failed.  Otherwise, a standard mysqldb error is thrown.
        """
        query = self._get_query(query_function, query_function_args)
        return self._safe_execute(query, params)

    @staticmethod
    def _key_value_fetchall(cursor):
        """ pymysql cursorclass=pymysql.cursors.DictCursor, so we can just fetchall
        """
        return cursor.fetchall()

    def _safe_execute(self, query, params):
        """ During long processing times, the MySQL server will go away
            if not touched for several seconds.
            If this happens, we want to create a new connection.
            Otherwise, the connection is good and we execute as normal.

            Additionally, Python DB API cannot handle multistatement transactions. So we
            split and handle them sequentially. If any statement fails, the transaction does not
            continue.  However, there is no rollback.  Instead, a detailed error is thrown.

        Raises:
            Exception: if a statement in a multistatement transaction fails, an error of the
            failure is given with additional information about what part of the transaction
            failed.
        """
        statements = self._split_multistatement_transactions(query)
        number_of_statements = len(statements)
        for index, statement in enumerate(statements):
            try:
                if number_of_statements <= 1:
                    return self._safe_execute_statement(statement, params)
                self._safe_execute_statement(statement, params)
            except Exception as exception:
                if number_of_statements <= 1:
                    raise exception
                error = ('Statement {0}/{1} in the transaction failed.\n'
                         'Statement: {2}\nTransaction: {3}\nError: {4}'
                         .format(index + 1, number_of_statements, statement, query, exception))
                raise Exception(error)
        return None

    def _split_multistatement_transactions(self, query):
        """ If the given query is a multistatement transaction, split the query and return
            only the executable statements in order.

            Assumes ; is not contained within statements.
            Assumes query is not a tested transaction.
            Assumes multistatement starts with `START TRANSACTION;` and ends with `COMMIT`
        """
        if not self._has_transaction_indicators(query):
            return [query]
        # @ASSERT: ";" is no where else in MySQL query besides delimiting statements
        # This does not include possible escaped parameter values.
        statements = query.split(';')
        # @NOTE: expecting at least three statements if multistatement: START; STATEMENT; COMMIT;
        if len(statements) < 3:
            return [query]
        while len(statements) > 0 and not self._has_transaction_indicators(statements.pop(0)):
            pass
        while len(statements) > 0 and not self._has_transaction_indicators(statements.pop(-1)):
            pass
        if len(statements) < 1:
            return [query]
        # @ASSERT: there isn't nested transactions within the given transaction query.
        return statements

    @staticmethod
    def _has_transaction_indicators(statement):
        """ Returns true if statement is a transaction indicator.  False otherwise.
        """
        begin_transaction_indicators = ['START TRANSACTION', 'BEGIN']
        end_transaction_indicators = ['COMMIT']
        for begin_transaction_indicator in begin_transaction_indicators:
            if begin_transaction_indicator in statement:
                return True
        for end_transaction_indicator in end_transaction_indicators:
            if end_transaction_indicator in statement:
                return True
        return False

    def _safe_execute_statement(self, statement, params):
        """ Executes and commits the statement.  If connection has gone away, reconnects and tries
            to execute again.
        """
        try:
            with self.mysql.cursor() as cursor:
                cursor.execute(statement, params)
                self.mysql.commit()
                return self._key_value_fetchall(cursor)
        except:
            try:
                self.mysql.close()
            except:
                pass
            try:
                self.mysql = Configurer.connect_mysql(self.config)
                with self.mysql.cursor() as cursor:
                    cursor.execute(statement, params)
                    self.mysql.commit()
                    return self._key_value_fetchall(cursor)
            # @DEBUG: this is particularly a MySQLdb.OperationalError error, but I get an error
            # when trying to reference OperationalError
            except:
                # @NOTE: at this point, it is most likely due to switching MySQL server nodes,
                # ("WSREP has not yet prepared node for application use") which
                # can cause disruption for a few seconds as the DNS resolves to the new node.
                # Waiting a minute should be more than enough time.
                try:
                    self.mysql.close()
                except:
                    pass
                sleep(60)
                self.mysql = Configurer.connect_mysql(self.config)
                with self.mysql.cursor() as cursor:
                    cursor.execute(statement, params)
                    self.mysql.commit()
                    return self._key_value_fetchall(cursor)

    def _get_query(self, query_function, query_function_args=None):
        """ Converts the given query_function return values into a MySQL string query.
            Returned object has the table name ('table') and the query string ('query').
            The query string will have a '{0}', ready for the table name to be injected into
            query string.
            The table name can be modified to include '_test', if it is a testing environment.

            If the resulting query potentially has several tables it queries against, the returned
            query string will not contain '{0}'.  Instead, it is expected to pass
            query_function_args as a dict with at least an entry of 'is_test': self._is_test.
            It is expected of the query_function to append '_test', as needed.
        Args:
            query_function (FUNCTION)
            query_function_args (DICT, optional): If given, passes the dict to the given
                query_function.  This is useful if queries need to be dynamically formatted.
        """
        if query_function_args is None:
            query_obj = query_function()
        else:
            query_obj = query_function(query_function_args)
        if 'table' in query_obj:
            if self._is_test:
                query_obj['table'] += '_test'
            return query_obj['query'].format(query_obj['table'])
        else:
            return query_obj['query']
