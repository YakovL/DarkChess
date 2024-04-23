"""
Application layer of the game

See secrets' description in GameSession.
"""
from typing import Union
from .game_domain.state import Player, BoardView
from .storage import GameSessionsStorage

class GameSessionsManager:
    """
    Exposes application methods like creating a session,
    joining it and making a move, to the framework (API, WS or any other)
    """
    def __init__(self):
        self.storage = GameSessionsStorage()

    def create_session(self) -> tuple[str, BoardView]:
        """
        Creates a new game session in the storage,
        returns (white_secret, board_view__white).

        Implies that the player with white pieces invites the other player.
        """
        session = self.storage.create_session()
        return (session.white_secret, session.game_state.get_board_view(Player.white))

    def get_join_secret(self, white_secret: str) -> Union[str, None]:
        """ Finds a session by white_secret, returns join_secret or None if not found """
        session = self.storage.get_session_by_secret(white_secret)
        if session is None or session.white_secret != white_secret:
            return None
        return session.join_secret

