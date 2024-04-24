import json
from .serialization import to_json
from .game_session import GameSession

def test_serializes_game_session():
    session = GameSession()

    session_json = to_json(session)

    assert json is not None
    assert isinstance(session_json, str)

