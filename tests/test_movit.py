from movit.movit import Board, Move, Piece
from tests.conftest import (BOARD_1, BOARD_2, BOARD_3, BOARD_4, BOARD_5,
                            BOARD_6, BOARD_6A, BOARD_7, BOARD_8)


def test_board_init():
    b = Board(json_string=BOARD_1)
    assert b
    assert b._state == (("X",),)

    b = Board(json_string=BOARD_2)
    assert b
    assert b._state == (
        ("X", "X", "X",), ("X", "a", "X",), ("X", "X", "X",),)


def test_board_get_piece_success():
    b = Board(json_string=BOARD_2)
    p = b.get_piece('a')
    assert p
    assert p.name == 'a'
    assert p.pos_tup == ((1, 1),)


def test_board_get_piece_failure():
    b = Board(json_string=BOARD_2)
    p = b.get_piece('w')
    assert not p


def test_board_get_piece_names():
    b = Board(json_string=BOARD_3)
    assert b._get_piece_names() == ['a', 'b']


def test_board_get_pieces():
    b = Board(json_string=BOARD_3)
    pieces = b.get_pieces()
    assert len(pieces) == 2
    assert 'a' in pieces.keys()
    assert 'b' in pieces.keys()


def test_board_is_move_available_success():
    b = Board(json_string=BOARD_4)
    p = b.get_piece('b')
    m = Move(p, 1, 0)
    assert b.is_move_available(m)

    b = Board(json_string=BOARD_5)
    p = b.get_piece('b')
    m = Move(p, 1, 0)
    assert b.is_move_available(m)


def test_board_is_move_available_failure():
    b = Board(json_string=BOARD_4)
    p = b.get_piece('b')
    m = Move(p, 0, 1)
    assert not b.is_move_available(m)
    m = Move(p, -1, 0)
    assert not b.is_move_available(m)
    b = Board(json_string=BOARD_7)
    p = b.get_piece('b')
    m = Move(p, 0, 1)
    assert not b.is_move_available(m)


def test_board_is_exit_move_available_success():
    b = Board(json_string=BOARD_6)
    p = b.get_piece('b')
    m = Move(p, 0, 1)
    assert b.is_move_available(m)


def test_board_is_exit_move_available_failure():
    b = Board(json_string=BOARD_7)
    p = b.get_piece('b')
    m = Move(p, 0, 1)
    assert not b.is_move_available(m)


def test_board_get_available_moves():
    bd = Board(json_string=BOARD_5)
    b = bd.get_piece('b')
    c = bd.get_piece('c')
    moves = bd.get_available_moves()
    assert len(moves) == 4
    assert Move(b, 1, 0) in moves
    assert Move(b, 0, 1) in moves
    assert Move(c, -1, 0, double=True) in moves
    assert Move(c, 0, -1) in moves


def test_board_apply_move():
    b = Board(json_string=BOARD_7)
    a = b.get_piece('a')
    m = Move(a, 0, 1)
    b2 = b.apply_move(m)
    assert b2 == Board(json_string=BOARD_8)


def test_board_apply_exit_move():
    bd = Board(json_string=BOARD_6)
    b = bd.get_piece('b')
    m = Move(b, 0, 1)
    bd2 = bd.apply_move(m)
    assert bd2 == Board(json_string=BOARD_6A)
    assert bd2.previous == bd


def test_move_get_next_position():
    p = Piece('a', ((1, 1), (1, 2)))
    m = Move(p, 1, 2)
    assert m.get_new_position() == [(2, 3), (2, 4)]
    p = Piece('a', ((0, 0), (1, 0)))
    m = Move(p, 0, 2)
    assert m.get_new_position() == [(0, 2), (1, 2)]
