# -*- coding:utf-8 -*-

import re

from mower import Mower

UP_RIGHT_CORNER_PATTERN = re.compile('([-+]?\\d+) ([-+]?\\d+)')

MOWER_STATUS_PATTERN = re.compile('([-+]?\\d+) ([-+]?\\d+) ([NESW])')


def read_integer(matcher, grp_number, line_number):
    """
    Parse an integer from a regex matcher able to parse strings formatted as "%d %d".
    :param matcher: regex matcher applied on the line string regarding the UP_RIGHT_CORNER_PATTERN pattern.
    :param grp_number: index of the integer to read (1 or 2)
    :param line_number: line number in the input file (used in exception to report error)
    :return: an integer if no exception occurs
    """
    try:
        coordinate = int(matcher.group(grp_number))
        if coordinate < 0:
            raise Exception('Error line {}: not a positive integer'.format(line_number))
        else:
            return coordinate
    except ValueError:
        raise Exception('Error line {}: not a valid integer'.format(line_number))


def read_grid_up_right_corner(line, line_number):
    """
    Parse the first line of the test file (which provides the grid lawn upper right corner coordinates).
    :param line: the first line of the test file as a string
    :param line_number: line number in the input file (used in exception to report error)
    :return: an tuple holding grid upper right corner coordinates if no exception occurs
    """
    matcher = re.match(UP_RIGHT_CORNER_PATTERN, line)
    if matcher and len(matcher.groups()) == 2:
        up_right_x = read_integer(matcher, 1, line_number)
        up_right_y = read_integer(matcher, 2, line_number)
        return up_right_x, up_right_y
    else:
        raise Exception('Error line {}, format expected: "%d %d"'.format(line_number))


def read_mower_status(line, line_number, up_right):
    """
    Parse a "mower status" line in the input test file (format: "%d %d [NESW]") and returns a mower initial status.
    :param line: a line holding a mower status in the test file as a string
    :param line_number: line number in the input file (used in exception to report error)
    :param up_right: (int, int) tuple ==> grid lawn upper right corner coordinates
    :return: a tuple as ((int, int), [NESW]) giving a mower status (position, orientation) if no exception occurs
    """
    matcher = re.match(MOWER_STATUS_PATTERN, line)
    if matcher and len(matcher.groups()) == 3:
        x = read_integer(matcher, 1, line_number)
        y = read_integer(matcher, 2, line_number)
        if x > up_right[0] or y > up_right[1]:
            raise Exception('Error line {}, coordinates should be less or equal than line 1 coordinates'
                            .format(line_number))
        else:
            if Mower.is_valid_orientation(matcher.group(3)):
                return (x, y), matcher.group(3)
            else:
                raise Exception('Error line {}, format expected:'.format(line_number) +
                                '"%d %d {one char in N,E,S,W}"')
    else:
        raise Exception('Error line {}, format expected:'.format(line_number) + '"%d %d {one char in N,E,S,W}"')


def read_program(line, line_number):
    """
    Parse a mower "program" line in the test file (should be a sequence of valid mower actions (a, G or D) as a string.
    :param line: line holding the mower program as a string
    :param line_number: line number in the input file (used in exception to report error)
    :return: the program as a string if no exception occurs
    """
    for action in line:
        if not Mower.is_valid_moving_code(action):
            raise Exception('Error line {}: programs should be a sequence matching "[AGD]*"'.format(line_number))
    return line


def read_line(f):
    """
    Read a line from a text file and remove end of line characters.
    :param f: text file handler
    :return: a cleaned line as string
    """
    line = f.readline()
    length = len(line)
    if length > 0 and line[length - 1] == '\n':
        line = line[:-1]
        length -= 1
        if length > 0 and line[length - 1] == '\r':
            line = line[:-1]
    return line


class MowersTestPlayer(object):
    """
    Class to read and apply a test file with a format defined in the exercise statements:
    First line ==> gives the grid lawn upper right corner coordinates. ex:   5 5
    Other lines ==> sequence of couple of lines giving (mower status + a mower program to apply)
    """

    def __init__(self, file_name):
        self._filename = file_name      # test file name
        self._mowers = []               # list of tuples (Mover, program) parsed from: the test file
        self._final_status = []         # list of final mower status when test has been applied

    @property
    def mowers(self):
        return self._mowers

    @property
    def all_status(self):
        return self._final_status

    def open(self):
        """
        Open and parse input test file (file_name).
        :return: A list of tuples (Mower, program) if no exception occurs
        """
        with open(self._filename, 'r') as f:
            line = read_line(f)
            Mower.set_up_right_corner(read_grid_up_right_corner(line, 1))
            line_number = 1
            status = None
            self._mowers = []
            line = read_line(f)
            while line != '':
                line_number += 1
                if line_number % 2 == 0:
                    status = read_mower_status(line, line_number, Mower.GRID_UP_RIGHT_CORNER)
                else:
                    program = read_program(line, line_number)
                    self._mowers.append((Mower(status[0], status[1]), program))
                line = read_line(f)
            f.close()

    def apply(self, with_history=False):
        """
        Apply the program for each mower identified in the test file.
        :return: the list of final status of the mowers as strings when with_history is False
        else return the list of all steps executed by mower and all initial status
        """
        self._final_status = []
        if not with_history:
            for tmover in self._mowers:
                tmover[0].move_multiple_steps(tmover[1])
                self._final_status.append(tmover[0].get_str_status())
            return self.all_status
        else:
            initial_status = []
            for tmover in self._mowers:
                initial_status.append(tmover[0].status)
                mower_history = []
                for step in tmover[1]:
                    tmover[0].move_one_step(step)
                    mower_history.append((tmover[0].status, step))
                self._final_status.append(mower_history)
            return self.all_status, initial_status



