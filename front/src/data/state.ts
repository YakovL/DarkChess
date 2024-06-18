import { create } from 'zustand'
import { router } from './statePersistance'
import { Player, CellContent } from './model'

// TODO: add isWaitingForPromotion, set in setGameState, updateAfterMove
interface GameState {
  playerSecret: string | null
  playerColor: Player | null
  boardCells: CellContent[][] | null
  joinSecretToShare: string | null
  isOurTurn: boolean | null
  winner: Player | null
}

export const useGameStore = create<GameState>(() => ({
  playerSecret: null,
  playerColor: null,
  boardCells: null,
  joinSecretToShare: null,
  isOurTurn: null,
  winner: null,
}))

export const setGameState = (
  playerSecret: GameState['playerSecret'],
  playerColor: GameState['playerColor'],
  boardCells: GameState['boardCells'],
  joinSecretToShare: GameState['joinSecretToShare'],
  isOurTurn: GameState['isOurTurn'],
  winner?: GameState['winner'],
) => useGameStore.setState(() => {
  // later: try to separate into a middleware instead
  router.setValue('game', playerSecret)

  return {
    playerSecret,
    playerColor,
    boardCells,
    joinSecretToShare,
    isOurTurn,
    winner: winner || null,
  }
})

// method for resuming a game or updating the state after a move
// set and setState functions _merge_ state (not deeply, though)
export const refresh = (
  boardCells: CellContent[][],
  whosTurn: Player,
  winner: GameState['winner'],
  playerColor?: Player,
) => useGameStore.setState((state: GameState) => ({
  boardCells,
  isOurTurn: whosTurn === state.playerColor,
  winner,
  playerColor: playerColor || state.playerColor,
}))

export const useGameStoreBit = {
  PlayerSecret: () => useGameStore((state) => router.getValue('game') || state.playerSecret),
  PlayerColor: () => useGameStore((state) => state.playerColor),
  BoardCells: () => useGameStore((state) => state.boardCells),
  IsOurTurn: () => useGameStore((state) => state.isOurTurn),
  JoinSecretToShare: () => useGameStore((state) => router.getValue('join') || state.joinSecretToShare),
  Winner: () => useGameStore((state) => state.winner),
}
