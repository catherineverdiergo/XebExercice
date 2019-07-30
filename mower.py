# -*- coding:utf-8 -*-

"""
  Xebia exercice: Robotic mower moving on a grid lawn modelization.
"""


class Mower(object):

    GRID_UP_RIGHT_CORNER = None  # should hold upper right corner of the grid ( via set_up_right_corner method)

    # list of valid orientations (!!! keep this order to insure proper swing operations !!!)
    ORIENTATIONS = ['N', 'E', 'S', 'W']

    # list of (coordinate, operation) to perform when moving the mower forward regarding ORIENTATIONS list
    # for instance 'W': (0, -1) means that if the mower's position is 'N' and if the mower should move forward,
    # we should operate on the first coordinate (index 0 or x) and add it -1
    MOVE_FORWARD_OPERATIONS = {'N': (1, 1), 'E': (0, 1), 'S': (1, -1), 'W': (0, -1)}

    MOVING_CODES = ['A', 'D', 'G']  # list of valid moving codes

    # operations to perform on orientation when action is 'D' or 'G' regarding the ORIENTATIONS list
    # if the current mower's orientation is 'S' (index 2 in the ORIENTATIONS list) and if it should move on the left
    # (moving code 'G'), its next orientation index in the ORIENTATIONS list will be 2-1=1 (hence 'E')
    # To swing properly, the orientation shift is performed modulo the length of the ORIENTATIONS list (see the swing
    # method)
    SWING_OPERATIONS = {'D': 1, 'G': -1}

    @classmethod
    def is_valid_position(cls, position):
        """
        Check if a position is valid. As position, we expect a tuple of 2 positive integers.
        :param position: position parameter to validate
        :return: boolean (True if position parameter is valid, otherwise False)
        """
        return isinstance(position, tuple) and len(position) == 2 and isinstance(position[0], int) \
            and isinstance(position[1], int )and position[0] >= 0 and position[1] >= 0

    @classmethod
    def is_valid_orientation(cls, orientation):
        """
        Check if an orientation is valid. Should be in the ORIENTATIONS list.
        :param orientation: orientation parameter to check
        :return: boolean (True if orientation parameter is valid, otherwise False)
        """
        return orientation in Mower.ORIENTATIONS

    @classmethod
    def is_valid_moving_code(cls, moving_code):
        """
        Check if a moving_code is valid. Should be in the MOVING_CODES list.
        :param moving_code: moving_code parameter to check
        :return: boolean (True if moving_code parameter is valid, otherwise False)
        """
        return moving_code in Mower.MOVING_CODES

    @classmethod
    def set_up_right_corner(cls, up_right_corner):
        """
        Class method to initialize (as a valid position parameter) the upper right corner of the lawn grid.
        :param up_right_corner: upper right corner of the lawn grid
        :return: None
        """
        if Mower.is_valid_position(up_right_corner):
            Mower.GRID_UP_RIGHT_CORNER = up_right_corner
        else:
            raise Exception('up_right_corner parameter should be a tuple2 with positive coordinates')

    def __init__(self, position, orientation):
        """
        Mower constructor. set initial position and orientation for the mower.
        :param position: initial position
        :param orientation: initial orientation
        """
        if Mower.is_valid_position(position):
            self._position = position
        else:
            raise Exception('position parameter should be a tuple2 with positive coordinates')
        if Mower.is_valid_orientation(orientation):
            self._orientation = orientation
        else:
            raise Exception('orientation parameter should be among {}'.format(Mower.ORIENTATIONS))

    @property
    def position(self):
        """
        Mower position accessor.
        :return: the mower position
        """
        return self._position

    @property
    def orientation(self):
        """
        Mower orientation accessor.
        :return: the mower orientation
        """
        return self._orientation

    @property
    def status(self):
        """
        Mower status accessor.
        :return: a tuple with mower position and orientation
        """
        return self.position, self.orientation

    def get_str_status(self):
        return '{} {} {}'.format(self.position[0], self.position[1], self.orientation)

    def move_forward(self):
        """
        Move the mower forward (moving code 'A') from its current position and orientation.
        Computes the new position of the mower.
        :return: None
        """
        if Mower.is_valid_position(Mower.GRID_UP_RIGHT_CORNER):
            coordinates = list(self._position)
            target_coordinate = Mower.MOVE_FORWARD_OPERATIONS[self.orientation][0]
            operand_2_add = Mower.MOVE_FORWARD_OPERATIONS[self.orientation][1]
            next_coordinate = self.position[target_coordinate] + operand_2_add
            if 0 <= next_coordinate <= Mower.GRID_UP_RIGHT_CORNER[target_coordinate]:
                coordinates[target_coordinate] = next_coordinate
                self._position = tuple(coordinates)
        else:
            raise Exception('Mower.GRID_UP_RIGHT_CORNER should be defined (use Mower.set_up_right_corner method)')

    def swing(self, moving_code):
        """
        Swings the mower (moving code 'G' or 'D').
        Computes the next orientation of the mower.
        :param moving_code: 'G' or 'D'
        :return: None
        """
        current_orientation_index = Mower.ORIENTATIONS.index(self.orientation)
        next_orientation_index = (current_orientation_index + Mower.SWING_OPERATIONS[moving_code]) \
                                 % len(Mower.ORIENTATIONS)
        self._orientation = Mower.ORIENTATIONS[next_orientation_index]

    def move_one_step(self, moving_code):
        """
        Apply a moving code ('A' or 'G' or 'D') to the mower.
        Computes the next status (position + orientation) of the mower).
        :param moving_code: a valid moving code
        :return:
        """
        if Mower.is_valid_moving_code(moving_code):
            if moving_code == 'A':
                self.move_forward()
            else:
                self.swing(moving_code)

    def move_multiple_steps(self, moving_program):
        """
        Apply a set of moving code to the mower.
        Computes the next status (position + orientation) of the mower).
        :param moving_program: a string as a list of moving codes
        :return: None
        """
        for action in moving_program:
            self.move_one_step(action)
