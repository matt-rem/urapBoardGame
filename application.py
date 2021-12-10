import os
import sqlite3
from flask import Flask
from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/assets/board_images'
UPLOAD_FOLDER_GAME = 'static/assets/game_pieces'
UPLOAD_FOLDER_DICE = 'static/assets/dice_sides'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_GAME'] = UPLOAD_FOLDER_GAME
app.config['UPLOAD_FOLDER_DICE'] = UPLOAD_FOLDER_DICE
app.config['SECRET_KEY'] = "secret"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    con = sqlite3.connect('database.db')
    board_image_paths = [os.path.join(app.config['UPLOAD_FOLDER'], a[0])
                         for a in list(con.execute('''SELECT file_name FROM boards'''))]
    return render_template('home.html', boards=board_image_paths)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/")
        file = request.files['file']
        if file:
            if not save_file(file, app.config['UPLOAD_FOLDER'], "file_name", "boards"):
                return redirect("/error")
            session['board_path'] = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            return redirect("/setup_board")

@app.route('/piece_uploader', methods=['GET', 'POST'])
def upload_pieces():
    if request.method == 'POST':
        session['game_pieces'] = []
        session['dice_sides'] = []
        for key in request.form:
            src = request.form[key]
            if "player" in key:
                session["game_pieces"].append(src)
            else:
                session["dice_sides"].append(src)
        for key in request.files:
            file = request.files[key]
            if "player" in key:
                folder_key = "UPLOAD_FOLDER_GAME"
                session_key = "game_pieces"
                sql_table = "game_pieces"
            else:
                folder_key = "UPLOAD_FOLDER_DICE"
                session_key = "dice_sides"
                sql_table = "dice_sides"
            
            success = save_file(file, app.config[folder_key], "file_name", sql_table)
            if not success:
                    return redirect("/error")

            session[session_key].append(os.path.join(app.config[folder_key], secure_filename(file.filename)))
        return redirect("/game")

def save_file(file, folder, sql_column, sql_table):
    if file.filename == '':
        return False
    name = secure_filename(file.filename)
    file.save(os.path.join(folder, name))
    db = sqlite3.connect('database.db')
    board_image_paths = [a[0] for a in list(db.execute('SELECT ('+sql_column+') FROM ('+sql_table+')'))]
    print(board_image_paths)
    if name in board_image_paths:
        flash("already exists!")
        return False
    db.execute('INSERT INTO '+sql_table+' ('+sql_column+') VALUES (?)', (name,))
    db.commit()
    db.close()
    return True


@app.route('/select_image', methods=['GET', 'POST'])
def select_board():
    if request.method == "POST":
        session['board_path'] = request.form.get('selected-board')
        return redirect("/setup_board")

@app.route("/setup_board", methods=['GET', 'POST'])
def board_setup():
    return render_template('board_setup.html', board=session.get('board_path', None))

@app.route("/setup_finish", methods=['POST'])
def setup_finished():
    if request.method == 'POST':
        squares_length = int(request.form.get("maxSquareNumber"))
        square_coordinates_dict = {}
        for i in range(squares_length):
            coordinate_string = request.form.get(str(i))
            coordinates = coordinate_string.split(" ")
            square_coordinates_dict[str(i)] = (float(coordinates[0]), float(coordinates[1]))
        session['square_coordinates'] = square_coordinates_dict
        return redirect("/gamepiece")

@app.route("/gamepiece", methods=['GET', 'POST'])
def gamepiece_upload():
    db = sqlite3.connect('database.db')
    dice_sides = [os.path.join(app.config["UPLOAD_FOLDER_DICE"], a[0]) for a in list(db.execute('SELECT (file_name) FROM (dice_sides)'))]
    player_pieces = [os.path.join(app.config["UPLOAD_FOLDER_GAME"], a[0]) for a in list(db.execute('SELECT (file_name) FROM (game_pieces)'))]
    db.close()
    return render_template('gamepiece_upload.html', dice_sides=dice_sides, player_pieces=player_pieces)

@app.route("/game", methods=['GET', 'POST'])
def play_game():
    if request.method == 'GET':
        return render_template('game.html', board=session.get('board_path', None), 
                                coordinates=session.get('square_coordinates', None), 
                                game_pieces=session["game_pieces"], 
                                dice_sides=session["dice_sides"])

@app.route("/test", methods=['GET', 'POST'])
def test_website():
    return render_template('PixiJStest.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
