# urapBoardGame

This project is a board game engine in the python programming language. Users can use this project to customize their own board game with their own board game image file. The image file must be in the .png or .jpg format.

### Setting Up This Project

For this project, users will need to install Python3, the OpenCV library, and the Pygame package.

To run this project, press the green "code" button at the top of this github page. Then press the button to download the files as a zip. Drag the zip folder onto your desktop, and unzip the folder. The folder will be called "urapBoardGame-main". 

Inside the unzipped folder will be default board images, default tokens, a sound effect folder, multiple .py files that are used for the engine, and a file called sample.csv. These are all used in the creation and execution of the board game engine. Users will need to drag their preferred image file into the urapBoardGame-main folder before starting if they do not wish to use the defaults.

For the next step, open the Terminal application on your computer. 

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
Now you will be in the correct folder to move forward and start creating the board game.

### Marking The Squares
To start labelling the squares to create the main path for the board game, in the Terminal type:
```
python3 mark_squares.py [your board game image file name here]
```
In the terminal, a prompt will appear to ask the user to type in the name of their game.

After pressing "enter", the next prompt will ask for the maximum number of players that can play the game.

Hitting enter again will open up the board game image in another window.

Using your mouse or laptop touchpad, number the squares in the board game by clicking in the center of each square. Go in numerical order and start from the "start" square and end at the "finish" square in the board game and. By clicking the center of each square, the coordinates of each square will be saved.

After the user clicks on the finish square, they must click on the board in order to add where the dice for the game will go (the last click on the board will determine the position of the dice).

If the user has a snakes-and-ladders style board game, or wants to add ladder functionality to the  the user will press "l" on the board game. 

The Terminal will then prompt the user to enter in the number of the square that is the first square, or "bottom" of a ladder path (meaning when a player lands on this "bottom" square, they can use the ladder to ascend to another square).

After typing in the number, the user will be prompted to enter in the second square, or "destination" of the ladder (the square that the ladder takes the player to).

The same process is done for the snake paths in the game, but in reverse. This means after pressing "l", the first number that will be typed will be the "top" square, and the second number will be the "destination" square (at the bottom).

The user can then press "escape" to exit this window.

In the csv file, more special actions can be added. In the "misc1" column, you can type "skip" and "reroll" for certain squares. Adding "skip" means that if a player lands on a particular square, their turn gets skipped. Adding "reroll" means that if a player lands on a particular square, it is still their turn and they can roll again.

### Starting The Game

To start the game after marking the squares, open Terminal and run the line below:
```
python3 main.py [your board game image file name here] [true/false]
```
Entering false means that the game does not need to end on an exact roll. Entering true means that the game will end on an exact roll of the dice.

The terminal will prompt the user to enter the number of players who will be playing this game.

The terminal will then ask the user to enter in the names of each player.

If the user wants to play against the computer, the next line asks the user to enter in the number of bots they want for the game. If the user does not want this, they can just put 0.

The user's board game should open up in another window, with the player images on the start square and the dice in the position that the user determined earlier.

This is a pass and play style game. To roll the dice and move their token, the player whose turn it is presses the space bar.

The game ends once a player lands on the finish square. The window with the game will close and the winner will be printed in the Terminal.





