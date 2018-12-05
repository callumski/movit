#!/usr/bin/env python3
import argparse
import json
from string import ascii_lowercase


class Piece(object):
    def __init__(self, name, pos_tup):
        self.name = name
        self.pos_tup = pos_tup

    def __str__(self):
        return "{}: {}".format(self.name, str(self.pos_tup))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Move(object):
    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_new_position(self):
        return tuple(
            (sqr[0] + self.x, sqr[1] + self.y) for sqr in self.piece.pos_tup)


class Board(object):
    def __init__(self, json_string=None, state=None):
        if json_string:
            self._state = tuple(tuple(y) for y in json.loads(json_string))
        elif state:
            self._state = state

    def __eq__(self, other):
        return self._state == other._state

    def get_piece(self, name):
        return Piece(name,
                     tuple([(x, y) for y in range(len(self._state)) for x in
                            range(len(self._state[y])) if
                            self._state[y][x] == name]))

    def get_piece_names(self):
        return sorted(
            {j for i in self._state for j in i if j in ascii_lowercase})

    def get_pieces(self):
        return [self.get_piece(name) for name in self.get_piece_names()]

    def is_move_available(self, move):
        new_pos = move.get_new_position()
        for i in new_pos:
            cell = self._state[i[1]][i[0]]
            if not self._cell_is_free(cell, move.piece.name) \
                    and not self._piece_can_exit(cell, move.piece.name):
                return False
        return True

    def _cell_is_free(self, cell, name):
        return cell == " " or cell == name

    def _piece_can_exit(self, cell, name):
        return cell == "Z" and name == 'b'

    def get_available_moves(self):
        opts = ((1, 0), (0, 1), (-1, 0), (0, -1))
        moves = []
        for pce in self.get_pieces():
            for opt in opts:
                move = Move(pce, opt[0], opt[1])
                if self.is_move_available(move):
                    moves.append(move)
        return moves

    def apply_move(self, move):
        pce = move.piece.name
        new_pos = move.get_new_position()
        new_state = []
        for y in range(len(self._state)):
            new_y = []
            for x in range(len(self._state[y])):
                cell = self._state[y][x]
                if (x, y) in new_pos and cell != "Z":
                    new_y.append(pce)
                elif cell == pce:
                    new_y.append(" ")
                else:
                    new_y.append(self._state[y][x])
            new_state.append(tuple(new_y))
        return Board(state=tuple(new_state))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="movit.py: Looks for solution "
                                                 "to a board problem.")
    parser.add_argument("file", help="JSON file of board setup")
    args = parser.parse_args()

    with open(args.file, mode="r") as file:
        board = Board(file.read())

    for piece in board.get_pieces():
        print(piece)
