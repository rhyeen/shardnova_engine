""" Container for MysqlManipulator
"""
import json
from tools.configurer import Configurer


class MysqlManipulator(object):
    """ Used to manipulate the database in more manual ways while abstracting away the MySQL calls.
    """
    mysql = None

    """ @WARNING: Setting _IS_TEST to anything but True could result in a complete wipe of your
        real tables.
        Set to false at your own risk:
        Doing so would cause the database calls to be made on the real tables instead of the test
        tables.
    """
    _IS_TEST = True

    def __init__(self, config):
        """ Sets up class with the given config file
        """
        Configurer.check_config_object(config)
        self.mysql = Configurer.connect_mysql(config)

    def clear_table(self, table_name):
        """ Truncates the given table_name
        """
        cursor = self.mysql.cursor()
        cursor.execute(self._get_clear_table_query(table_name))

    def _get_clear_table_query(self, table):
        """ Returns a query to truncate the given table
        """
        if self._IS_TEST:
            table += '_test'
        return 'TRUNCATE TABLE `{0}`'.format(table)

    def drop_table(self, table_name):
        """ Drops the given table_name
        """
        cursor = self.mysql.cursor()
        cursor.execute(self._get_drop_table_query(table_name))

    def _get_drop_table_query(self, table):
        """ Returns a query to drop the given table
        """
        if self._IS_TEST:
            table += '_test'
        return 'DROP TABLE IF EXISTS `{0}`'.format(table)

    def add_entry_to_table(self, table_name, values, columns):
        """ Inserts a new row into the given table_name with the given values' index matching the
            given columns' index.
        """
        cursor = self.mysql.cursor()
        params = {}
        for index, column in enumerate(columns):
            value = values[index]
            if isinstance(value, dict):
                value = json.dumps(value)
            params[column] = value
        cursor.execute(self._get_add_entry_query(table_name, columns), params)
        self.mysql.commit()

    def _get_add_entry_query(self, table, columns):
        """ Returns a query for inserting the given values at the given columns into the given
            table.
        """
        if self._IS_TEST:
            table += '_test'
        column_expression = "(`{0}`)".format("`,`".join(columns))
        value_params = []
        for column in columns:
            value_params.append('%({0})s'.format(column))
        value_expression = '({0})'.format(','.join(value_params))
        return 'INSERT INTO `{0}` {1} VALUES {2}'.format(table,
                                                         column_expression,
                                                         value_expression)

    def add_dict_entry_to_table(self, table_name, entry):
        """ Inserts a new row into the given table_name with the given entry.
            Entry is of the following format:
            {
                'name_of_column1': 'value_for_column1',
                'name_of_column2': 'value_for_column2'
            }
        """
        columns = []
        values = []
        for key, value in entry.items():
            columns.append(key)
            values.append(value)
        self.add_entry_to_table(table_name, values, columns)

    def add_dict_entries_to_table(self, table_name, entries):
        """ Inserts all the given entries into the given table_name.  Entries is an array of
            Entry objects (see add_dict_entry_to_table())
        """
        for entry in entries:
            self.add_dict_entry_to_table(table_name, entry)

    def get_table_entries(self, table_name, conditions=None):
        """ Returns a dict with table rows that satisfy ALL (not ANY) of the conditions given.
            If no conditions are given, it will return all entries in the table.
        Args:
            table_name (STRING): Name of the table in the database.  Do not add '_test': this is
            inferred by the config file.
            conditions (DICT, optional): Dict of keys (being the column name in table), and values.
        """
        cursor = self.mysql.cursor()
        cursor.execute(self._get_table_entries_query(table_name, conditions))
        return cursor.fetchall()

    def _get_table_entries_query(self, table, conditions):
        """ Returns a query for selecting table rows that satisfy ALL of the conditions given.
        """
        if self._IS_TEST:
            table += '_test'
        conditional = ''
        conditionals = []
        if conditions:
            for key, value in conditions.items():
                conditionals.append('`{0}` = {1}'.format(key, value))
            conditional = ' WHERE {0}'.format(' AND '.join(conditionals))
        return 'SELECT * FROM `{0}` {1}'.format(table, conditional)

    def run_query(self, query, table=None):
        if table:
            if self._IS_TEST:
                table += '_test'
            query = query.format(table)
        cursor = self.mysql.cursor()
        cursor.execute(query)
        return cursor.fetchall()
