""" Container for Coordinates
"""


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
