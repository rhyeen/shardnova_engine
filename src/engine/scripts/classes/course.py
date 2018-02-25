""" Container for Course
"""


class Course(object):

    def __init__(self, drone, target_distance_from_system_center):
        self.__drone = drone
        self.__destination_distance = target_distance_from_system_center
        self.__destination_distance_name = self.__get_destination_name()
        self.__distance_to_destination = self.__get_distance_to_destination()
        self.__paused = False

    def __str__(self):
        return 'On course to {1}'.format(self.__distance_to_destination, self.__destination_distance_name)

    def __get_destination_name(self):
        celestial_body = self.__drone.coordinates.system.get_celestial_body_at_distance(self.__destination_distance)
        if celestial_body is None:
            return '{0:0.1f} pus'.format(self.__destination_distance)
        return celestial_body

    def __get_distance_to_destination(self):
        drone_distance_from_center = self.__drone.coordinates.distance_from_center
        return abs(drone_distance_from_center - self.__destination_distance)

    def get_destination_distance_from_center(self):
        return self.__destination_distance

    def is_finished(self):
        return self.__distance_to_destination == 0

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
            return 0
        return self.__decrement_distance()

    def __decrement_distance(self):
        distance_per_tick = self.__drone.get_distance_per_tick()
        self.__distance_to_destination -= distance_per_tick
        if self.__distance_to_destination > 0:
            return distance_per_tick
        distance_traveled = distance_per_tick + self.__distance_to_destination
        self.__distance_to_destination = 0
        return distance_traveled

    def get_distance_to_destination(self):
        return self.__distance_to_destination

    def get_destination(self):
        return self.__destination_distance_name

    def get_distance_per_tick(self):
        return self.__drone.get_distance_per_tick()

    def get_required_fuel_for_course(self):
        fuel_per_distance = self.__drone.get_fuel_per_distance()
        return fuel_per_distance * self.get_distance_to_destination()
