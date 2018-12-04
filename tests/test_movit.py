from movit.movit import Board, Piece

BOARD_1 = '[["X"]]'
BOARD_2 = '[["X","X","X"],["X","a","X"],["X","X","X"]]'
BOARD_3 = '[["X","X","X","X"],["X","b","a","X"],["X","X","X","X"]]'


def test_board_init():
    b = Board(BOARD_1)
    assert b
    assert b.state == (("X",),)

    b = Board(BOARD_2)
    assert b
    assert b.state == (("X", "X", "X",), ("X", "a", "X",), ("X", "X", "X",),)


def test_get_piece():
    b = Board(BOARD_2)
    p = b.get_piece('a')
    assert p
    assert p.name == 'a'
    assert p.pos_tup == ((1, 1),)


def test_get_piece_names():
    b = Board(BOARD_3)
    assert b.get_piece_names() == ['a', 'b']


def test_get_pieces():
    b = Board(BOARD_3)
    pieces = b.get_pieces()
    assert len(pieces) == 2
    assert pieces[0].name == 'a'