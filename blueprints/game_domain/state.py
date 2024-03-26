"""
This describes the whole game domain logic

Game state consists of the board state (what does each cell contain, .board),
who's turn it is (._whos_turn),

method to validate and to make a move, and

getters of
- the state itself (to save in a DB if needed),
- what the board looks like for each player, and
- whether anyone has won (or it's a draw).

Note: whites are on the bottom of the Board (y = 0, 1),
board view is not rotated for blacks (should be done on UI level).
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
    """ Init with a standard game position by default """
    def __init__(self, whos_turn: Player = Player.white, board_position: Board = Board()):
        self._whos_turn = whos_turn
        self._board = board_position
    def get_whos_turn(self) -> Player:
        """ Get who's turn it is (only maks sense if there's no winner or draw) """
        return self._whos_turn
    def get_board(self):
        """ Get what's in each cell (PlayerPiece or None) """
        return self._board

    def _is_empty_path(self, x_from: int, y_from: int, x_to: int, y_to: int) -> bool:
        if x_from == x_to:
            for y in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                if self._board.cells[x_from][y] is not None:
                    return False
            return True

        if y_from == y_to:
            for x in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                if self._board.cells[x][y_from] is not None:
                    return False
            return True

        # incorrect input
        return False
    def _is_empty_diagonal_path(self, x_from: int, y_from: int, x_to: int, y_to: int) -> bool:
        # incorrect input
        if abs(x_to - x_from) != abs(y_to - y_from):
            return False

        for x in range(min(x_from, x_to) + 1, max(x_from, x_to)):
            y = y_from + (x - min(x_from, x_to)) * (y_to - y_from) / (x_to - x_from)
            if self._board.cells[x][int(y)] is not None:
                return False
        return True
    def is_move_valid(self,
                      whos_turn: Player,
                      x_from: int,
                      y_from: int,
                      x_to: int,
                      y_to: int) -> bool:
        """ Check if the move is valid """
        cell_from = self._board.cells[x_from][y_from]
        cell_to = self._board.cells[x_to][y_to]

        # only own piece, inside board, to a different cell, not occupied by another own piece
        if cell_from is None or cell_from.player != whos_turn or \
           x_to > 7 or y_to > 7 or x_to < 0 or y_to < 0 or \
           x_to == x_from and y_to == y_from or \
           cell_to is not None and cell_to.player == whos_turn:
            return False
        #TODO: prevent a move that causes checkmate (and make sure there's no infinite loop)

        # check that this piece can make this move
        if cell_from.piece == Piece.knight:
            return abs(x_to - x_from) == 2 and abs(y_to - y_from) == 1 or \
                   abs(x_to - x_from) == 1 and abs(y_to - y_from) == 2

        if cell_from.piece == Piece.rook:
            if x_to != x_from and y_to == y_from:
                return False
            return self._is_empty_path(x_from, y_from, x_to, y_to)

        if cell_from.piece == Piece.bishop:
            if abs(x_to - x_from) != abs(y_to - y_from):
                return False
            return self._is_empty_diagonal_path(x_from, y_from, x_to, y_to)

        if cell_from.piece == Piece.queen:
            if x_to != x_from and y_to == y_from:
                return self._is_empty_path(x_from, y_from, x_to, y_to)
            if abs(x_to - x_from) != abs(y_to - y_from):
                return self._is_empty_diagonal_path(x_from, y_from, x_to, y_to)
            return False

        if cell_from.piece == Piece.pawn:
            if whos_turn == Player.white and y_to < y_from or \
               whos_turn == Player.black and y_to > y_from:
                return False

            if x_from == x_to:
                # no need to check the player:
                # wrong direction and moves to y = 8 or -1 are disallowed above
                return (abs(y_to - y_from) == 1) or \
                       (abs(y_to - y_from) == 2 and y_from in (1, 6))

            # capture
            #TODO: implement en passant
            if abs(x_from - x_to) > 1 or abs(y_from - y_to) > 1: # or y_from == y_to:
                return False

            return cell_to is not None or \
                   self._board.cells[x_to][y_from] is not None

        if cell_from.piece == Piece.king:
            #TODO: implement castling
            return abs(x_to - x_from) <= 1 and abs(y_to - y_from) <= 1

        # incorrect input
        return False
