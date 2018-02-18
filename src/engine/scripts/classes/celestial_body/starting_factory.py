""" Container for <I> StartingFactory
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class StartingFactory(CelestialBody):

    def _get_unique_name(self):
        return 'UF Deep Space Factory'

    def __str__(self):
        return '{0}'.format(self.get_name())

    def _load_file_specifics(self, game_file):
        pass
