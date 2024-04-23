"""
Session describes everything related to a game of two players:

- the state of the game (board),
- secrets (white, black, join).

Join secret is something that allows a player to join a specific game.
White/black secrets should be kept safe, while join secret is intended
to be passed to one player so that they can invite the other;
hence, it can only be used once.

Session a simple container: it doesn't provide any secret protection logic
(should be implemented in the GameSessionsManager) or serialization.

Current implementation implies that there's just one join_secret
which white passes to black to join and once they do, it is removed.

Logic for more complex cases (joining by the same secret)
may be implemented later by adding a join method
and moving generation of player secrets there from __init__.
"""

import uuid
from typing import Union
from dataclasses import dataclass
from .game_domain.state import GameState

@dataclass
class GameSession:
    """ {module_docstring} """
    def __init__(self):
        self.white_secret = str(uuid.uuid4())
        self.join_secret: Union[str, None] = str(uuid.uuid4())
        self.black_secret = str(uuid.uuid4())
        self.game_state = GameState()

GameSession.__doc__ = str(GameSession.__doc__).format(module_docstring=__doc__)
