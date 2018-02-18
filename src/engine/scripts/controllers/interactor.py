""" Container for Interactor
"""
from scripts.facades.user import User
from scripts.classes.course import Course


class Interactor(object):

    def __init__(self, data_handler, game):
        """ game must come preloaded
        """
        self.__data_handler = data_handler
        self.__game = game

    def initialize_game(self):
        self.__game.initialize_game()

    def create_phone_user(self, phone, output_handler):
        user = User(self.__data_handler, output_handler)
        user.set_primary_phone(phone)
        is_new_user = self.__game.new_user(user)
        if is_new_user:
            user.output_handler.welcome()
        return user

    def get_map(self, user, drone):
        galaxy = drone.coordinates.galaxy
        sector = drone.coordinates.sector
        system = drone.coordinates.system
        if drone.coordinates.on_course():
            source = drone.coordinates.get_course().get_source()
            destination = drone.coordinates.get_course().get_destination()
            user.output_handler.show_on_course_map(galaxy, sector, system, source, destination)
        else:
            celestial_body = drone.coordinates.get_celestial_body()
            user.output_handler.show_map(galaxy, sector, system, celestial_body)

    def set_course(self, user, drone, destination_index):
        celestial_body = self.__get_celestial_body(drone, destination_index)
        if celestial_body is None:
            user.output_handler.invalid_index(destination_index)
        course = Course(drone, celestial_body)
        fuel_use = course.get_required_fuel_for_course()
        if fuel_use > drone.fuel:
            user.output_handler.insufficient_fuel(celestial_body, fuel_use, drone.fuel)
            return
        drone.coordinates.set_course(course)
        self.check_course(user, drone, fuel_use)

    def __get_celestial_body(self, drone, destination_index):
        if destination_index < 0:
            return None
        celestial_bodies = drone.coordinates.system.get_celestial_bodies()
        if destination_index >= len(celestial_bodies):
            return None
        return celestial_bodies[destination_index]

    def check_course(self, user, drone, fuel_use=None):
        course = drone.coordinates.get_course()
        if course is None:
            user.output_handler.no_course()
            return
        celestial_body = course.get_destination()
        distance_to_destination = course.get_distance_to_destination()
        distance_per_tick = course.get_distance_per_tick()
        ticks_to_finished = distance_to_destination / distance_per_tick
        if fuel_use is None:
            user.output_handler.check_course(celestial_body, distance_to_destination, ticks_to_finished, drone.fuel)
            return
        user.output_handler.on_course(fuel_use, drone.fuel, celestial_body, distance_to_destination, ticks_to_finished)
