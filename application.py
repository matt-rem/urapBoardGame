import os
import sqlite3
from flask import Flask
from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/assets/board_images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    con = sqlite3.connect('database.db')
    board_images = ['assets/board_images/' + a[0]
                    for a in list(con.execute('''SELECT file_name FROM boards'''))]
    list_index = list(range(len(board_images)))
    print(list_index)
    return render_template('home.html', boards=board_images, image_indexes=list_index)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            db = sqlite3.connect('database.db')
            name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
            db.execute('''INSERT INTO boards (file_name) VALUES (?)''', (name,)
                       )  # current error: unique parameter failed (should return error html instead)
            db.commit()
            db.close()
            return redirect("/setup_board")


@app.route('/select_image', methods=['GET', 'POST'])
def select_board():
    if request.method == "POST":
        session['board_path'] = request.form.get('selected-board')
        return redirect("/setup_board")


@app.route("/setup_board", methods=['GET', 'POST'])
def board_setup():
    return render_template('board_setup.html', board=session.get('board_path', None))


@app.route("/gamepiece", methods=['GET', 'POST'])
def gamepiece_upload():
    return render_template('gamepiece_upload.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
