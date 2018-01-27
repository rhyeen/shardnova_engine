""" Container for Course
"""


class Course(object):

    def __init__(self, drone, destination_celestial_body):
        self.__drone = drone
        self.__destination = destination_celestial_body
        self.__source = self.__get_source()
        self.__distance_to_destination = self.__get_distance_to_destination()
        self.__distance_traveled_per_tick = self.__get_distance_traveled_per_tick()
        self.__finished = False

    def __get_source(self):
        coordinates = self.__drone.get_coordinates()
        if coordinates.at_celestial_body():
            return coordinates.get_celestial_body()
        else:
            course = coordinates.get_course()
            return course.get_source()

    def __get_distance_to_destination(self):
        coordinates = self.__drone.get_coordinates()
        distance = self.__get_distance_to_celestial_body(self.__source, self.__destination)
        if coordinates.at_celestial_body():
            return distance
        # Otherwise, coordinates.on_course = True
        course = coordinates.get_course()
        source = course.get_source()
        destination = course.get_destination()
        course_left = course.get_distance_to_destination()
        course_total_distance = self.__get_distance_to_celestial_body(source, destination)
        course_traveled = course_total_distance - course_left
        if self.__course_requires_u_turn(source, destination):
            # If we make a u-turn, the original course's destination should act as this course's
            # source to ensure that if a course correction happens again, we don't leap
            # space.
            self.__source = destination
            return distance + course_traveled
        else:
            return distance - course_traveled

    def __course_requires_u_turn(self, course_source, course_destination):
        distance_to_course_source = self.__get_distance_to_celestial_body(self.__destination, course_source)
        distance_to_course_destination = self.__get_distance_to_celestial_body(self.__destination, course_destination)
        return distance_to_course_destination > distance_to_course_source

    def __get_distance_to_celestial_body(self, source, destination):
        coordinates = self.__drone.get_coordinates()
        system = coordinates.get_system()
        return system.get_distance_between_celestial_bodies(source, destination)

    def get_destination(self):
        return self.__destination

    def is_finished(self):
        return self.__finished

    def tick(self):
        self.__decrement_distance()
        self.__finished = self.__distance_to_destination == 0

    def __decrement_distance(self):
        self.__distance_to_destination -= self.__distance_traveled_per_tick
        if self.__distance_to_destination < 0:
            self.__distance_to_destination = 0

    def get_distance_to_destination(self):
        return self.__distance_to_destination
