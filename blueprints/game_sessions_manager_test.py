from .game_sessions_manager import GameSessionsManager

def test_create_session():
    session_manager = GameSessionsManager()

    # should return a BoardView and a secret (not None; other things are tested in GameState)
    white_secret, board_view__white = session_manager.create_session()
    assert white_secret is not None
    assert board_view__white is not None
