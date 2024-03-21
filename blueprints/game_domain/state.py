"""
Game state consists of the board state (what does each cell contain, .board),
who's turn it is (.whos_turn),

method to validate and to make a move, and

getters of
- the state itself (to save in DB),
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
        (Player.white, Piece.knight, 0, 1),
        (Player.white, Piece.bishop, 0, 2),
        (Player.white, Piece.king, 0, 3),
        (Player.white, Piece.queen, 0, 4),
        (Player.white, Piece.bishop, 0, 5),
        (Player.white, Piece.knight, 0, 6),
        (Player.white, Piece.rook, 0, 7),
        (Player.white, Piece.pawn, 1, 0),
        (Player.white, Piece.pawn, 1, 1),
        (Player.white, Piece.pawn, 1, 2),
        (Player.white, Piece.pawn, 1, 3),
        (Player.white, Piece.pawn, 1, 4),
        (Player.white, Piece.pawn, 1, 5),
        (Player.white, Piece.pawn, 1, 6),
        (Player.white, Piece.pawn, 1, 7),
        (Player.black, Piece.pawn, 6, 0),
        (Player.black, Piece.pawn, 6, 1),
        (Player.black, Piece.pawn, 6, 2),
        (Player.black, Piece.pawn, 6, 3),
        (Player.black, Piece.pawn, 6, 4),
        (Player.black, Piece.pawn, 6, 5),
        (Player.black, Piece.pawn, 6, 6),
        (Player.black, Piece.pawn, 6, 7),
        (Player.black, Piece.rook, 7, 0),
        (Player.black, Piece.knight, 7, 1),
        (Player.black, Piece.bishop, 7, 2),
        (Player.black, Piece.king, 7, 3),
        (Player.black, Piece.queen, 7, 4),
        (Player.black, Piece.bishop, 7, 5),
        (Player.black, Piece.knight, 7, 6),
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
    def __init__(self):
        self.whos_turn = Player.white
        self.board = Board()