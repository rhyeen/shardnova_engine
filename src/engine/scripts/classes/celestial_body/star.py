""" Container for <I> Star
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class Star(CelestialBody):

    def _get_unique_name(self):
        return self._data_handler.get_unique_name('star')

    def __str__(self):
        return 'Star: {0}'.format(self.get_name())
