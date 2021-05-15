import square as sq
import player as pl
import gameboard as g 
import sys

#takes 2 arguments - the board game file, and true/false depending on if you need an exact roll to win the game
test = g.Gameboard(open(sys.argv[1],"r"), 0)
test.play('lets begin')
