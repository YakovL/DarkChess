from flask import Flask
from blueprints.serialization import to_json
from blueprints.game_sessions_manager import GameSessionsManager
from blueprints.storage import GameSessionsStorage

app = Flask(__name__)

session_manager = GameSessionsManager(GameSessionsStorage())

@app.post('/game/new')
def create_game():
    white_secret, board_view__white = session_manager.create_session()
    return to_json({
        'white_secret': white_secret,
        'board_view__white': board_view__white
    })

@app.get('/game/<white_secret>/join_secret')
def get_join_secret(white_secret: str):
    join_secret = session_manager.get_join_secret(white_secret)
    return {
        'join_secret': join_secret
    }

@app.post('/game/<join_secret>/join')
def join_game(join_secret: str):
    result = session_manager.join_session(join_secret)
    if result is None:
        return {
            'black_secret': None,
            'board_view__black': None
        }, 404

    black_secret, board_view__black = result
    return to_json({
        'black_secret': black_secret,
        'board_view__black': board_view__black
    })

@app.get('/game/<player_secret>/move-validity/<int:x_from>/<int:y_from>/<int:x_to>/<int:y_to>')
def is_move_valid(player_secret: str, x_from: int, y_from: int, x_to: int, y_to: int):
    session = session_manager.validate_move(player_secret, x_from, y_from, x_to, y_to)
    return {
        'valid': session is not None
    }

@app.post('/game/<player_secret>/move/<int:x_from>/<int:y_from>/<int:x_to>/<int:y_to>')
def make_move(player_secret: str, x_from: int, y_from: int, x_to: int, y_to: int):
    result = session_manager.make_move(player_secret, x_from, y_from, x_to, y_to)
    if result is None:
        #TODO: make respond more descriptive, return what get_view_and_stats returns and maybe ~move is not valid~ message
        return {
            'problem': 'invalid move or session was not found by secret'
        }

    return to_json(result)

@app.get('/game/<player_secret>/state')
def get_view_and_stats(player_secret: str):
    result = session_manager.get_player_view_and_stats(player_secret)
    if result is None:
        return {
            'problem': 'session not found by secret'
        }, 404

    return to_json(result)

#TODO: def promote(player_secret: str, x_from: int, y_from: int, x_to: int, y_to: int):

