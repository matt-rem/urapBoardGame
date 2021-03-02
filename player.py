

class Player:

	def __init__(self, string):
		self.player_name = string
		self.square = None
		#make sure none of the players at the beginning of game are winners
		#self.is_winner = false
		
	def getName(self):
		return self.player_name

	def getSquare(self):
		return self.square

	def setSquare(self, sq):
		self.square = sq
		return 
	