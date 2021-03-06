#!/usr/bin/env python3
import argparse
import json
from collections import deque
from pathlib import Path
from string import ascii_lowercase

THIS_DIR = str(Path(__file__).resolve().parent)

"""movit: A small project to find the solution to the puzzle outlined below.
    The solution involves moving pieces around the board and eventually moving
    b through Z in as few moves as possible.

    Once solved, it shows the moves from initial state to the final state in
    the optimal solution.

"""


class Piece(object):
    """
    Convenience class to hold the coordinates of a piece on the Board.
    """

    def __init__(self, name, pos_tup):
        self.name = name
        self.pos_tup = pos_tup

    def __str__(self):
        return "{}: {}".format(self.name, str(self.pos_tup))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Move(object):
    """
    Convenience class to represent a move of a piece on the Board.
    """

    def __init__(self, piece, x, y, double=False):
        self.piece = piece
        self.double = double
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{}: x:{} y:{} double:{}".format(self.piece, self.x, self.y,
                                                self.double)

    def get_new_position(self):
        """
        Get the new position of the Piece.

        Add the move (doubling if necessary) to the Pieces positions.
        :return: a list of cartesian tuples.
        spider)
        """
        mult = 1
        if self.double:
            mult = 2
        return [(sqr[0] + (mult * self.x), sqr[1] + (mult * self.y)) for sqr in
                self.piece.pos_tup]


class Board(object):
    """
    Class to hold Board we are playing on, with several helper methods.
    """

    def __init__(self, json_string=None, state=None, previous=None, move=None,
                 pieces=None):
        if json_string:
            self._state = tuple(tuple(y) for y in json.loads(json_string))
        elif state:
            self._state = state
        self._pieces = pieces
        self.previous = previous
        self.move = move

    def __eq__(self, other):
        return self._state == other._state

    def get_piece(self, name):
        return self.get_pieces().get(name)

    def _get_piece(self, name):
        """For a given piece name, find all it's cells on the Board, build a
        Piece onject and return it."""
        return Piece(name, tuple([(x, y) for y in range(len(self._state))
                                  for x in range(len(self._state[y])) if
                                  self._state[y][x] == name]))

    def _get_piece_names(self):
        return sorted(
            {j for i in self._state for j in i if j in ascii_lowercase})

    def get_pieces(self):
        """ Lazily fetch the dict of Pieces."""
        if not self._pieces:
            self._pieces = {name: self._get_piece(name) for name in
                            self._get_piece_names()}
        return self._pieces

    def is_move_available(self, move):
        """
        Is the provided Move possible on this Baord.

        Get the position where the Piece would end up. Check that it will be
        either on free space or a space it currently occupies. If the piece is
        piece 'b' then that can sit on the 'Z' cells.
        :return: a Move object
        """
        new_pos = move.get_new_position()
        for i in new_pos:
            try:
                cell = self._state[i[1]][i[0]]
            except IndexError:
                return False
            if not self._cell_is_free(cell, move.piece.name) \
                    and not self._piece_can_exit(cell, move.piece.name):
                return False
        return True

    def _cell_is_free(self, cell, name):
        return cell == " " or cell == name

    def _piece_can_exit(self, cell, name):
        return cell == "Z" and name == 'b'

    def get_available_moves(self):
        """
        Get a list of the Moves possible on this Baord.

        For each piece, see if it can move in any direction. However, do not
        try the move that brought us here.
        :return: a list of Move objects
        """
        prev_move = None
        if self.move:
            prev_move = (-self.move.x, -self.move.y)
        opts = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if prev_move:
            opts.remove(prev_move)
        moves = []
        for pce in self.get_pieces().values():
            for opt in opts:
                move = Move(pce, opt[0], opt[1])
                if self.is_move_available(move):
                    move.double = True
                    if not self.is_move_available(move):
                        move.double = False
                    moves.append(move)
        return moves

    def apply_move(self, move):
        """
        Apply a Moves possible to the  Baord.

        Redraw a new Board that is the reuslt of applying to Move. Also make
        sure the Move and this Board are stored on the new one.
        :param: a Move object
        :return: a new Board Object
        """
        pce = move.piece.name
        new_pos = move.get_new_position()
        new_state = []
        for y in range(len(self._state)):
            new_y = []
            for x in range(len(self._state[y])):
                cell = self._state[y][x]
                # We might go over the edge, if so it is legal
                if cell == "Z" or cell == "X":
                    new_y.append(cell)
                    if (x, y) in new_pos:
                        # but we need to remove the cells from the piece
                        # to avoid IndexErrors
                        new_pos.remove((x, y))
                elif (x, y) in new_pos:
                    new_y.append(pce)
                elif cell == pce:
                    new_y.append(" ")
                else:
                    new_y.append(self._state[y][x])
            new_state.append(tuple(new_y))
        # Update this list of pieces and pass it on to avoid recalculating.
        new_pieces = self.get_pieces().copy()
        new_pieces.pop(pce)
        if new_pos:
            new_pieces[pce] = Piece(pce, new_pos)
        return Board(state=tuple(new_state), previous=self, move=move,
                     pieces=new_pieces)


