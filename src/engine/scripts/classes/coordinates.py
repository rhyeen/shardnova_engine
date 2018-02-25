""" Container for Coordinates
"""
from scripts.classes.course import Course


class Coordinates(object):

    def __init__(self, distance_from_center=None):
        self.galaxy = None
        self.sector = None
        self.system = None
        self.__celestial_body = None
        self.__course = None
        self.distance_from_center = distance_from_center

    def __str__(self):
        if self.at_celestial_body():
            return 'Currently orbiting {0}'.format(self.__celestial_body)
        elif self.on_course():
            return '{0}'.format(self.__course)
        else:
            return 'At {0:0.1f} pus'.format(self.distance_from_center)

    def at_celestial_body(self):
        return self.__celestial_body is not None

    def set_celestial_body(self, distance_from_center):
        self.__celestial_body = self.system.get_celestial_body_at_distance(distance_from_center)
        self.__course = None
        self.distance_from_center = distance_from_center

    def get_celestial_body(self):
        return self.__celestial_body

    def set_course(self, course):
        self.__course = course
        if self.__course.is_finished():
            self.distance_from_center = self.__course.get_destination_distance_from_center()
            self.__celestial_body = self.system.get_celestial_body_at_distance(self.distance_from_center)
            self.__course = None
            return
        self.__celestial_body = None

    def get_course(self):
        return self.__course

    def on_course(self):
        return self.__course is not None

    def tick(self):
        if not self.on_course():
            return 0, None
        distance_traveled = self.__course.tick()
        course = self.__course
        if self.__course.is_finished():
            self.set_celestial_body(self.__course.get_destination_distance_from_center())
        self.__update_distance_from_center()
        return distance_traveled, course

    def __update_distance_from_center(self):
        if self.__course is None:
            return
        destination = self.__course.get_destination_distance_from_center()
        distance_to_destination = self.__course.get_distance_to_destination()
        # traveling away from the system center
        if self.distance_from_center < destination:
            self.distance_from_center = destination - distance_to_destination
        # traveling towards the system center
        else:
            self.distance_from_center = destination + distance_to_destination

    def load_file(self, game_file, universe, drone):
        self.galaxy = universe.get_galaxy(game_file['galaxy'])
        self.sector = self.galaxy.get_sector(game_file['sector'])
        self.system = self.sector.get_system(game_file['system'])
        self.distance_from_center = game_file['distanceFromSystemCenter']
        if 'course' in game_file and game_file['course'] is not None:
            course = Course(drone, game_file['course']['targetDistanceFromSystemCenter'])
            self.set_course(course)
            return
        self.set_celestial_body(self.distance_from_center)
