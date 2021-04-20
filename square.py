


class Square:

	goal = False
	special = None
	misc1 = None
	misc2 = None
	nextSquare = None
	number = None

	#added
	occupied = False

	def __init__(self, x, y, number):
		self.position = x, y
		self.number = int(number)

	def getCoords(self):
		return self.position
	
	def getNextSquare(self):
		return self.nextSquare
		
	def getNumber(self):
		return self.number

	def setNumber(self, n):
		self.number = n


	def hasNextSquare(self):
		return nextSquare == True
	#Resolves special rules like taking a ladder if you stand on one.
	def doSpecial(self):
		if self.special == "ladder":
			return self.misc1
		elif self.special == "forward":
			return self.number + self.misc1
		elif self.special == "back":
			return self.number - self.misc1
		elif self.special == "skip":
			return "skip";
		elif self.special == "reroll" or self.special == "roll again":
			return "reroll"
		else:
			return "resolved"
	'''wanted to add methods for snakes and ladders if the square is either the bottom of a ladder or the start of a snake, we can set
	the position of the square the player will eventually land on. 
	
	def set_successor(self, s):
		self.successor.x = s.x
		self.successor.y = s.y
	
	'''
	
	
