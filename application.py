# --------------------------------------------------------------
# Backend for hosting website and processing requests, data, and 
# create/send HTML pages with custom board game configurations
# --------------------------------------------------------------
from datetime import datetime
import json
import os
import sqlite3
from flask import Flask
from flask import Flask, flash, request, redirect, url_for, render_template, session, send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename
import re
from flask import send_file
from zipfile import ZipFile
from io import BytesIO
import os, glob
import shutil

# Paths to each folder for storing board game element images and data
UPLOAD_FOLDER_BOARD = 'static/assets/board_images'
UPLOAD_FOLDER_GAME = 'static/assets/game_pieces'
UPLOAD_FOLDER_DICE = 'static/assets/dice_sides'
DATABASE_PATH = 'database.db'

# Configuring which folders images should be saved into
app = Flask(__name__)
app.config['UPLOAD_FOLDER_BOARD'] = UPLOAD_FOLDER_BOARD
app.config['UPLOAD_FOLDER_GAME'] = UPLOAD_FOLDER_GAME
app.config['UPLOAD_FOLDER_DICE'] = UPLOAD_FOLDER_DICE

# Configurations for flask app and user session
app.config['SECRET_KEY'] = "secret"  # FIXME: Should be a hash of current time, so each user's key is different
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    """
    Creates the page for the home page. 
    """
    db = sqlite3.connect(DATABASE_PATH)

    # Take every stored board image path in database and concatenate with board image folder path to get relative path to each board game image
    # List of relative paths is then use by flask templating engine to create scrolling series of existing board images that user can choose.
    finished_games = list(db.execute('''SELECT * FROM saved_games'''))
    saved_games_dict = {}
    for i in range(len(finished_games)):
        game = {}
        game["index"] = finished_games[i][0]
        game["title"] = finished_games[i][1]
        game["creator"] = finished_games[i][2]
        game["board_path"] = finished_games[i][3]
        saved_games_dict[i] = game
    db.close()

    return render_template('home.html', saved_game_data=saved_games_dict)


