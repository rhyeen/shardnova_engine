""" Container for <I> AsteroidBelt
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class AsteroidBelt(CelestialBody):

    def _get_unique_name(self):
        return self._data_handler.get_unique_name('asteroid_belt')

    def __str__(self):
        return 'Asteroid belt: {0}'.format(self.get_name())
