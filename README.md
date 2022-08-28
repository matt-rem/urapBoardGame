# urapBoardGame

UrapBoardGame is a Javascript engine for creating board games. Through the website, users can upload board game image files (in .png or .jpg format) to create and customize their own board game.



## Installation/Getting Started

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



## Hosting the Website

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

Copy the link (in this case http://127.0.0.1:5000/) into your browser. By default, this should show the "home.html" page located within the templates folder.

## Creating a Board Game


