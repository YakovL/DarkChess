import { Player, Piece, CellContent } from '../model'
import classes from './board.module.css'

interface ICellProps {
  inside: CellContent
  x: number
  y: number
  isSelected: boolean
  onClick: () => void
};

const BoardCell = ({
  inside, x, y, onClick, isSelected
}: ICellProps) => {
  const displayPiece = (piece: Piece, player: Player) => (
    // TODO: get pictures for pieces, render
    // TODO: map color instead of using inside.player directly
    <span style={{ color: player }}>
      {(piece == 'knight' ? 'n' : piece[0]).toUpperCase()}
    </span>
  )

  return (
    <div
      title={`${x},${y}`}
      className={
        // TODO: pick colors more consistently
        `${classes.cell} ${
          inside == 'is_dark' ? classes.cell_dark : (x + y) % 2 == 0 ? classes.cell_odd : classes.cell_even
        } ${
          isSelected ? classes.cell_selected : ''
        }`}
      onClick={onClick}
    >
      {inside && inside != 'is_dark' && displayPiece(inside.piece, inside.player)}
    </div>
  )
}

interface IBoardProps {
  cells: CellContent[][]
  currentPlayer: Player
  isCurrentPlayerTurn: boolean
  makeMove: (from: { x: number, y: number }, to: { x: number, y: number }) => Promise<any>
}

export default function Board({
  cells,
  currentPlayer,
  isCurrentPlayerTurn,
  makeMove,
}: IBoardProps) {

}
