""" Container for DroneWarehouse
"""
from scripts.classes.drone.probe_drone import ProbeDrone


class DroneWarehouse(object):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__active_drones = []
        self.__inactive_drones = []
        self.__killed_drones = []

    def get_active_drones(self):
        return self.__active_drones

    def get_inactive_drones(self):
        return self.__inactive_drones

    def get_killed_drones(self):
        return self.__killed_drones

    def add_drone(self, drone):
        self._add_drone(self.__inactive_drones, drone)

    def __drone_exists(self, group, drone):
        return self.__get_drone_index(group, drone) is not None

    @staticmethod
    def __get_drone_index(group, drone):
        for index, __drone in enumerate(group):
            if (__drone.get_id() == drone.get_id()):
                return index
        return None

    def __add_drone(self, group, drone):
        if (self.__drone_exists(self.__inactive_drones, drone) or
                self.__drone_exists(self.__active_drones, drone) or
                self.__drone_exists(self.__killed_drones, drone)):
            return
        group.append(drone)

    def deactivate_drone(self, drone):
        if not self.__drone_exists(self.__active_drones, drone):
            raise ValueError('{0} is not an active drone.'.format(drone))
        self.__move_drone(self.__active_drones, self.__inactive_drones, drone)

    def __move_drone(self, old_group, new_group, drone):
        self.__remove_drone(old_group, drone)
        self.__add_drone(new_group, drone)

    def __remove_drone(self, group, drone):
        remove_index = self.__get_drone_index(group, drone)
        if remove_index is not None:
            del group[remove_index]

    def activate_drone(self, drone):
        if not self.__drone_exists(self.__inactive_drones, drone):
            raise ValueError('{0} is not an inactive drone.'.format(drone))
        self.__move_drone(self.__inactive_drones, self.__active_drones, drone)

    def kill_drone(self, drone):
        if self.__drone_exists(self.__active_drones, drone):
            self.__move_drone(self.__active_drones, self.__killed_drones, drone)
        elif self.__drone_exists(self.__inactive_drones, drone):
            self.__move_drone(self.__inactive_drones, self.__killed_drones, drone)
        else:
            raise ValueError('{0} is not an active or inactive drone.'.format(drone))

    def load_file(self, game_file, universe):
        self.__load_drone_group(game_file['activeDrones'], self.__active_drones, universe)
        self.__load_drone_group(game_file['inactiveDrones'], self.__inactive_drones, universe)
        self.__load_drone_group(game_file['killedDrones'], self.__killed_drones, universe)

    def __load_drone_group(self, game_file, group, universe):
        for drone_file in game_file:
            drone_type = drone_file['type']
            if drone_type == 'probe':
                drone = ProbeDrone(self.__data_handler)
            else:
                raise ValueError('Drone of type "{0}" unsupported'.format(drone_type))
            drone.load_file(drone_file, universe)
            self.__add_drone(group, drone)
