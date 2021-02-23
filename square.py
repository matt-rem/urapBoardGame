


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
	
	'''wanted to add methods for snakes and ladders if the square is either the bottom of a ladder or the start of a snake, we can set
	the position of the square the player will eventually land on. 
	
	def set_successor(self, s):
		self.successor.x = s.x
		self.successor.y = s.y
	
	'''
	
	
