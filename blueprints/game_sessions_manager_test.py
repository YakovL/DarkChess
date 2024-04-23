from .game_sessions_manager import GameSessionsManager

def test_create_session():
    session_manager = GameSessionsManager()

    # should return a BoardView and a secret (not None; other things are tested in GameState)
    white_secret, board_view__white = session_manager.create_session()
    assert white_secret is not None
    assert board_view__white is not None

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
