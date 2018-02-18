""" Container for JumpPoint
"""


class JumpPoint(object):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.galaxy_name = None
        self.sector_name = None
        self.system_name = None
        self.celestial_body_name = None
        self.ticks_per_jump = 0
        self.cost_per_jump = 0

    def __str__(self):
        return 'Jump to: {0}'.format(self.__coordinates)

    def load_file(self, game_file):
        # @NOTE: intentionally not pushing it to coordinates.
        # Coordinates require the universe to be prebuilt to retrieve
        # the actual galaxy object (and other objects).
        # Since we're building out the universe, we only want to push out the
        # names.  During the actual jump, would we retrieve the actual objects.
        self.galaxy_name = game_file['galaxy']
        self.sector_name = game_file['sector']
        self.system_name = game_file['system']
        self.celestial_body_name = game_file['celestial_body']
        self.ticks_per_jump = game_file['ticksPerJump']
        self.cost_per_jump = game_file['costPerJump']
