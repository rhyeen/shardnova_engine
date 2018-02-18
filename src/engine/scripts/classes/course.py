""" Container for Course
"""


class Course(object):

    def __init__(self, drone, destination_celestial_body):
        self.__drone = drone
        self.__destination = destination_celestial_body
        self.__source = self.__get_source()
        self.__distance_to_destination = self.__get_distance_to_destination()
        self.__finished = False
        self.__paused = False

    def __str__(self):
        return '{0} --> {1} :: {2} pu'.format(self.__source, self.__destination, self.__distance_to_destination)

    def __get_source(self):
        coordinates = self.__drone.coordinates
        if coordinates.at_celestial_body():
            return coordinates.get_celestial_body()
        else:
            course = coordinates.get_course()
            return course.get_source()

    def __get_distance_to_destination(self):
        coordinates = self.__drone.coordinates
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
        coordinates = self.__drone.coordinates
        system = coordinates.system
        return system.get_distance_between_celestial_bodies(source, destination)

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def is_finished(self):
        return self.__finished

    def is_paused(self):
        return self.__paused

    def pause_course(self):
        self.__paused = True

    def resume_course(self):
        if self.__drone.fuel < self.get_required_fuel_for_course():
            return False
        self.__paused = False
        return True

    def tick(self):
        if self.__paused:
            return
        self.__decrement_distance()
        self.__finished = self.__distance_to_destination == 0

    def __decrement_distance(self):
        self.__distance_to_destination -= self.__drone.get_distance_per_tick()
        if self.__distance_to_destination < 0:
            self.__distance_to_destination = 0

    def get_distance_to_destination(self):
        return self.__distance_to_destination

    def get_distance_per_tick(self):
        return self.__drone.get_distance_per_tick()

    def get_required_fuel_for_course(self):
        fuel_per_distance = self.__drone.get_fuel_per_distance()
        return fuel_per_distance * self.__get_distance_to_destination()
