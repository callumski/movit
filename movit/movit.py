#!/usr/bin/env python3
import json
from string import ascii_lowercase


class Piece(object):
    def __init__(self, name, pos_tup):
        self.name = name
        self.pos_tup = pos_tup

    def __str__(self):
        return "{}: {}".format(self.name, str(self.pos_tup))


class Board(object):
    def __init__(self, json_string):
        self.state = tuple(tuple(y) for y in json.loads(json_string))

    def get_piece(self, name):
        return Piece(name,
                     tuple([(x, y) for y in range(len(self.state)) for x in
                            range(len(self.state[y])) if
                            self.state[y][x] == name]))

    def get_piece_names(self):
        return sorted(
            {j for i in self.state for j in i if j in ascii_lowercase})

    def get_pieces(self):
        return [self.get_piece(name) for name in self.get_piece_names()]


if __name__ == '__main__':
    with open('default_board.json', mode="r") as file:
        board = Board(file.read())

    for piece in board.get_pieces():
        print(piece)
