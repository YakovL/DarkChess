from state import State, Player, Piece

def test_init():
    """
    With default positions, nobody wins;
    check also the corner pieces
    """
    game_state = State()
    assert game_state.get_winner() is None

    left_bottom_piece = game_state.get_board().cells[0][0]
    assert left_bottom_piece is not None
    assert left_bottom_piece.piece == Piece.rook
    assert left_bottom_piece.player == Player.white

    top_right_piece = game_state.get_board().cells[7][7]
    assert top_right_piece is not None
    assert top_right_piece.piece == Piece.rook
    assert top_right_piece.player == Player.black

