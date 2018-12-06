#!/usr/bin/env python3
import argparse
import json
from collections import deque, namedtuple
from pathlib import Path
from string import ascii_lowercase

import numpy as np

THIS_DIR = str(Path(__file__).resolve().parent)

Piece = namedtuple('Piece', ['name', 'cells'])


class Move(object):
    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{}: x:{} y:{}".format(self.piece, self.x, self.y)

    def get_new_position(self):
        new_pos = np.add([self.y, self.x], self.piece.cells)
        return new_pos


class Board(object):
    def __init__(self, json_string=None, state=None, previous=None, move=None,
                 pieces=None):
        if json_string:
            self._state = np.array(json.loads(json_string))
        elif state is not None:
            self._state = state
        self._pieces = pieces
        self.previous = previous
        self.move = move
        self.hash_state = tuple(self._state.flatten())

    def __eq__(self, other):
        return (self._state == other._state).all()

    def __repr__(self):
        return repr(self._state)

    def get_pieces(self):
        if not self._pieces:
            self._init_pieces()
        return self._pieces

    def _init_pieces(self):
        names = [name for name in np.unique(self._state) if
                 name in ascii_lowercase]
        self._pieces = {name: Piece(name, np.argwhere(self._state == name)) for
                        name in
                        names}

    def is_move_possible(self, move):
        new_pos = move.get_new_position()
        for i in new_pos:
            cell = self._state.item((i[0], i[1]))
            if not self._cell_is_free(cell, move.piece.name) \
                    and not self._piece_can_exit(cell, move.piece.name):
                return False
        return True

    def _cell_is_free(self, cell, name):
        return cell == " " or cell == name

    def _piece_can_exit(self, cell, name):
        return cell == "Z" and name == 'b'

    def get_available_moves(self):
        prev_move = None
        if self.move:
            prev_move = (-self.move.x, -self.move.y)
        opts = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if prev_move:
            opts.remove(prev_move)
        moves = []
        for piece in [self.get_pieces()[name] for name in
                      self._get_candidate_pieces()]:
            for opt in opts:
                move = Move(piece, opt[0], opt[1])
                if self.is_move_possible(move):
                    moves.append(move)
        return moves

    def _get_candidate_pieces(self):
        candidates = [self._state.item(cell[0], cell[1]) for empty in
                      self._get_empty_cells() for cell in
                      self._get_neighbours(empty[0], empty[1])]
        candidates = {candidate for candidate in candidates if
                      candidate in ascii_lowercase}
        candidates.add('b')
        return candidates

    def _get_empty_cells(self):
        return np.argwhere(self._state == ' ')

    def _get_neighbours(self, x, y):
        nbhs = np.array([[x + 1, y], [x, y + 1], [x - 1, y], [x, y - 1]])
        return nbhs

    def _clear_cell(self, state, cell):
        state[cell[0]][cell[1]] = ' '

    def _update_cell(self, state, cell, name):
        if state[cell[0]][cell[1]] not in ["X", "Z"]:
            state[cell[0]][cell[1]] = name

    def apply_move(self, move):
        new_pos = move.get_new_position()
        new_state = self._state.copy()
        for cell in move.piece.cells:
            self._clear_cell(new_state, cell)
        for cell in new_pos:
            self._update_cell(new_state, cell, move.piece.name)
        return Board(state=new_state, previous=self, move=move)


def solve_board(start_board):
    queue = deque([start_board])
    visited_boards = set()
    result = None
    while queue:
        board = queue.popleft()
        if 'b' not in board.get_pieces().keys():
            result = board
            break
        for next_board in [board.apply_move(move) for move in
                           board.get_available_moves()]:
            if next_board.hash_state not in visited_boards:
                visited_boards.add(next_board.hash_state)
                queue.append(next_board)
    return (result, len(visited_boards))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="movit.py: Finds solutions "
                                                 "to a board problem.")
    parser.add_argument("file", help="JSON file of board setup", nargs='?')
    args = parser.parse_args()

    if not args.file:
        args.file = THIS_DIR + "/simple_board.json"

    with open(args.file, mode="r") as file:
        board = Board(file.read())

    final_board, visited = solve_board(board)
    print("movit visited: {} unique board positions.".format(visited))
    if final_board:
        print("Here is the best solution found:")
        solution = []
        while final_board.previous:
            solution.append(final_board)
            final_board = final_board.previous

        solution.reverse()

        for state in solution:
            for y in state._state:
                print(y)
            print("--------------------------------")
    else:
        print("No solution was found :(")
