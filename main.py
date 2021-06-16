import square as sq
import player as pl
import gameboard as g 
import sys

#takes 2 arguments - the board game file, and true/false depending on if an exact roll is needed to win the game
test = g.Gameboard(open(sys.argv[1],"r"), sys.argv[2])
test.play('lets begin')
