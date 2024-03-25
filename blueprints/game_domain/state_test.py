from state import State, Player, Piece

def test_init():
    """
    With default positions, nobody wins;
    check also the corner pieces and another two positions
    """
    game_state = State()
    assert game_state.get_winner() is None

    bottom_left_piece = game_state.get_board().cells[0][0]
    assert bottom_left_piece is not None
    assert bottom_left_piece.piece == Piece.rook
    assert bottom_left_piece.player == Player.white

    top_right_piece = game_state.get_board().cells[7][7]
    assert top_right_piece is not None
    assert top_right_piece.piece == Piece.rook
    assert top_right_piece.player == Player.black

    middle_left_piece = game_state.get_board().cells[0][3]
    assert middle_left_piece is None

    bottom_center_piece = game_state.get_board().cells[3][0]
    assert bottom_center_piece is not None
    assert bottom_center_piece.piece == Piece.king
    assert bottom_center_piece.player == Player.white

