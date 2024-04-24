from .game_sessions_manager import GameSessionsManager
from .serialization import to_json

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
