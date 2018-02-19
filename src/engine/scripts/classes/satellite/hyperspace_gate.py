""" Container for <I> HyperspaceGate
"""
from scripts.classes.satellite.satellite import Satellite
from scripts.classes.jump_point import JumpPoint


class HyperspaceGate(Satellite):

    def __init__(self, data_handler):
        self.__jump_points = []
        super().__init__(data_handler)

    def get_jump_points(self):
        return self.__jump_points

    def add_jump_point(self, jump_point):
        if self.__jump_point_exists(jump_point):
            return
        self.__add_jump_point(jump_point)

    def __jump_point_exists(self, jump_point):
        return self.__get_jump_point_index(jump_point) is not None

    def __get_jump_point_index(self, jump_point):
        for index, __jump_point in enumerate(self.__jump_points):
            if __jump_point.get_name() == jump_point.get_name():
                return index
        return None

    def __add_jump_point(self, jump_point):
        self.__jump_points.append(jump_point)

    def remove_jump_point(self, jump_point):
        if not self.__jump_point_exists(jump_point):
            raise ValueError('{0} is not found.'.format(jump_point))
        index = self.__get_jump_point_index(jump_point)
        self.__remove_jump_point(index)

    def __remove_jump_point(self, jump_point_index):
        del self.__jump_points[jump_point_index]

    def _load_file_specifics(self, game_file):
        for jump_point_file in game_file['jumpPoints']:
            jump_point = JumpPoint(self._data_handler)
            jump_point.load_file(jump_point_file)
            self.add_jump_point(jump_point)
