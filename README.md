# URAP Hygiene Heroes Board Game Engine 

UrapBoardGame is a Javascript engine for creating board games. Through the website, users can upload board game image files (in .png or .jpg format) to create and customize their own board game.

# FOR ENGINE DEVELOPERS:

## Installation

Prerequisites: <a href="https://www.python.org/downloads/">Python3</a>, Python-Flask, and the latest version of any modern browser (preferably <a href="https://www.google.com/chrome/">Google Chrome</a>)

To install Python-Flask, open the Terminal application on your computer and copy paste the following:

```
pip3 install Flask
```

To set up the project, press the green "code" button at the top right of this page, select 'Download Zip'.

Drag the zip folder onto your Desktop and unzip the folder, the folder should be called "urapBoardGame-main".

Open the Terminal application on your computer.

Check your current directory by typing 

For the next step, open Terminal/Command Prompt on your computer. 

Check your current directory by typing:

```
pwd
```
and pressing enter.

Based on what is displayed after typing the above, changing directories will be necessary to get inside the urapBoardGame-main folder.

Enter this into your terminal and press enter:

```
cd desktop/urapBoardGame-main
```

Now you should be in the correct folder for debugging and hosting the website.

### Hosting the Website

To host the website on your local computer, type the following command in your terminal (make sure you're in the urapBoardGame-main folder first!):

```
python application.py
```
If that doesn't work, try

```
python3 application.py
```

The terminal should now show something similar to:

```
* Serving Flask app "application" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 217-776-073
```

Copy the link (in this case http://127.0.0.1:5000/) into your browser.

Follow this <a href="https://drive.google.com/file/d/1gayOkys_UK9tRImTNYTV2d4S6szS_aEY/view?usp=sharing">tutorial</a> to make your first board game

### File Structure

The engine uses Python and Flask for the backend, to dynamically create webpages with the assets required for specific board games. This code is found in application.py.

For storing data, the code uses sqLite and an SQL database. The data for each board game and for uploaded assets are stored in database.db, while the code that deals with updating the database is all in application.py. If there are any questions, there are comments in the code to explain their function. 

The majority of the code lies in the frontend, which uses primarily JavaScript and PIXI.JS for the board game functionality and rendering images. It also uses Jinja templates to work with Flask for dymanically creating webpages. This code can be found in the HTML files located in the templates folder, and there are tutorials and references in the Notes.txt file. 

Assets are stored in the static folder. Board images can be found in statics/assets/board_images, dice images are in statics/assets/dice_sides, and other game pieces (such as players) are in statics/assets/game_pieces.

### Core Workflow/Loop

1. The user requests a page
2. Application.py takes the page request URL to call the requested function
3. Application.py requests data from the Database for paths and information on necessary assets to produce webpage required for the user.
4. Application.py passes data from database and required assets to create an HTML page through Flask, using one of the templates in the templates folder.
5. Jinja uses template to fit information and assets that were passed in, adding the images and data that Flask provided to the webpage.
6. Webpage is served to the user. PIXI.JS and JavaScript handles everything from now on - for uploading images to the webpage, playing the board game, rendering images, etc.
7. If the user presses on a new page without uploading something, return to 1. If the user uploaded something, pass that information to one of the upload functions in the backend Python code, which adds the asset to the folder as well as its name and relevant information to the databse before returning to 

# FOR BOARD GAMES DESIGNERS:

1. Follow installation instructions above to start up the engine and run the game
2. Follow the website instructions and this <a href="https://drive.google.com/file/d/1gayOkys_UK9tRImTNYTV2d4S6szS_aEY/view?usp=sharing">tutorial</a> to create your board game

# FOR PLAYTESTERS:
1. Follow installation instructions above to start up the engine and run the game
2. On the home page, click on one of the already created games to play the game.
3. Press spacebar to roll dice. Take turns with others (or test by yourself) through Hot Seating the same computer.