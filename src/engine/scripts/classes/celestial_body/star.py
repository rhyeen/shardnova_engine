""" Container for <I> Star
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class Star(CelestialBody):

    def _get_unique_name(self):
        return self._data_handler.get_unique_name('star')
