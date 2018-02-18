""" Container for Game
"""
from scripts.facades.universe import Universe
from scripts.facades.users import Users
from scripts.classes.coordinates import Coordinates
from scripts.classes.drone.probe_drone import ProbeDrone


class Game(object):

    def __init__(self, data_handler):
        self.universe = None
        self.users = None
        self.__data_handler = data_handler

    def initialize_game(self):
        self.universe = Universe(self.__data_handler)
        self.universe.generate()
        self.users = Users(self.__data_handler)

    def load_game_file(self, game_file):
        self.universe = Universe(self.__data_handler)
        self.universe.load_file(game_file['universe'])
        self.users = Users()
        self.users.load_file(game_file['users'], self.universe)

    def new_user(self, user):
        is_new_user = self.users.add_user(user)
        if not is_new_user:
            return False
        drone = ProbeDrone(self.__data_handler)
        drone.fuel = 20
        user.character.drone_warehouse.add_drone(drone)
        user.character.drone_warehouse.activate_drone(drone)
        drone.coordinates = Coordinates()
        drone.coordinates.galaxy = self.universe.get_starting_galaxy()
        drone.coordinates.sector = self.universe.get_starting_sector()
        drone.coordinates.system = self.universe.get_starting_system()
        drone.coordinates.set_celestial_body(drone.coordinates.system.get_tutorial_starting_point())
        return True

    def tick(self):
        self.users.tick()
