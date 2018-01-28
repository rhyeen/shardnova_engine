""" Container for <I> StartingFactory
"""
from scripts.classes.celestial_body.celestial_body import CelestialBody


class StartingFactory(CelestialBody):

    def _get_unique_name(self):
        return 'UF Deep Space Factory'
