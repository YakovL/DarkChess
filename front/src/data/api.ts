import { Player, CellContent } from './model'
import config from '../config'


export const requestNewGame = async () => {
}

export const requestJoinSecret = async (whiteSecret: string) => {
}

export const requestJoinGame = async (joinSecret: string) => {
}

export const requestGameState = async (playerSecret: string) => {
}

export const requestMove = async (playerSecret: string, from: { x: number, y: number }, to: { x: number, y: number }) => {
}
