""" Container for DateFormatter
"""
from datetime import datetime, timedelta
import calendar

class DateFormatter(object):
    """ For simple date manipulation.  Wrapper around typical datetime methods for functions
        written 90% if the time in code anyway.

        See individual public functions for more details.
    """
    constants = {
        'default_date_format': '%Y-%m-%d %H:%M:%S'
    }

    def __init__(self, test_config=None):
        self._datetime = None
        self._date_formats = None
        self._test_config = test_config
        self.set_datetime()

    def get_datetime(self):
        """ Returns the class-defined datetime object. If set_datetime() is not called, it is
            the timestamp of when the class was initialized.
        """
        if self._datetime:
            return self._datetime
        self.set_datetime()
        return self._datetime

    def set_datetime(self, given_date=None):
        """ Set the class-defined datetime object to the given_date.

            If given_date is not provided, it will set the datetime to the UTC current timestamp.
        """
        if not given_date:
            given_date = datetime.utcnow()
        self._datetime = given_date

    def get_datetime_object(self, string_datetime=None, string_datetime_format=None):
        """ Given the string_datetime and the string_datetime_format, return a datetime object.

            If string_datetime is not provided, the datetime upon the class initialization is
            returned (unless overwritten by calling set_datetime(),
            in which case the override is used).

            If string_datetime_format is not provided, the default of '%Y-%m-%d %H:%M:%S is used.
        """
        if not string_datetime:
            return self.get_datetime()
        if not string_datetime_format:
            string_datetime_format = self._get_default_date_format()
        return datetime.strptime(string_datetime, string_datetime_format)

    def get_datetime_string(self, given_datetime=None, string_datetime_format=None):
        """ Given the given_datetime and the string_datetime_format, return a datetime string.

            If given_datetime is not provided, the datetime upon the class initialization is used
            (unless overwritten by calling set_datetime(), in which case the override is used).

            If string_datetime_format is not provided, the default of '%Y-%m-%d %H:%M:%S is used.
        """
        if not given_datetime:
            given_datetime = self.get_datetime()
        if not string_datetime_format:
            string_datetime_format = self._get_default_date_format()
        return given_datetime.strftime(string_datetime_format)

    def get_day_of_week(self, given_date=None):
        """ Returns the day of the week as "Monday"-"Sunday" of the given_date.

            If given_date is not provided, it will use the class-defined datetime object.
        """
        if not given_date:
            given_date = self.get_datetime()
        return calendar.day_name[given_date.weekday()]

    def modify_date(self, given_date=None, weeks=0, days=0, hours=0, minutes=0):
        """ Modify the given date by the given number of weeks, days, hours, and/or minutes.
        """
        if not given_date:
            given_date = self.get_datetime()
        return given_date + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)

    def zero_out_time(self, given_date=None):
        if not given_date:
            given_date = self.get_datetime()
        return given_date.replace(hour=0, minute=0, second=0, microsecond=0)

    def _get_default_date_format(self):
        return self.constants['default_date_format']
