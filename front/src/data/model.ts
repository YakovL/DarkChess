export type Player = 'black' | 'white'
export type Piece = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn'
export type PlayerPiece = {
  player: Player;
  piece: Piece;
}
export type CellContent = PlayerPiece | 'is_dark' | null
