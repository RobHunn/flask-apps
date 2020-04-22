from flask import Flask, render_template, request, redirect, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True


boggle_board = Boggle()


@app.route('/')
def home():
    board = boggle_board.make_board()
    session['board'] = board
    return render_template('home.html', board=board)


@app.route('/answer', methods=['POST'])
def guess():
    if request.is_json:
        req = request.get_json()
        guess = req['answer']
        return jsonify({"your guess was": guess})
    else:
        return jsonify({"message": " send json fool..."})
