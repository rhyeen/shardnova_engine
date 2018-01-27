""" Container for Coordinates
"""


class Coordinates(object):

    def __init__(self):
        self.__galaxy = None
        self.__sector = None
        self.__system = None
        self.__celestial_body = None
        self.__course = None

    def set_galaxy(self, galaxy):
        self.__galaxy = galaxy

    def get_galaxy(self):
        return self.__galaxy

    def set_sector(self, sector):
        self.__sector = sector

    def get_sector(self):
        return self.__sector

    def set_system(self, system):
        self.__system = system

    def get_system(self):
        return self.__system

    def at_celestial_body(self):
        return self.__celestial_body is not None

    def set_celestial_body(self, celestial_body):
        self.__celestial_body = celestial_body
        self.__course = None

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
        if self.__course is None:
            return
        self.__course.tick()
        if not self.__course.is_finished():
            return
        self.set_celestial_body(self.__course.get_destination())
