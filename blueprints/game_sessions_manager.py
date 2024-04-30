"""
Application layer of the game

See secrets' description in GameSession.
"""
from dataclasses import dataclass
from .game_domain.state import Player, BoardView
from .storage import GameSessionsStorage
from .game_session import GameSession

@dataclass
class PlayerViewAndStats:
    """ A container of output data telling player "what's going on?" """
    def __init__(self,
                 player_view: BoardView,
                 whos_turn: Player,
                 is_waiting_for_promotion: bool,
                 is_our_king_under_attack: bool,
                 is_their_king_under_attack: bool,
                 winner: Player | None,
                 ):
        self.player_view = player_view
        self.whos_turn = whos_turn
        self.is_waiting_for_promotion = is_waiting_for_promotion
        self.is_our_king_under_attack = is_our_king_under_attack
        self.is_their_king_under_attack = is_their_king_under_attack
        self.winner = winner

class GameSessionsManager:
    """
    Exposes application methods like creating a session,
    joining it and making a move, to the framework (API, WS or any other)
    """
    def __init__(self, storage: GameSessionsStorage):
        self.storage = storage

    def create_session(self) -> tuple[str, BoardView]:
        """
        Creates a new game session in the storage,
        returns (white_secret, board_view__white).

        Implies that the player with white pieces invites the other player.
        """
        session = self.storage.create_session()
        return (session.white_secret, session.game_state.get_board_view(Player.white))

    def get_join_secret(self, white_secret: str) -> str | None:
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

    def get_player_view_and_stats(self, secret: str) -> PlayerViewAndStats | None:
        """
        "View" method for the player: gives all the necessary info about the game.
        Can be used in polling, pushed via WS, or reused in methods like make_move.
        Returns None when the session is not found by secret.
        """
        session = self.storage.get_session_by_secret(secret)
        if session is None:
            return None
        if not secret in (session.black_secret, session.white_secret):
            return None
        us = Player.black if secret == session.black_secret else Player.white
        them = Player.white if secret == session.black_secret else Player.black

        winner = Player.white if session.game_state.is_checkmated(Player.black) else \
                 Player.black if session.game_state.is_checkmated(Player.white) else \
                 None

        return PlayerViewAndStats(
            session.game_state.get_board_view(us),
            session.game_state.get_whos_turn(),
            session.game_state.is_waiting_for_promotion,
            session.game_state.is_king_under_attack(us),
            session.game_state.is_king_under_attack(them),
            winner)

    def validate_move(self,
                      secret: str,
                      x_from: int,
                      y_from: int,
                      x_to: int,
                      y_to: int) -> GameSession | None:
        """
        Checks move validity: returns None when invalid, session otherwise
        """
        session = self.storage.get_session_by_secret(secret)
        if session is None:
            return None

        whos_turn = session.game_state.get_whos_turn()
        if whos_turn == Player.white and session.white_secret != secret or \
           whos_turn == Player.black and session.black_secret != secret:
            return None

        if session.game_state.is_move_valid(whos_turn, x_from, y_from, x_to, y_to):
            return session
        return None

    def _make_move_get_session(self,
                               secret: str,
                               x_from: int,
                               y_from: int,
                               x_to: int,
                               y_to: int) -> GameSession | None:
        session = self.validate_move(secret, x_from, y_from, x_to, y_to)
        if not session:
            return None

        session.game_state.make_move(x_from, y_from, x_to, y_to)
        return session

    def make_move(self, secret: str, x_from: int, y_from: int, x_to: int, y_to: int):
        """ Validate the move, make if valid, return PlayerViewAndStats """
        session = self._make_move_get_session(secret, x_from, y_from, x_to, y_to)
        if not session:
            return None

        #TODO (perf): instead of getting session by secret again, overload get_player_view_and_stats and
        # pass the session (should return result for whos_turn)
        return self.get_player_view_and_stats(secret)
