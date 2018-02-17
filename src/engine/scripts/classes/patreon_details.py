""" Container for PatreonDetails
"""


class PatreonDetails(object):

    def __init__(self, patreon_id=None):
        self.__patreon_id = patreon_id

    def get_patreon_id(self):
        return self.__patreon_id

    def set_patreon_id(self, patreon_id):
        self.__patreon_id = patreon_id
