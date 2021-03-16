# urapBoardGame

This project is a board game engine. Users can use this project to customize their own board game with their own board game image file.

### Marking The Squares

To start labelling the squares to create the main path for the board game, open Terminal and run:
```
python3 mark_squares.py [your board game image file name here]
```
This will open up the board game image in another window.

The Terminal will prompt the user to enter the name of the game and the number of players who will be playing.

Using your mouse, number the squares in the board game by left-clicking on the center of each square. Start from the "start" square and end at the "finish" square in the board game. By left-clicking the center of each square, the coordinates of each square will be saved.

After the user left-clicks on the finish square, they must left-click on the board in order to add where the dice for the game will go (the last lieft-click will determine the position of the dice).

If the user has a snakes-and-ladders style board game, the user will right-click on the board game. 

The Terminal will then prompt the user to enter in the number of the square that is the first square, or "bottom" of a ladder path (meaning when a player lands on this "bottom" square, they can use the ladder to ascend to another square).

After typing in the number, the user will be prompted to enter in the second square, or "top" of the ladder (the square that the ladder takes the player to).

The same process is done for the snake paths in the game.

The user can then press any key to exit this window.

### Starting The Game

To start the game after marking the squares, open Terminal and run:
```
python3 main.py [your board game image file name here]
```
The user's board game should open up in another window, with the player images on the start square and the dice in the position that the user determined earlier.

This is a pass and play style game. To roll the dice and move their token, the player whose turn it is presses the space bar.

The game ends once a player lands on the finish square. The window with the game will close and the winner will be printed in the Terminal.





