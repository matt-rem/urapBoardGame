import square as sq
import player as pl


class Gameboard:
	players = []
	indexPlayersTurn = None
	contiguousSquares = []
	winningSquare = None
	startSquare = None

	def __init__(self, file):
		self.board = file

	def setUp(self, file):
		"NEEDS IMPLEMENTATION"
		return

	def gameOver(self):
		if winningSquare.getPlayers():
			return True
		return False

	def getWinningSquare(self):
		return winningSquare

	def getStartSquare(self):
		return startSquare

	def getPlayerTurn(self):
		return players[indexPlayersTurn]

	def makeMove(self):
		"NEEDS IMPLEMENTATION"
		return 