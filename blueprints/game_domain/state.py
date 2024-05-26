"""
This describes the whole game domain logic.

The modification of standart chess is the limited visibility of the board,
calced in the get_board_view method. This is an experimental feature, and
may be modified in the future versions. 

Here's an example of a board and it's views for both players:

    k        XXXXXXX    XXX k XX
P           PXXXXXXX    PXX   XX
            XXXXXXXX    X XXXXXX
            XXXXXXXX    XX XXXXX
            XXXXXXXX    XXX XXXX
            XXXXXXXX    XXXX XXX
            XXX   XX    XXXXX X
    K b     XXX K XX    XXXXXXbX


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
from typing import TypedDict
from dataclasses import dataclass
from copy import deepcopy

Player = Enum('Player', 'white black')
Piece = Enum('Piece', 'pawn rook bishop knight queen king')

# unlike TypedDict, dataclass makes Enum props json-serializable
@dataclass
class PlayerPiece:
    """ Black bishop, etc. """
    player: Player
    piece: Piece

@dataclass
class Board:
    """
    Holds a 2D array of PlayerPiece-s, x, y,
    can be initialized with a list of (player, piece, x, y).
    If the positions list is omitted, the start game position is used.
    """
    def __init__(self, positions: list[tuple[Player, Piece, int, int]] | None = None):
        if not positions:
            positions = [
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
            ]

        if len(positions) > 32:
            raise Exception('no more than 32 pieces are expected')
        # validate more, if needed (number of pieces, etc)

        self.cells: list[list[PlayerPiece | None]] = \
            [[None for _ in range(8)] for _ in range(8)]
        for position in positions:
            player, piece, x, y = position
            self.cells[x][y] = PlayerPiece(player, piece)

#TODO: use Python 3.10 and Literal Type (Literal['is_dark']) instead
class IsDark:
    def to_json(self):
        return 'is_dark'
BoardViewCell = PlayerPiece | IsDark | None
BoardView = list[list[BoardViewCell]]

class GameState:
    """ Init with a standard game position by default """
    def __init__(self, whos_turn: Player = Player.white, board_position: Board | None = None):
        self._whos_turn = whos_turn
        self.is_waiting_for_promotion = False
        self._board = board_position if board_position else Board()
    def to_dict(self):
        """ For JSON serialization """
        return {
            'is_waiting_for_promotion': self.is_waiting_for_promotion,
            'whos_turn': self._whos_turn.name,
            'board': self._board
        }

    def get_whos_turn(self) -> Player:
        """ Get who's turn it is (only maks sense if there's no winner or draw) """
        return self._whos_turn
    def get_board(self):
        """ Get what's in each cell (PlayerPiece or None) """
        return self._board
    def get_player_pieces_coordinates(self, player: Player) -> list[tuple[int, int]]:
        """ Get the coordinates of all player's pieces """
        return [
            (x, y)
            for x in range(8)
            for y in range(8)
            if (in_cell := self._board.cells[x][y]) is not None
            and in_cell.player == player
        ]

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
            y = y_from + (x - x_from) * (y_to - y_from) / (x_to - x_from)
            if self._board.cells[x][int(y)] is not None:
                return False
        return True
    def is_king_under_attack(self, king_owner: Player):
        """ Check if the king is under attack """
        opponent = Player.black if king_owner == Player.white else Player.white
        opponent_pieces_coordinates: list[tuple[int, int]] = []
        king_coordinates = None
        for x in range(8):
            for y in range(8):
                in_cell = self._board.cells[x][y]
                if in_cell is None: continue
                if in_cell.player == opponent:
                    opponent_pieces_coordinates.append((x, y))
                if in_cell.player == king_owner and in_cell.piece == Piece.king:
                    king_coordinates = (x, y)
        if king_coordinates is None:
            return False

        for cell_coordinates in opponent_pieces_coordinates:
            if self.is_move_valid(opponent,
                                  cell_coordinates[0], cell_coordinates[1],
                                  king_coordinates[0], king_coordinates[1]):
                return True
        return False
    def is_move_valid(self,
                      whos_turn: Player,
                      x_from: int,
                      y_from: int,
                      x_to: int,
                      y_to: int,
                      is_virtual: int = False) -> bool:
        """ Check if the move is valid """
        cell_from = self._board.cells[x_from][y_from]
        cell_to = self._board.cells[x_to][y_to]

        # only own piece, inside board, to a different cell, not occupied by another own piece
        if cell_from is None or cell_from.player != whos_turn or \
           x_to > 7 or y_to > 7 or x_to < 0 or y_to < 0 or \
           x_to == x_from and y_to == y_from or \
           cell_to is not None and cell_to.player == whos_turn:
            return False
        # already moved, has to promote
        if self.is_waiting_for_promotion:
            return False
        # shouldn't put their king under attack
        if not is_virtual:
            state_after_move = self.make_virtual_move(x_from, y_from, x_to, y_to)
            if state_after_move.is_king_under_attack(whos_turn):
                return False

        # check that this piece can make this move
        if cell_from.piece == Piece.knight:
            return abs(x_to - x_from) == 2 and abs(y_to - y_from) == 1 or \
                   abs(x_to - x_from) == 1 and abs(y_to - y_from) == 2

        if cell_from.piece == Piece.rook:
            if x_to != x_from and y_to != y_from:
                return False
            return self._is_empty_path(x_from, y_from, x_to, y_to)

        if cell_from.piece == Piece.bishop:
            if abs(x_to - x_from) != abs(y_to - y_from):
                return False
            return self._is_empty_diagonal_path(x_from, y_from, x_to, y_to)

        if cell_from.piece == Piece.queen:
            if x_to == x_from or y_to == y_from:
                return self._is_empty_path(x_from, y_from, x_to, y_to)
            if abs(x_to - x_from) == abs(y_to - y_from):
                return self._is_empty_diagonal_path(x_from, y_from, x_to, y_to)
            return False

        if cell_from.piece == Piece.pawn:
            # only correct direction
            if whos_turn == Player.white and y_to <= y_from or \
               whos_turn == Player.black and y_to >= y_from:
                return False

            # move forward
            if x_from == x_to:
                # no need to check the player:
                # wrong direction and moves to y = 8 or -1 are disallowed above
                return cell_to is None and (
                       abs(y_to - y_from) == 1 or \
                       abs(y_to - y_from) == 2 and y_from in (1, 6)
                )

            # capture
            if abs(x_from - x_to) > 1 or abs(y_from - y_to) > 1:
                return False

            #TODO: implement en passant
            return cell_to is not None #or \
            #       self._board.cells[x_to][y_from] is not None

        if cell_from.piece == Piece.king:
            #TODO: implement castling
            return abs(x_to - x_from) <= 1 and abs(y_to - y_from) <= 1

        # incorrect input
        return False

    def _pass_turn(self) -> None:
        self._whos_turn = Player.black if self._whos_turn == Player.white \
            else Player.white

    def make_move(self, x_from: int, y_from: int, x_to: int, y_to: int) -> None:
        """
        Change the state accordingly (without validation, as it would produce an infinite loop).
        Doesn't promote pawns, should be done separately.
        """
        if self.is_waiting_for_promotion:
            return

        moving_piece = self._board.cells[x_from][y_from]
        if moving_piece is None:
            return

        #TODO: implement en passant (if moving_piece.piece == Piece.pawn, ...)
        #TODO: implement castling (if moving_piece.piece == Piece.king, ...)

        self._board.cells[x_to][y_to] = moving_piece
        self._board.cells[x_from][y_from] = None

        self.is_waiting_for_promotion = moving_piece.piece == Piece.pawn and \
            (y_to == 0 and moving_piece.player == Player.black or \
             y_to == 7 and moving_piece.player == Player.white)

        if not self.is_waiting_for_promotion:
            self._pass_turn()

    def make_virtual_move(self, x_from: int, y_from: int, x_to: int, y_to: int) -> 'GameState':
        """ Create a new GameState, make the move in it, and return it """
        virtual_state = GameState(self._whos_turn, deepcopy(self._board))
        virtual_state.make_move(x_from, y_from, x_to, y_to)
        return virtual_state

    #TODO: optimize the approach to iterate possible moves
    def is_checkmated(self, player: Player) -> bool:
        """ Returns whether the player is checkmated, assuming it's their turn """
        if not self.is_king_under_attack(player):
            return False

        player_pieces_coordinates = self.get_player_pieces_coordinates(player)
        for x_from, y_from in player_pieces_coordinates:
            for x_to in range(8):
                for y_to in range(8):
                    if self.is_move_valid(player, x_from, y_from, x_to, y_to):

                        # for each possible move,
                        # check if it allows to get the king from under attack
                        possible_state = self.make_virtual_move(x_from, y_from, x_to, y_to)
                        if not possible_state.is_king_under_attack(player):
                            return False

        return True

    def promote(self, player: Player, x: int, y: int, piece: Piece) -> bool:
        """
        Promotes a pawn if it is in the given cell, is owned by the given player, etc.
        Returns True if everything is correct and the promotion was done (False otherwise).
        """
        # not checking self.is_waiting_for_promotion since checking conditions for it

        cell = self._board.cells[x][y]

        # should be their pawn
        if cell is None or cell.player != player or cell.piece is not Piece.pawn:
            return False

        # should reach the other end
        if player == Player.white and y != 7 or player == Player.black and y != 0:
            return False

        # not all pieces are allowed to promote into
        if piece in { Piece.king, Piece.pawn }:
            return False

        self._board.cells[x][y] = PlayerPiece(player, piece)
        self.is_waiting_for_promotion = False
        self._pass_turn()
        return True

    def get_board_view(self, player: Player) -> BoardView:
        """ Returns the board view of the given player """
        view: BoardView = [[None for _ in range(8)] for _ in range(8)]
        class PieceOnBoard(TypedDict):
            """ This is just to type player_pieces here """
            piece: Piece
            x: int
            y: int
        player_pieces: list[PieceOnBoard] = []

        # copy pieces into the view and gather player_pieces
        for x in range(8):
            for y in range(8):
                piece_in_cell = self._board.cells[x][y]
                view[x][y] = piece_in_cell

                if piece_in_cell is not None and piece_in_cell.player == player:
                    player_pieces.append({ 'piece': piece_in_cell.piece, 'x': x, 'y': y })

        # calc visibility mask
        visibility_mask = [[False for _ in range(8)] for _ in range(8)]
        for piece in player_pieces:
            for x in range(8):
                for y in range(8):
                    if visibility_mask[x][y]:
                        continue

                    # the cell is visible if their piece occupies it or can move to it
                    if piece['x'] == x and piece['y'] == y:
                        visibility_mask[x][y] = True
                        continue
                    if self.is_move_valid(player, piece['x'], piece['y'], x, y, is_virtual=True):
                        visibility_mask[x][y] = True

        # apply visibility mask
        for x in range(8):
            for y in range(8):
                if not visibility_mask[x][y]:
                    view[x][y] = IsDark()

        return view

