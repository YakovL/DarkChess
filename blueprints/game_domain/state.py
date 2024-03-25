"""
Game state consists of the board state (what does each cell contain, .board),
who's turn it is (._whos_turn),

method to validate and to make a move, and

getters of
- the state itself (to save in a DB if needed),
- what the board looks like for each player, and
- whether anyone has won (or draw).
"""
from enum import Enum
from typing import Union

Player = Enum('Player', 'white black')
Piece = Enum('Piece', 'pawn rook bishop knight queen king')

class PlayerPiece:
    """ Black bishop, etc. """
    def __init__(self, player: Player, piece: Piece):
        self.player = player
        self.piece = piece

class Board:
    """
    Holds a 2D array of PlayerPiece-s, x, y,
    can be initialized with a list of (player, piece, x, y).
    If the positions list is omitted, the start game position is used.
    """
    def __init__(self, positions: list[tuple[Player, Piece, int, int]] = [
        (Player.white, Piece.rook, 0, 0),
        (Player.white, Piece.knight, 1, 0),
        (Player.white, Piece.bishop, 2, 0),
        (Player.white, Piece.king, 3, 0),
        (Player.white, Piece.queen, 4, 0),
        (Player.white, Piece.bishop, 5, 0),
        (Player.white, Piece.knight, 6, 0),
        (Player.white, Piece.rook, 7, 0),
        (Player.white, Piece.pawn, 0, 1),
        (Player.white, Piece.pawn, 1, 1),
        (Player.white, Piece.pawn, 2, 1),
        (Player.white, Piece.pawn, 3, 1),
        (Player.white, Piece.pawn, 4, 1),
        (Player.white, Piece.pawn, 5, 1),
        (Player.white, Piece.pawn, 6, 1),
        (Player.white, Piece.pawn, 7, 1),
        (Player.black, Piece.pawn, 0, 6),
        (Player.black, Piece.pawn, 1, 6),
        (Player.black, Piece.pawn, 2, 6),
        (Player.black, Piece.pawn, 3, 6),
        (Player.black, Piece.pawn, 4, 6),
        (Player.black, Piece.pawn, 5, 6),
        (Player.black, Piece.pawn, 6, 6),
        (Player.black, Piece.pawn, 7, 6),
        (Player.black, Piece.rook, 0, 7),
        (Player.black, Piece.knight, 1, 7),
        (Player.black, Piece.bishop, 2, 7),
        (Player.black, Piece.king, 3, 7),
        (Player.black, Piece.queen, 4, 7),
        (Player.black, Piece.bishop, 5, 7),
        (Player.black, Piece.knight, 6, 7),
        (Player.black, Piece.rook, 7, 7),
    ]):
        if len(positions) > 32:
            raise Exception('no more than 32 pieces are expected')
        # validate more, if needed (number of pieces, etc)

        self.cells: list[list[Union[PlayerPiece, None]]] = \
            [[None for _ in range(8)] for _ in range(8)]
        for position in positions:
            player, piece, x, y = position
            self.cells[x][y] = PlayerPiece(player, piece)

class State:
    """ Init with a standard game position """
    def __init__(self):
        self._whos_turn = Player.white
        self._board = Board()
    def get_whos_turn(self) -> Player:
        """ Get who's turn it is (only maks sense if there's no winner or draw) """
        return self._whos_turn
    def get_board(self):
        """ Get what's in each cell (PlayerPiece or None) """
        return self._board
