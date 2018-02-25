""" Container for Interactor
"""
from scripts.facades.user import User
from scripts.classes.course import Course
from scripts.classes.signal.distress_signal import DistressSignal


class Interactor(object):

    def __init__(self, data_handler, game):
        """ game must come preloaded
        """
        self.data_handler = data_handler
        self.__game = game

    def initialize_game(self):
        self.__game.initialize_game()

    def load_game_file(self, game_file):
        self.__game.load_game_file(game_file)

    def create_phone_user(self, phone, output_handler):
        user = User(self.data_handler, output_handler)
        user.set_primary_phone(phone)
        is_new_user = self.__game.new_user(user)
        if is_new_user:
            user.output_handler.welcome()
        return user

    def get_map(self, user, drone):
        user.output_handler.show_map(drone.coordinates)

    def set_course(self, user, drone, destination_index):
        celestial_body = self.__get_celestial_body(drone, destination_index)
        if celestial_body is None:
            user.output_handler.invalid_index(destination_index)
            return
        course = Course(drone, self.__get_celestial_body_distance(drone, celestial_body))
        fuel_use = course.get_required_fuel_for_course()
        if fuel_use > drone.fuel:
            user.output_handler.insufficient_fuel(celestial_body, fuel_use, drone.fuel)
            return
        drone.coordinates.set_course(course)
        distance_to_destination = course.get_distance_to_destination()
        distance_per_tick = course.get_distance_per_tick()
        ticks_to_finished = distance_to_destination / distance_per_tick
        if fuel_use == 0:
            user.output_handler.already_at_course_desintation(celestial_body)
            return
        user.output_handler.on_course(fuel_use, drone.fuel, celestial_body, distance_to_destination, ticks_to_finished)

    def __get_celestial_body_distance(self, drone, celestial_body):
        return drone.coordinates.system.get_distance_from_center(celestial_body)

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
        user.output_handler.check_course(celestial_body, distance_to_destination, ticks_to_finished, drone.fuel)

    def send_distress_signal(self, user, distress_signal):
        user.output_handler.send_distress_signal(distress_signal)
        self.__game.add_signal(distress_signal)

    def send_distress_response_offer(self, user, distress_response_offer):
        user.output_handler.send_distress_response_offer(distress_response_offer)
        self.__game.add_signal(distress_response_offer)

    def accept_distress_response_offer(self, user, distress_response_offer):
        user.output_handler.accept_distress_response_offer(distress_response_offer)

    def reject_distress_response_offer(self, user, distress_response_offer):
        user.output_handler.reject_distress_response_offer(distress_response_offer)

    def handle_dropped_distress_signal(self, user, distress_signal_id):
        distress_signal = DistressSignal(None, None)
        distress_signal.set_id(distress_signal_id)
        user.output_handler.distress_signal_dropped(distress_signal)
