""" Container for System
"""
import random
from scripts.classes.orbital_plane import OrbitalPlane
from scripts.classes.celestial_body.star import Star
from scripts.classes.celestial_body.starting_factory import StartingFactory
from scripts.classes.satellite.hyperspace_gate import HyperspaceGate
from scripts.classes.celestial_body.beacon import Beacon
from scripts.classes.celestial_body.planet import Planet
from scripts.classes.celestial_body.asteroid_belt import AsteroidBelt


class System(object):

    max_celestial_bodies = 8
    max_orbital_distance = 20

    def __init__(self, data_handler, name=None):
        self.__data_handler = data_handler
        self.__orbital_plane = OrbitalPlane()
        self.__starting_factory = None
        if name is None:
            name = self.__get_unique_name()
        self.__name = name

    def __str__(self):
        return 'System: {0}'.format(self.get_name())

    def __get_unique_name(self):
        return self.__data_handler.get_unique_name('system')

    def get_name(self):
        return self.__name

    def get_celestial_bodies(self):
        return self.__orbital_plane.get_celestial_bodies()

    def get_celestial_body(self, name):
        return self.__orbital_plane.get_celestial_body(name)

    def get_distance_from_center(self, celestial_body):
        return self.__orbital_plane.get_distance_from_center(celestial_body)

    def get_distances(self, celestial_body):
        return self.__orbital_plane.get_distances(celestial_body)

    def get_distance_between_celestial_bodies(self, body1, body2):
        return self.__orbital_plane.get_distance_between_celestial_bodies(body1, body2)

    def get_celestial_body_at_distance(self, distance_from_center):
        return self.__orbital_plane.get_celestial_body_at_distance(distance_from_center)

    def generate(self):
        total = random.randint(1, self.max_celestial_bodies)
        self.__orbital_plane.push(Star(self.__data_handler))
        for index in range(total - 1):
            # @TODO: alter it to allow for different types of celestial bodies
            self.__orbital_plane.push(Planet(self.__data_handler), random.randint(1, self.max_orbital_distance))

    def set_as_tutorial(self):
        self.__orbital_plane = OrbitalPlane()
        self.__orbital_plane.push(Star(self.__data_handler))
        self.__orbital_plane.push(Planet(self.__data_handler), 8)
        self.__starting_factory = StartingFactory(self.__data_handler)
        self.__orbital_plane.push(self.__starting_factory, 2)
        beacon = Beacon(self.__data_handler)
        hyperspace_gate = HyperspaceGate(self.__data_handler)
        beacon.add_satellite(hyperspace_gate)
        self.__orbital_plane.push(beacon, 4)

    def get_tutorial_starting_point(self):
        return self.__orbital_plane.get_distance_from_center(self.__starting_factory)

    def load_file(self, game_file):
        self.__name = game_file['name']
        self.__orbital_plane = OrbitalPlane()
        for orbital_plane_file in game_file['orbitalPlane']:
            celestial_body = self.__load_file_celestial_body(orbital_plane_file['celestialBody'])
            if 'distanceToPrev' in orbital_plane_file:
                distance_to_previous = orbital_plane_file['distanceToPrev']
            else:
                distance_to_previous = None
            self.__orbital_plane.push(celestial_body, distance_to_previous)

    def __load_file_celestial_body(self, game_file):
        celestial_body_type = game_file['type']
        if celestial_body_type == 'star':
            celestial_body = Star(self.__data_handler)
        elif celestial_body_type == 'planet':
            celestial_body = Planet(self.__data_handler)
        elif celestial_body_type == 'beacon':
            celestial_body = Beacon(self.__data_handler)
        elif celestial_body_type == 'asteroidBelt':
            celestial_body = AsteroidBelt(self.__data_handler)
        elif celestial_body_type == 'startingFactory':
            celestial_body = StartingFactory(self.__data_handler)
            self.__starting_factory = celestial_body
        else:
            raise ValueError('Celestial body of type "{0}" unsupported'.format(celestial_body_type))
        celestial_body.load_file(game_file)
        return celestial_body
