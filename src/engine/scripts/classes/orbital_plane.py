""" Container for OrbitalPlane
"""


class Node(object):
    def __init__(self, celestial_body):
        self.celestial_body = celestial_body
        self.next_node = None
        self.next_edge = None
        self.prev_node = None
        self.prev_edge = None


class Graph(object):
    def __init__(self):
        self.first_node = None
        self.last_node = None

    def get_distances(self, celestial_body):
        node = self.__get_node(celestial_body)
        prev_distance = 0
        next_distance = 0
        distances = {}
        current_node = node
        while True:
            distances[current_node.celestial_body.get_id()] = next_distance
            current_node = self.__next(current_node)
            if current_node is None:
                break
            next_distance += current_node.prev_edge
        while True:
            distances[current_node.celestial_body.get_id()] = prev_distance
            current_node = self.__prev(current_node)
            if current_node is None:
                break
            prev_distance += current_node.next_edge
        return distances

    def __get_node(self, celestial_body):
        if self.first_node is None:
            return None
        current_node = self.first_node
        while current_node is not None:
            if current_node.celestial_body.get_id() == celestial_body.get_id():
                return current_node
            current_node = self.__next(current_node)
        raise ValueError('{0} does not exist in the orbital plane'.format(celestial_body))

    def __next(self, current_node):
        return current_node.next_node

    def __prev(self, current_node):
        return current_node.prev_node

    def get_celestial_bodies(self):
        celestial_bodies = []
        current_node = self.first_node
        while current_node is not None:
            celestial_bodies.append(current_node.celestial_bodies)
            current_node = self.__next(current_node)
        return celestial_bodies

    def push(self, celestial_body, distance_from_last=0):
        if self.first_node is None:
            self.__initialize(celestial_body)
            return
        new_node = Node(celestial_body)
        new_node.prev_node = self.last_node
        new_node.prev_edge = distance_from_last
        self.last_node.next_node = new_node
        self.last_node.next_edge = distance_from_last
        self.last_node = new_node

    def insert(self,
               celestial_body,
               previous_celestial_body,
               distance_to_previous_celestial_body):
        prev_node = self.__get_node(previous_celestial_body)
        if not prev_node:
            raise ValueError('Could not find the previous_celestial_body')
        next_node = self.__next(prev_node)
        if not next_node:
            self.push(celestial_body, distance_to_previous_celestial_body)
            return
        prev_edge = prev_node.next_edge
        if (distance_to_previous_celestial_body > prev_edge):
            raise ValueError('distance_to_previous_celestial_body ({0}) cannot be greater than '
                             'the distance between previous_celestial_body\'s '
                             'and the next celestial body ({1})'
                             .format(distance_to_previous_celestial_body, prev_edge))
        new_node = Node(celestial_body)
        new_node.prev_node = prev_node
        new_node.prev_edge = distance_to_previous_celestial_body
        new_node.next_node = next_node
        new_node.next_edge = prev_edge - distance_to_previous_celestial_body
        prev_node.next_node = new_node
        prev_node.next_edge = new_node.prev_edge
        next_node.prev_node = new_node
        next_node.prev_edge = new_node.next_edge

    def __initialize(self, celestial_body):
        self.first_node = Node(celestial_body)
        self.last_node = self.first_node

    def get_distance_between_celestial_bodies(self, body1, body2):
        distances = self.get_distances(body1)
        if body2.get_id() not in distances:
            raise ValueError('second celestial body, {0} not within orbital plane'
                             .format(body2))
        return distances[body2.get_id()]


class OrbitalPlane(object):

    def __init__(self):
        self.__plane = Graph()