@app.route("/setup_play", methods=['POST'])
def setup_play():
    if request.method == 'POST':
        index = request.form.get("index")
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM saved_games WHERE id=?""", (index,))
        row = cursor.fetchone()
        session["title"] = row[1]
        session["creator"] = row[2]
        session["board_path"] = row[3]
        session["square_coordinates"] = json.loads(row[4])
        session["game_pieces"] = json.loads(row[5])
        session["dice_sides"] = json.loads(row[6])
    return redirect("/play")

@app.route("/board_select")
def board_select():
    """
    Creates the page for the board upload phase. 
    """
    db = sqlite3.connect(DATABASE_PATH)

    # Take every stored board image path in database and concatenate with board image folder path to get relative path to each board game image
    # List of relative paths is then use by flask templating engine to create scrolling series of existing board images that user can choose.
    board_image_paths = [(app.config['UPLOAD_FOLDER_BOARD'] + "/" + a[0])
                         for a in list(db.execute('''SELECT file_name FROM boards'''))]
    db.close()

    return render_template('board_select.html', boards=board_image_paths)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_board():
    '''
    Handles board upload requests from user.
    Saves uploaded board to folder, adds name into database, and returns board setup phase page.
    '''
    if request.method == 'POST':
        if 'file' not in request.files:  # Check if user request actually contains a file
            flash('No file part')
            return redirect("/")
        file = request.files['file']
        name = str(hash(datetime.now()))
        if file:
            # Attempts to upload image and path to folder and backend, respectively. If error occurs, abort.
            if not save_file(file, app.config['UPLOAD_FOLDER_BOARD'], "file_name", "boards", name):                          
                return redirect("/error")
            
            # Save currently uploaded board to user session so they can start using it immediately for board setup phase
            session['board_path'] = (app.config['UPLOAD_FOLDER_BOARD'] + "/" + name) 
            return redirect("/setup_board")

@app.route('/select_image', methods=['GET', 'POST'])
def select_board():
    '''
    Handles requests from user to use a pre-uploaded board rather than upload their own.
    Takes the path of the image they chose, assigns it to the session's board image, and returns board setup phase.
    '''
    if request.method == "POST":
        session['board_path'] = request.form.get('selected-board')
        return redirect("/setup_board")

@app.route('/piece_uploader', methods=['GET', 'POST'])
def upload_pieces():
    '''
    Handles game piece and dice side uploads from users.
    Functions similarly to a combination of select_board and upload_board, except it has to handle an arbitrary number of images 
    that can be a game piece or a dice side AND there may be a combination of uploaded images and selected pre-uploaded images. 
    The logic is split into 2 parts: first, handle all requests to use pre-uploaded images (which are stored simply as key-value pairs
    where the key is either "diceN" or "playerN" where N is the dice side or player number). Depending on if it's a dice key or a player key,
    the string is added to the list of gamepieces or dice sides in the user's session (so that the board game can use it later)
    Second, it handles all requests to upload new game pieces or dice sides. Using the same key-value pair logic from above, it 
    first uploads the images themselves to the hosting server's respective folders, adds the names to the database, and lastly adds the 
    image paths to the user's sessions (exact same way as above) for use in the final board game later.
    '''
    if request.method == 'POST':
        # Initialize game_pieces and dice_size sessions as empty lists so we can add multiple paths inside for each piece
        session['game_pieces'] = {}
        session['dice_sides'] = {}
        for key in request.form:
            # Request.form contains a list of paths to existing game pieces and dice pieces that the user selected in the Upload
            # Game Elements phase. No need to upload or modify these - just use directly for the final board game.
            src_value = request.form[key]
            key_int = re.sub("[^0-9]", "", key)
            # Add selected image path to either gamepiece or dicesides user session list (depending on what it is) for final board game 
            # to reference and use.
            if "player" in key:
                session["game_pieces"].update({key_int: src_value})
            else:
                session["dice_sides"].update({key_int: src_value})
        for key in request.files:
            # Upload every board piece image in the request to the database and folder. 
            file = request.files[key]
            key_int = re.sub("[^0-9]", "", key)
            name = str(hash(datetime.now()))

            if "player" in key:  # It's a player piece image, upload to player piece folder and database
                folder_key = "UPLOAD_FOLDER_GAME"
                session_key = "game_pieces"
                sql_table = "game_pieces"
            else:  # It's a gamepiece image, upload to gamepiece folder and database
                folder_key = "UPLOAD_FOLDER_DICE"
                session_key = "dice_sides"
                sql_table = "dice_sides"
            
            success = save_file(file, app.config[folder_key], "file_name", sql_table, name)
            if not success:
                    return redirect("/error")
            
            # Add this image path to the respective user session list so that the final board game can reference and use it.
            session[session_key].update({key_int: app.config[folder_key] + "/" + name})
    return redirect("/game")

def save_file(file, folder, sql_column, sql_table, name):
    '''
    Uploads the file object to folder, and adds the name of that file to the specific sql column in the sql table.
    Returns a boolean signifying if it was successful (False = failed, True = success)
    '''
    if file.filename == '':
        return False
    file.save(os.path.join(folder, name))
    db = sqlite3.connect(DATABASE_PATH)
    board_image_paths = [a[0] for a in list(db.execute('SELECT ('+sql_column+') FROM ('+sql_table+')'))]
    if name in board_image_paths:  # FIXME: Duplicate images should be warned about before user actually uploads.
        flash("already exists!")
        return False
    db.execute('INSERT INTO '+sql_table+' ('+sql_column+') VALUES (?)', (name,))
    db.commit()
    db.close()
    return True

@app.route("/setup_board", methods=['GET', 'POST'])
def board_setup():
    '''
    Returns the board setup HTML page. Uses the board image in the user's session as the board to set up.
    '''
    return render_template('board_setup.html', board=session.get('board_path', None))

@app.route("/setup_finish", methods=['POST'])
def setup_finished():
    '''
    Handles user's uploaded data after the setup phase. Uploads the coordinates of each square (as defined by the user)
    of the currently selected board into the session and the TODO: database as well.
    '''
    squares_dict = {}
    if request.method == 'POST':
        data=json.loads(request.form.get(("json")))
        print(data)
        for i in range(0, len(data.keys())):
            square = {}
            square["x"] = data[str(i)]["x"]
            square["y"] = data[str(i)]["y"]
            square["type"] = data[str(i)]["type"]
            squares_dict[str(i)] = square
        session['square_coordinates'] = squares_dict

        return redirect("/gamepiece")

@app.route("/gamepiece", methods=['GET', 'POST'])
def gamepiece_upload():
    '''
    Creates the webpage for the Upload Game Elements page
    Takes all names of pre-uploaded game peices and dice sides in the database and passes it into the Flask template so Jinja can create a list of
    pre-uploaded images in the bottom of the page. The user is then able to drag these images into the upload section to use pre-uploaded 
    images rather than having to re-upload or constantly use new images.
    '''
    db = sqlite3.connect(DATABASE_PATH)
    dice_sides = [(app.config["UPLOAD_FOLDER_DICE"] + "/" + a[0]) for a in list(db.execute('SELECT (file_name) FROM (dice_sides)'))]
    player_pieces = [(app.config["UPLOAD_FOLDER_GAME"] + "/" + a[0]) for a in list(db.execute('SELECT (file_name) FROM (game_pieces)'))]
    db.close()
    return render_template('gamepiece_upload.html', dice_sides=dice_sides, player_pieces=player_pieces)

@app.route("/game", methods=['GET', 'POST'])
def playtest_game():
    '''
    Creates the webpage for the final, finished board game (playtest)
    Passes in all information currently stored in the user's session (that should have been filled out in previous phases either by
    uploading the user's images or selecting pre-existing images) so Jinja can integrate it into the JavaScript game engine.
    '''
    sorted_game_pieces = sorted(session["game_pieces"].items(), key=lambda x: int(x[0]))
    sorted_dice_sides = sorted(session["dice_sides"].items(), key=lambda x: int(x[0]))

    if request.method == 'GET':
        return render_template('game.html',
                                board=session.get('board_path', None), 
                                square_data=session.get('square_coordinates', None), 
                                game_pieces=[x[1] for x in sorted_game_pieces], 
                                dice_sides=[x[1] for x in sorted_dice_sides])

@app.route("/play")
def play():
    '''
    Takes the currently requested game from session (chosen from home page), creates and serves webpage with the game that 
    the user chose. 
    '''
    sorted_game_pieces = sorted(session["game_pieces"].items(), key=lambda x: int(x[0]))
    sorted_dice_sides = sorted(session["dice_sides"].items(), key=lambda x: int(x[0]))
    return render_template("play.html",
                                title=session.get('title', None),
                                creator=session.get('creator', None),
                                board=session.get('board_path', None), 
                                square_data=session.get('square_coordinates', None), 
                                game_pieces=[x[1] for x in sorted_game_pieces], 
                                dice_sides=[x[1] for x in sorted_dice_sides])


@app.route("/download")
def download():
   path = "static/assets/dice_sides/dice_1.png"
   return send_file(path, as_attachment=True)

@app.route("/download_folders", methods=['GET'])
def download_folders():
    current_path  = os.getcwd() 
    destination_path = 'destination'

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    if os.path.exists('downloads.zip'):
        shutil.rmtree('downloads.zip')

    # Recursively copy all files from the source to the destination
    for root, dirs, files in os.walk(current_path):
        # Create corresponding subdirectories in the destination
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            dest_dir = source_dir.replace(current_path, destination_path)
            os.makedirs(dest_dir, exist_ok=True)
    
        # Copy all files from the source to the destination
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = source_file.replace(current_path, destination_path)
            shutil.copy(source_file, dest_file)
    
    # Compress the output folder into a zip file
    shutil.make_archive(destination_path, 'zip', destination_path)

    return send_from_directory(directory=destination_path, filename='destination.zip', as_attachment=True)

@app.route("/save", methods=['POST'])
def save_game():
    '''
    Finishes the game creation process by saving all information in session to the database, creating a new entry
    that other users can then select and play from the home page. 
    '''
    game_title = request.form.get("gameTitle")
    name = request.form.get("name")
    board_path = session.get('board_path', None)
    square_data = json.dumps(session.get('square_coordinates', None))
    game_pieces = json.dumps(session.get("game_pieces", None))
    dice_sides = json.dumps(session.get("dice_sides", None))
    print((game_title, name, board_path, square_data, game_pieces, dice_sides))
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('''INSERT INTO saved_games (title, creator, board_path, square_data, game_piece_paths, dice_side_paths) 
                VALUES (?, ?, ?, ?, ?, ?)''', 
                (game_title, name, board_path, square_data, game_pieces, dice_sides))
    db.commit()
    db.close()
    print("hmm")
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()