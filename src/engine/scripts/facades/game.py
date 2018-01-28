""" Container for Game
"""
from scripts.classes.facades.universe import Universe
from scripts.classes.facades.users import Users
from scripts.classes.coordinates import Coordinates
from scripts.classes.drone.probe_drone import ProbeDrone


class Game(object):

    def __init__(self):
        self.universe = None
        self.users = None

    def initialize_game(self):
        self.universe = Universe()
        self.universe.generate()
        self.users = Users()

    def load_game(self, universe, users):
        self.universe = universe
        self.users = users

    def new_user(self, user):
        is_new_user = self.users.add_user(user)
        if not is_new_user:
            return False
        drone = ProbeDrone()
        user.character.drone_warehouse.add_drone(drone)
        user.character.drone_warehouse.activate_drone(drone)
        drone.coordinates = Coordinates()
        drone.coordinates.galaxy = self.universe.get_starting_galaxy()
        drone.coordinates.sector = self.universe.get_starting_sector()
        drone.coordinates.system = self.universe.get_starting_system()
        drone.coordinates.set_celestial_body(user.coordinates.system.get_tutorial_starting_point())
        return True

    def tick(self):
        self.users.tick()
