# -----------------------------------------------------------
# Backend for hosting website and processing requests, data, and 
# create/send HTML pages with custom board game configurations
# -----------------------------------------------------------
from datetime import datetime
import os
import sqlite3
from flask import Flask
from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_session import Session
from werkzeug.utils import secure_filename
import re

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
    Creates the page for the home/board upload phase. 
    """
    db = sqlite3.connect(DATABASE_PATH)

    # Take every stored board image path in database and concatenate with board image folder path to get relative path to each board game image
    # List of relative paths is then use by flask templating engine to create scrolling series of existing board images that user can choose.
    board_image_paths = [(app.config['UPLOAD_FOLDER_BOARD'] + "/" + a[0])
                         for a in list(db.execute('''SELECT file_name FROM boards'''))]
    db.close()

    return render_template('home.html', boards=board_image_paths)


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
    of the currently selected board into the sesion and the TODO: database as well.
    '''
    if request.method == 'POST':
        squares_length = int(request.form.get("maxSquareNumber"))  # Get the number of squares (this is for iterating through all keys)

        # Dictionary that stores each coordinate as key-value pairs. Key is the square index, while the value is a tuple with 
        # the x coordinate in the first index, and y coordinate in the second.
        square_coordinates_dict = {} 

        for i in range(squares_length):
            # The coordinates are stored in key-value pairs where
            # Key: int index representing which square it is (0 = square 1, 1 = square 2, etc.)
            # Value: a string with both the x and y coordinate separated by space e.g. ("20 60") means x: 20 and y: 60
            coordinate_string = request.form.get(str(i))
            coordinates = coordinate_string.split(" ")
            square_coordinates_dict[str(i)] = (float(coordinates[0]), float(coordinates[1]))

        # Add the dictionary to the session so the final finished board game can use it
        session['square_coordinates'] = square_coordinates_dict

        # TODO: also add these coordinates to the database so future users don't need to set up the board again
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
def play_game():
    '''
    Creates the webpage for the final, finished board game

    Passes in all information currently stored in the user's session (that should have been filled out in previous phases either by
    uploading the user's images or selecting pre-existing images) so Jinja can integrate it into the JavaScript game engine.
    '''
    sorted_game_pieces = sorted(session["game_pieces"].items(), key=lambda x: int(x[0]))
    sorted_dice_sides = sorted(session["dice_sides"].items(), key=lambda x: int(x[0]))
    if request.method == 'GET':
        return render_template('game.html', board=session.get('board_path', None), 
                                coordinates=session.get('square_coordinates', None), 
                                game_pieces=sorted_game_pieces, 
                                dice_sides=sorted_dice_sides)

@app.route("/test", methods=['GET', 'POST'])
def test_website():
    return render_template('PixiJStest.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
