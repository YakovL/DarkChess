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
