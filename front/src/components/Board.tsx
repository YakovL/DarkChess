import { useState } from 'react'
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

  const [selectedCell, setSelectedCell] = useState<{ x: number, y: number } | null>(null)
  const onCellClick = (x: number, y: number) => {
    if(!isCurrentPlayerTurn) {
      // TODO: provide visual feedback (or show the whole board so that it's clear that "it's their turn")
      return
    }

    const inCell = cells[x][y]
    const hasClickedOwnPiece = inCell &&
      inCell != 'is_dark' &&
      inCell.player == currentPlayer

    // unselect
    if(selectedCell && selectedCell.x == x && selectedCell.y == y) {
      setSelectedCell(null)
      return
    }

    // select or reselect (another piece)
    if(!selectedCell || hasClickedOwnPiece) {
      if(hasClickedOwnPiece) {
        setSelectedCell({ x, y })
      } else {
        // TODO: maybe provide visual feedback
      }
      return
    }

    makeMove(selectedCell, { x, y })
    // TODO: provide visual feedback, maybe optimistic
    setSelectedCell(null)
  }

  return (
    <div className={classes.board}>
      {// rendering goes from top to bottom, in reverse to the y axis
      (['top', 7, 6, 5, 4, 3, 2, 1, 0, 'bottom'] as const).map(y =>
        (['left', 0, 1, 2, 3, 4, 5, 6, 7, 'right'] as const).map(x =>
          // gutters
          x == 'left' || x == 'right' ?
          <div className={classes.gutter}>{
            typeof y == 'number' ? y : ''
          }</div> :
          y == 'top' || y == 'bottom' ?
          <div className={classes.gutter}>{
            typeof x == 'number' ? String.fromCharCode('A'.charCodeAt(0) + x) : ''
          }</div> :

          <BoardCell
            key={`${x},${y}`}
            x={x} y={y}
            inside={cells[x][y]}
            isSelected={selectedCell?.x == x && selectedCell?.y == y}
            onClick={() => onCellClick(x, y)}
          />
        ).reduce((jsx, cellJSX) => <>{jsx}{cellJSX}</>)
      ).reduce((jsx, cellJSX) => <>{jsx}{cellJSX}</>)}
    </div>
  )
}
