


class Square:

	goal = False
	special = None
	nextSquare = None

	def __init__(self, x, y):
		self.position = x,y

	def getCoords(self):
		return self.position
	
	def getNextSquare(self):
		return self.nextSquare

	def hasNextSquare(self):
		return nextSquare == True
	'''wanted to add methods for snakes and ladders if the square is either the bottom of a ladder or the start of a snake, we can set
	the position of the square the player will eventually land on. 
	
	def set_successor(self, s):
		self.successor.x = s.x
		self.successor.y = s.y
	
	'''
	
	
