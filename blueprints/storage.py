"""
Simple in-memory storage of sessions.
"""

from abc import ABC, abstractmethod
from .game_session import GameSession

class IGameSessionStorage(ABC):
    """
    An abstract class (interface) to allow dependency injections and mocking
    """
    @abstractmethod
    def create_session(self) -> GameSession:
        """ Create a new session, store and return it """

    @abstractmethod
    def get_session_by_secret(self, secret: str) -> GameSession | None:
        """ Find session by any secret (join, white, black) """

class GameSessionsStorage(IGameSessionStorage):
    """
    Simple in-memory storage of sessions.
    """
    def __init__(self):
        self.sessions: list[GameSession] = []

    def create_session(self):
        """ Create a new session, store and return it """
        session = GameSession()
        self.sessions.append(session)
        return session

    def get_session_by_secret(self, secret: str):
        """ Find session by any secret (join, white, black) """
        for session in self.sessions:
            if secret in { session.white_secret, session.join_secret, session.black_secret }:
                return session
        return None

