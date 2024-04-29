from .game_sessions_manager import GameSessionsManager
from .serialization import to_json
from .game_domain.state import Player, IsDark

def test_create_session():
    session_manager = GameSessionsManager()

    # should return a BoardView and a secret (not None; other things are tested in GameState)
    white_secret, board_view__white = session_manager.create_session()
    assert white_secret is not None
    assert board_view__white is not None

    # same board view each time, different secrets
    white_secret_2, board_view__white_2 = session_manager.create_session()
    assert white_secret_2 != white_secret
    assert to_json(board_view__white) == to_json(board_view__white_2)

def test_get_join_secret():
    session_manager = GameSessionsManager()
    white_secret, _ = session_manager.create_session()

    join_secret = session_manager.get_join_secret(white_secret)
    assert join_secret is not None
    assert join_secret != white_secret

    # idempotent
    join_secret_again = session_manager.get_join_secret(white_secret)
    assert join_secret_again == join_secret

    non_existing_secret = 'some garbage'
    join_secret = session_manager.get_join_secret(non_existing_secret)
    assert join_secret is None

def test_join_session():
    session_manager = GameSessionsManager()
    white_secret, board_view__white = session_manager.create_session()
    join_secret = session_manager.get_join_secret(white_secret)
    if join_secret is None:
        raise ValueError('join_secret is None')

    non_existing_secret = 'some garbage'
    result = session_manager.join_session(non_existing_secret)
    assert result is None

    result = session_manager.join_session(white_secret)
    assert result is None

    # should return a BoardView and a secret, like create_session
    result = session_manager.join_session(join_secret)
    assert result is not None
    black_secret, board_view__black = result
    assert black_secret is not None
    assert board_view__black is not None

    assert black_secret != white_secret
    assert black_secret != join_secret
    assert to_json(board_view__white) != to_json(board_view__black)

    join_secret_after_join = session_manager.get_join_secret(white_secret)
    assert join_secret_after_join is None

def test_get_player_view_and_stats():
    session_manager = GameSessionsManager()
    white_secret, board_view__white = session_manager.create_session()

    player_view_and_stats__white = session_manager.get_player_view_and_stats(white_secret)
    assert player_view_and_stats__white is not None
    assert to_json(player_view_and_stats__white.player_view) == to_json(board_view__white)
    assert player_view_and_stats__white.is_their_king_under_attack is False
    assert player_view_and_stats__white.is_our_king_under_attack is False
    assert player_view_and_stats__white.winner is None

def test_validate_move():
    session_manager = GameSessionsManager()
    white_secret, _ = session_manager.create_session()
    join_secret = session_manager.get_join_secret(white_secret)
    if not join_secret:
        raise ValueError('join_secret is None')
    join_result = session_manager.join_session(join_secret)
    if not join_result:
        raise ValueError('join_result is None')
    black_secret = join_result[0]

    # wrong secret shouldn't work
    assert session_manager.validate_move('some garbage', 0, 1, 0, 2) is None
    # join_secret shouldn't work
    assert session_manager.validate_move(join_secret, 0, 1, 0, 2) is None
    # other player's secret shouldn't work
    assert session_manager.validate_move(black_secret, 0, 1, 0, 2) is None

    # not their turn
    assert session_manager.validate_move(black_secret, 0, 6, 0, 5) is None

    # incorrect (pawn) move
    assert session_manager.validate_move(white_secret, 0, 1, 1, 2) is None
    # a non-move
    assert session_manager.validate_move(white_secret, 0, 1, 0, 1) is None

    # an example of a valid move
    assert session_manager.validate_move(white_secret, 0, 1, 0, 2) is not None

def test_make_move():
    session_manager = GameSessionsManager()
    white_secret, _ = session_manager.create_session()

    # an incorrect move (i.e. validation is used before applying)
    assert session_manager.make_move(white_secret, 0, 1, 1, 2) is None

    # a valid move
    x_from = 0
    y_from = 1
    x_to = 0
    y_to = 2
    move_result = session_manager.make_move(white_secret, x_from, y_from, x_to, y_to)
    assert move_result is not None
    assert move_result.whos_turn is Player.black

    in_cell_where_moved = move_result.player_view[x_to][y_to]
    assert in_cell_where_moved is not None
    assert isinstance(in_cell_where_moved, IsDark) is False
    if isinstance(in_cell_where_moved, IsDark):
        raise ValueError('in_cell_where_moved is dark, expected a piece')
    assert in_cell_where_moved.player is Player.white

    assert move_result.player_view[x_from][y_from] is None
