""" Container for QueryMaker
"""


class QueryMaker(object):
    """ Static class that creates the MySQL queries for the module.
        Each method returns the table name, and the query string for that given method.

        This allows the table name to be converted into a test table, if need be for functional
        testing.

        Use with tools.query_handler.py
    """

    @staticmethod
    def get_test_query():
        """ Table and query are seperated in case the table name wants to be modified by adding
            `_test` to the end of the table name for functional testing.
        """
        table = 'test_table'
        query = ('INSERT INTO {0} (`test_column`, `test_other_name`, `test_flag`) '
                 'VALUES (%(test_column)s, %(test_other_name)s, %(test_flag)s')
        return {
            'table': table,
            'query': query
        }
