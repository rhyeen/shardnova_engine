""" Container for JumpPoint
"""


class JumpPoint(object):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.galaxy_name = None
        self.sector_name = None
        self.system_name = None
        self.celestial_body_name = None
        # @TODO: cost and ticks should be determined by looking at the current
        # location and determine if the jump is to another system, sector, or galaxy.
        # Each increasing in costs and ticks.  Cost may also, like all
        # other costs, be affected by the Faction who owns the gate.
        self.ticks_per_jump = 0
        self.cost_per_jump = 0

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return ('{0}->{1}->{2}->{3}'
                .format(self.galaxy_name, self.sector_name, self.system_name, self.celestial_body_name))

    def load_file(self, game_file):
        # @NOTE: intentionally not pushing it to coordinates.
        # Coordinates require the universe to be prebuilt to retrieve
        # the actual galaxy object (and other objects).
        # Since we're building out the universe, we only want to push out the
        # names.  During the actual jump, would we retrieve the actual objects.
        self.galaxy_name = game_file['galaxy']
        self.sector_name = game_file['sector']
        self.system_name = game_file['system']
        self.celestial_body_name = game_file['celestialBody']
        self.ticks_per_jump = game_file['ticksPerJump']
        self.cost_per_jump = game_file['costPerJump']
