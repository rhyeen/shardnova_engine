""" Container for <I> Beacon
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class Beacon(CelestialBody):

    def _get_unique_name(self):
        return self._data_handler.get_unique_name('beacon')

    def __str__(self):
        return 'Beacon: {0}'.format(self.get_name())

    def _load_file_specifics(self, game_file):
        pass
