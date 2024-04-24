import json
from .serialization import to_json
from .game_session import GameSession
from .game_sessions_manager import PlayerViewAndStats
from .game_domain.state import Player

def test_serializes_game_session():
    session = GameSession()

    session_json = to_json(session)

    assert json is not None
    assert isinstance(session_json, str)

def test_serializes_player_view_and_stats():
    session = GameSession()
    board_view__black = session.game_state.get_board_view(Player.black)
    player_view_and_stats = PlayerViewAndStats(board_view__black, False, False, None)

    player_view_and_stats_json = to_json(player_view_and_stats)

    assert json is not None
    assert isinstance(player_view_and_stats_json, str)
