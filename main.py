import square as sq
import player as pl
import gameboard as g 
import sys

test = g.Gameboard(open(sys.argv[1], "r"))
test.play('lets begin')
