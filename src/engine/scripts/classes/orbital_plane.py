""" Container for OrbitalPlane
"""


class OrbitalPlane(object):
    def __init__(self):
        self.__celestial_body_objects = []

    def get_distances(self, celestial_body):
        distances = {}
        distance_from_center = self.get_distance_from_center(celestial_body)
        for celestial_body_object in self.__celestial_body_objects:
            distance_from_given = abs(distance_from_center - celestial_body_object['distance_from_center'])
            distances[celestial_body_object['celestial_body'].get_name()] = distance_from_given
        return distances

    def get_celestial_bodies(self):
        celestial_bodies = []
        for celestial_body_object in self.__celestial_body_objects:
            celestial_bodies.append(celestial_body_object['celestial_body'])
        return celestial_bodies

    def get_celestial_body(self, name):
        index = self.__get_celestial_body_index(name)
        return self.__celestial_body_objects[index]['celestial_body']

    def get_distance_from_center(self, celestial_body):
        index = self.__get_celestial_body_index(celestial_body.get_name())
        return self.__celestial_body_objects[index]['distance_from_center']

    def __get_celestial_body_index(self, name):
        for index, celestial_body_object in enumerate(self.__celestial_body_objects):
            celestial_body = celestial_body_object['celestial_body']
            if celestial_body.get_name() == name:
                return index
        raise ValueError('{0} does not exist in the orbital plane'.format(name))

    def push(self, celestial_body, distance_from_last=1):
        if len(self.__celestial_body_objects) == 0:
            distance_from_center = 0
        else:
            assert (distance_from_last > 1)
            distance_from_center = self.__celestial_body_objects[-1]['distance_from_center'] + distance_from_last
        self.__celestial_body_objects.append({
            'celestial_body': celestial_body,
            'distance_from_center': distance_from_center
        })

    def insert(self, celestial_body, distance_from_center=0):
        assert(distance_from_center > 0)
        if len(self.__celestial_body_objects) == 0:
            distance_from_center = 0
        insert_index = 0
        while insert_index < len(self.__celestial_body_objects):
            insert_index += 1
            celestial_body_object = self.__celestial_body_objects[insert_index]
            if distance_from_center < celestial_body_object['distance_from_center']:
                break
            if distance_from_center == celestial_body_object['distance_from_center']:
                raise ValueError('Cannot insert celestial body with same distance from center of the system as {0}'
                                 .format(celestial_body_object['celestial_body']))
        celestial_body_object = {
            'celestial_body': celestial_body,
            'distance_from_center': distance_from_center
        }
        self.__celestial_body_objects.insert(insert_index, celestial_body_object)

    def get_distance_between_celestial_bodies(self, body1, body2):
        distances = self.get_distances(body1)
        if body2.get_name() not in distances:
            raise ValueError('second celestial body, {0} not within orbital plane'
                             .format(body2))
        return distances[body2.get_name()]

    def get_celestial_body_at_distance(self, distance_from_center):
        assert(distance_from_center >= 0)
        for celestial_body_object in self.__celestial_body_objects:
            if distance_from_center == celestial_body_object['distance_from_center']:
                return celestial_body_object['celestial_body']
        return None
