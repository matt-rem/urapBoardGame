


class Square:

	goal = False
	special = None
	misc1 = None
	misc2 = None
	nextSquare = None
	number = None

	dist = -1

	#added
	occupied = False

	def __init__(self, x, y, number, d):
		self.position = x, y
		self.number = int(number)
		self.dist = d


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
	
	#returns the distance between the player and the winning square
	def getDist(self):
		return self.dist

	def setDist(self, x):
		self.dist = x
	
	
