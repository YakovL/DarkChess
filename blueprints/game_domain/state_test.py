from state import GameState, Board, Player, Piece

def test_init():
    """
    With default positions, nobody wins;
    check also the corner pieces and another two positions
    """
    game_state = GameState()

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

def test_is_move_valid():
    """
    Check various valid and invalid moves
    """
    game_state = GameState()

    # not their piece = not their turn
    assert game_state.is_move_valid(Player.white, 0, 6, 0, 5) is False
    # no move
    assert game_state.is_move_valid(Player.white, 0, 1, 0, 1) is False
    # attempt to occupy a cell occupied by another own piece
    assert game_state.is_move_valid(Player.white, 0, 3, 1, 3) is False
    # attempt to move something from an empty cell
    assert game_state.is_move_valid(Player.white, 3, 3, 3, 4) is False

    # neither a rook, nor a bishop, nor a queen can go through another piece
    assert game_state.is_move_valid(Player.white, 0, 0, 0, 4) is False
    assert game_state.is_move_valid(Player.white, 4, 0, 4, 2) is False
    assert game_state.is_move_valid(Player.white, 2, 0, 4, 2) is False

    # a pawn can't move more than 2 cells ahead
    assert game_state.is_move_valid(Player.white, 0, 1, 0, 4) is False
    # examples of valid moves with a pawn
    assert game_state.is_move_valid(Player.white, 0, 1, 0, 2) is True
    assert game_state.is_move_valid(Player.white, 0, 1, 0, 3) is True

    # knight
    assert game_state.is_move_valid(Player.white, 1, 0, 2, 2) is True
    assert game_state.is_move_valid(Player.white, 1, 0, 0, 2) is True
    assert game_state.is_move_valid(Player.white, 1, 0, 1, 2) is False

    # king shouldn't get or stay under attack
    #    k
    #   /b
    #  B
    #
    #    K
    game_state = GameState(board_position=Board(positions=[
        (Player.black, Piece.king, 3, 4),
        (Player.black, Piece.bishop, 3, 3),
        (Player.white, Piece.king, 3, 0),
        (Player.white, Piece.bishop, 1, 2)
    ]), whos_turn=Player.black)
    assert game_state.is_move_valid(Player.black, 3, 7, 2, 6) is False
    assert game_state.is_move_valid(Player.black, 3, 6, 2, 5) is False

def test_is_checkmated():
    """
    Check simple cases: on diagram below, white (upper case)
    are expected to be checkmated when black have 2 rooks,
    and not to be checkmated when black have either 1 rook:

    rr k
    
    K
    """
    game_state = GameState()
    # neither player is checkmated on start
    assert game_state.is_checkmated(Player.black) is False
    assert game_state.is_checkmated(Player.white) is False

    game_state = GameState(board_position=Board(positions=[
        (Player.white, Piece.king, 0, 0),
        (Player.black, Piece.king, 3, 2),
        (Player.black, Piece.rook, 0, 2),
        (Player.black, Piece.rook, 1, 2),
    ]), whos_turn=Player.white)
    assert game_state.is_checkmated(Player.white) is True

    game_state = GameState(board_position=Board(positions=[
        (Player.white, Piece.king, 0, 0),
        (Player.black, Piece.king, 3, 2),
        (Player.black, Piece.rook, 0, 2),
    ]), whos_turn=Player.white)
    assert game_state.is_checkmated(Player.white) is False

    game_state = GameState(board_position=Board(positions=[
        (Player.white, Piece.king, 0, 0),
        (Player.black, Piece.king, 3, 2),
        (Player.black, Piece.rook, 1, 2),
    ]), whos_turn=Player.white)
    assert game_state.is_checkmated(Player.white) is False

def test_promote():
    """ Check that promotes only a pawn on the "last" line only to correct pieces """
    game_state = GameState(board_position=Board(positions=[
        (Player.white, Piece.king, 4, 0),
        (Player.white, Piece.pawn, 0, 7),
        (Player.white, Piece.pawn, 0, 0),
        (Player.black, Piece.king, 4, 7),
        (Player.black, Piece.bishop, 6, 0),
    ]))
    # empty cell
    assert game_state.promote(Player.white, 0, 3, Piece.queen) is False
    # not their piece
    assert game_state.promote(Player.black, 0, 7, Piece.queen) is False
    # not on the last line
    assert game_state.promote(Player.white, 0, 0, Piece.queen) is False
    # can't keep being a pawn
    assert game_state.promote(Player.white, 0, 7, Piece.pawn) is False
    # can't become a king
    assert game_state.promote(Player.white, 0, 7, Piece.king) is False
    # not a pawn
    assert game_state.promote(Player.black, 6, 0, Piece.queen) is False

    # correct promotion
    assert game_state.promote(Player.white, 0, 7, Piece.queen) is True
    updated_cell = game_state.get_board().cells[0][7]
    assert updated_cell is not None
    assert updated_cell.piece == Piece.queen

