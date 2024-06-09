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

const theme = {
  Piece: ({ player, piece }: { player: Player, piece: Piece }) => {
    return (
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
        <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g>
        <g id="SVGRepo_iconCarrier">
        {piece == 'pawn' &&
          <path fillRule="evenodd" clipRule="evenodd" fill={player == "white" ? "#FFFFFF" : "#000000"} d="M9.5 6.5C9.5 5.11929 10.6193 4 12 4C13.3807 4 14.5 5.11929 14.5 6.5C14.5 7.88071 13.3807 9 12 9C10.6193 9 9.5 7.88071 9.5 6.5ZM12 2C9.51472 2 7.5 4.01472 7.5 6.5C7.5 7.91363 8.15183 9.17502 9.17133 10H8C7.44772 10 7 10.4477 7 11C7 11.5523 7.44772 12 8 12H9.12533C9.15208 12.3659 9.16098 12.833 9.11237 13.3535C8.99568 14.6027 8.55656 16.0909 7.31094 17.2753C6.86615 17.6982 6.19221 18.1531 5.58717 18.5199C5.29266 18.6984 5.02896 18.8475 4.83934 18.9517C4.74472 19.0037 4.66905 19.0442 4.61781 19.0713L4.56008 19.1017L4.54633 19.1088L4.54347 19.1103L4.54336 19.1103L4.54322 19.1104C4.3106 19.2299 4.13401 19.4357 4.05132 19.6838L3.27924 22H3C2.44772 22 2 22.4477 2 23C2 23.5523 2.44772 24 3 24H4H20H21C21.5523 24 22 23.5523 22 23C22 22.4477 21.5523 22 21 22H20.7659L20.1559 19.7395C20.0787 19.4533 19.8784 19.2161 19.6092 19.0919L19.609 19.0918L19.6072 19.091L19.5951 19.0853C19.5836 19.0799 19.5655 19.0714 19.5415 19.0598C19.4933 19.0366 19.4214 19.0014 19.3304 18.9553C19.1482 18.8629 18.8918 18.7279 18.5996 18.5595C18.0041 18.2164 17.3055 17.7605 16.7767 17.2682C15.5139 16.0923 15.054 14.6022 14.92 13.349C14.8647 12.8316 14.8667 12.3662 14.8878 12H16C16.5523 12 17 11.5523 17 11C17 10.4477 16.5523 10 16 10H14.8287C15.8482 9.17502 16.5 7.91363 16.5 6.5C16.5 4.01472 14.4853 2 12 2ZM11.1037 13.5395C11.158 12.9576 11.1549 12.4315 11.1296 12H12.8852C12.8649 12.4363 12.8682 12.9705 12.9313 13.5616C13.0971 15.112 13.6847 17.1218 15.4138 18.7319C15.512 18.8233 15.6134 18.9128 15.717 19L8.38107 19C8.48825 18.9094 8.59149 18.8175 8.68906 18.7247C10.3982 17.0996 10.9591 15.0879 11.1037 13.5395ZM5.72076 21L18.4246 21L18.6944 22H5.38743L5.72076 21Z"></path>}
          {/* TODO: grab the rest from svgrepo.com/collection/zest-interface-icons/?search=chess , use in BoardCell */}
          {/* TODO: move fill definition outside the specific path */}
          </g>
      </svg>
    )
  }
}

const BoardCell = ({
  inside, x, y, onClick, isSelected
}: ICellProps) => {
  const displayPiece = (piece: Piece, player: Player) => (
    // TODO: get pictures for pieces, render
    // TODO: map color instead of using inside.player directly
    <span style={{ color: player }}>
      {piece == 'pawn' ? <theme.Piece player={player} piece={piece}></theme.Piece> :
      (piece == 'knight' ? 'n' : piece[0]).toUpperCase()}
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
