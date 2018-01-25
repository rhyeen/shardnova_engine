""" Container for FunctionalTestPopulator
"""

class FunctionalTestPopulator(object):

    @staticmethod
    def get_test_table_entries():
        entries = [
            {
                'some_column': 'some_value',
                'some_column2': None
            }
        ]

        return entries

    @staticmethod
    def get_test_file_content():
        entries = [
            [
                'some_cell_value',
                'some_cell_value2'
            ]
        ]

        return entries