def solve_board(start_board, all_solutions, find_n=-1, json_output=False):
    """
    Find the solution(s) to a  Baord.

    Iterate through the available Moves for each Baord in a Breadth First
    Search. Depending on the settings stop at the first solution.
    :param: start_board: a Board object
    :param: all_solutions: bool: do we search for all solutions
    :param: find_n: an int of how many solutions to search for
    :param: json_output: bool: should we output in JSON
    :return: a new Board Object
    """
    queue = deque([start_board])
    visited_boards = set()
    results = 0
    while queue:
        # pop left and append from the other end
        board = queue.popleft()
        # Have we got 'b' off the board?
        if not board.get_piece('b'):
            results += 1
            print_solution(results, board, len(visited_boards), json_output)
            if results == find_n and not all_solutions:
                break
        #
        for next_board in [board.apply_move(move) for move in
                           board.get_available_moves()]:
            if next_board._state not in visited_boards:
                visited_boards.add(next_board._state)
                queue.append(next_board)
    return results


def print_solution(num, board, visited, json_output):
    """Build the list of board states in the solution and pass them to the
    right function"""
    boards = []
    while board.previous:
        boards.append(board._state)
        board = board.previous

    boards.reverse()

    if json_output:
        print_json(num, boards, visited)
    else:
        print_for_human(num, boards, visited)


def print_json(num, boards, visited):
    """ Outout a solution in JSON Lines format."""
    print(
        "{{\"solution_nunber\": {}, \"board_states_visited\": {},"
        " \"board_states\": [{}]}}".format(
            num, visited, json.dumps(boards)))


def print_for_human(num, boards, visited):
    """ Outout a solution in human readable format."""
    print("Here is solution {} - found from visiting {} unique board "
          "positions:".format(num, visited))

    for chunk in chunks(boards, 6):
        print_chunk(chunk)
    print(
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")  # noqa


def print_chunk(boards):
    print(
        "---------------------------------------------------------------------------------------------------------")  # noqa
    for i in range(len(boards[0])):
        line = []
        for bd in boards:
            line += bd[i]
            line += ["    "]
        print("   " + " ".join(line))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="movit.py: Finds solutions "
                    "to a board problem.")
    parser.add_argument("file", help="full path to JSON file of board setup",
                        nargs='?')
    parser.add_argument("--find-all", dest="find_all", action="store_true",
                        help="find all possible solutions")
    parser.add_argument("--find-n", type=int,
                        help="find N solutions: default is 1", default=1)
    parser.add_argument("--json-output", dest="json_output",
                        action="store_true",
                        help="output solutions as JSON Lines see:"
                             " http://jsonlines.org/")

    args = parser.parse_args()
    if not args.file:
        parser.print_help()
        exit(1)

    with open(args.file, mode="r") as file:
        board = Board(file.read())

    results = solve_board(board, args.find_all, args.find_n,
                          json_output=args.json_output)

    if not args.json_output:
        if results:
            print("Found {} solutions.".format(results))
        else:
            print("No solution was found :(")
