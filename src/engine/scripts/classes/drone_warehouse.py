""" Container for DroneWarehouse
"""


class DroneWarehouse(object):

    def __init__(self):
        self.__active_drones = []
        self.__inactive_drones = []
        self.__killed_drones = []
        self.__primary_drone = None

    def get_active_drones(self):
        return self.__active_drones

    def get_inactive_drones(self):
        return self.__inactive_drones

    def get_killed_drones(self):
        return self.__killed_drones

    def add_drone(self, drone):
        if (self.__drone_exists(self.__inactive_drones, drone) or
                self.__drone_exists(self.__active_drones, drone) or
                self.__drone_exists(self.__killed_drones, drone)):
            return
        self.__add_drone(self.__inactive_drones, drone)

    def __drone_exists(self, group, drone):
        return self.__get_drone_index(group, drone) is not None

    def __add_drone(group, drone):
        group.append(drone)

    def deactivate_drone(self, drone):
        if not self.__drone_exists(self.__active_drones, drone):
            raise ValueError('Drone {0} is not an active drone.'.format(drone.get_id()))
        self.__move_drone(self.__active_drones, self.__inactive_drones, drone)

    def __move_drone(self, old_group, new_group, drone):
        self.__remove_drone(old_group, drone)
        self.__add_drone(new_group, drone)

    def __remove_drone(self, group, drone):
        remove_index = self.__get_drone_index(group, drone)
        if remove_index is not None:
            del group[remove_index]

    def __get_drone_index(group, drone):
        for index, grouped_drone in enumerate(group):
            if (grouped_drone.get_id() == drone.get_id()):
                return index
        return None

    def activate_drone(self, drone):
        if not self.__drone_exists(self.__inactive_drones, drone):
            raise ValueError('Drone {0} is not an inactive drone.'.format(drone.get_id()))
        self.__move_drone(self.__inactive_drones, self.__active_drones, drone)

    def kill_drone(self, drone):
        if self.__drone_exists(self.__active_drones, drone):
            self.__move_drone(self.__active_drones, self.__killed_drones, drone)
        elif self.__drone_exists(self.__inactive_drones, drone):
            self.__move_drone(self.__inactive_drones, self.__killed_drones, drone)
        else:
            raise ValueError('Drone {0} is not an active or inactive drone.'.format(drone.get_id()))
