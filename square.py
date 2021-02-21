


class Square:

	players = []
	goal = False

	def __init__(self, x, y):
		self.position = x,y

	def addPlayer(self, player):
		self.players.append(player)
		return

	def removePlayer(self, player):
		self.players.remove(player)
		return

	def getPlayers(self):
		return players
