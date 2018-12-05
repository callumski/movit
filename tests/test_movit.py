from movit.movit import Board, Move, Piece

BOARD_1 = '[["X"]]'
BOARD_2 = '[["X","X","X"],["X","a","X"],["X","X","X"]]'
BOARD_3 = '[["X","X","X","X"],["X","b","a","X"],["X","X","X","X"]]'
BOARD_4 = '[["X","X","X","X"],["X","a"," ","X"],["X","X","X","X"]]'
BOARD_5 = '[["X","X","X","X","X"],["X","a"," ","X"],["X"," "," ","X"],["X","X","X","X","X"]]'


def test_board_init():
    b = Board(BOARD_1)
    assert b
    assert b.state == (("X",),)

    b = Board(BOARD_2)
    assert b
    assert b.state == (
        ("X", "X", "X",), ("X", "a", "X",), ("X", "X", "X",),)


def test_board_get_piece():
    b = Board(BOARD_2)
    p = b.get_piece('a')
    assert p
    assert p.name == 'a'
    assert p.pos_tup == ((1, 1),)


def test_board_get_piece_names():
    b = Board(BOARD_3)
    assert b.get_piece_names() == ['a', 'b']


def test_board_get_pieces():
    b = Board(BOARD_3)
    pieces = b.get_pieces()
    assert len(pieces) == 2
    assert pieces[0].name == 'a'


def test_board_is_move_available_success():
    b = Board(BOARD_4)
    p = b.get_piece('a')
    m = Move(p, 1, 0)
    assert b.is_move_available(m)


def test_board_is_move_available_failure():
    b = Board(BOARD_4)
    p = b.get_piece('a')
    m = Move(p, 0, 1)
    assert not b.is_move_available(m)
    m = Move(p, 1, 1)
    assert not b.is_move_available(m)


def test_board_get_available_moves():
    b = Board(BOARD_5)
    p = b.get_piece('a')
    moves = b.get_available_moves()
    assert len(moves) == 2
    print(moves)
    assert Move(p, 1, 0) in moves
    assert Move(p, 0, 1) in moves


def test_move_get_next_position():
    p = Piece('a', ((1, 1), (1, 2)))
    m = Move(p, 1, 2)
    assert m.get_new_position() == ((2, 3), (2, 4))
    p = Piece('a', ((0, 0), (1, 0)))
    m = Move(p, 0, 2)
    assert m.get_new_position() == ((0, 2), (1, 2))
