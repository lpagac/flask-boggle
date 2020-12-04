from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.route('/api/score-word', methods=['POST'])
def check_word():
    response = request.get_json()
    word = response['word']
    game_id = response["gameId"]

    is_in_word_list = games[game_id].is_word_in_word_list(word)
    is_word_on_board = games[game_id].check_word_on_board(word)

    if (is_in_word_list and is_word_on_board):
        result = "ok"
    else:
        # If the word is on the board, then it must not be a word.
        result = "not-word" if is_word_on_board else "not-on-board"

    return jsonify({"result": result})