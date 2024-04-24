"""
Application layer of the game

See secrets' description in GameSession.
"""
from typing import Union
from dataclasses import dataclass
from .game_domain.state import Player, BoardView
from .storage import GameSessionsStorage

@dataclass
class PlayerViewAndStats:
    """ A container of output data telling player "what's going on?" """
    def __init__(self,
                 player_view: BoardView,
                 is_our_king_under_attack: bool,
                 is_their_king_under_attack: bool,
                 winner: Union[Player, None],
                 ):
        self.player_view = player_view
        self.is_our_king_under_attack = is_our_king_under_attack
        self.is_their_king_under_attack = is_their_king_under_attack
        self.winner = winner

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

    def join_session(self, join_secret: str):
        """
        Get the player secret by join_secret.
        Currently removes the join_secret right away so that it can't be used twice;
        it also only allows to join via join_secret and not the black_secret.
        Returns (black_secret, black_board_view)
        """
        session = self.storage.get_session_by_secret(join_secret)
        if session is None:
            return None

        # Don't allow joining by player's secret: otherwise white could obtain it,
        # pass to black as a join secret, and be able to see their view
        if session.join_secret != join_secret:
            return None

        # If black loses the response, they won't be able to join
        session.join_secret = None
        return (session.black_secret, session.game_state.get_board_view(Player.black))

