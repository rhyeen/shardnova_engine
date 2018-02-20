""" Container for Coordinates
"""
from scripts.classes.course import Course


class Coordinates(object):

    def __init__(self):
        self.galaxy = None
        self.sector = None
        self.system = None
        self.__celestial_body = None
        self.__course = None

    def __str__(self):
        if self.at_celestial_body():
            return 'At: {0}'.format(self.__celestial_body)
        else:
            return 'Course: {0}'.format(self.__course)

    def at_celestial_body(self):
        return self.__celestial_body is not None

    def set_celestial_body(self, celestial_body):
        self.__celestial_body = celestial_body
        course = self.__course
        self.__course = None
        return course

    def get_celestial_body(self):
        return self.__celestial_body

    def set_course(self, course):
        self.__course = course
        self.__celestial_body = None

    def get_course(self):
        return self.__course

    def on_course(self):
        return self.__course is not None

    def tick(self):
        if not self.on_course():
            return False, None
        self.__course.tick()
        if not self.__course.is_finished():
            return False, None
        course = self.set_celestial_body(self.__course.get_destination())
        return True, course

    def load_file(self, game_file, universe, drone=None):
        self.galaxy = universe.get_galaxy(game_file['galaxy'])
        self.sector = self.galaxy.get_sector(game_file['sector'])
        self.system = self.sector.get_system(game_file['system'])
        if 'celestialBody' in game_file and game_file['celestialBody'] is not None:
            celestial_body = self.sector.get_celestial_body(game_file['celestialBody'])
            self.set_celestial_body(celestial_body)
            return
        if drone is None:
            raise ValueError('Coordinates is expecting a course, but there is no drone for the course.')
        destination = self.system.get_celestial_body(game_file['course']['destination'])
        source = self.system.get_celestial_body(game_file['course']['source'])
        distance_to_destination = game_file['course']['distanceToDestination']
        course = Course(drone, destination, source, distance_to_destination)
        self.set_course(course)
