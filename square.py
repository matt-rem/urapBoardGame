import pygame

#This class creates square position instances that will correspond to points on the board.
#These points will create a path for the players to follow from the start square to the end
class Square:

	goal = False
	special = None
	misc1 = None
	misc2 = None
	nextSquare = None
	number = None
	sound = 0
	#the distance between this square and the finish square of the game (distance is measured by difference in sequence numbers)
	dist = -1
	occupied = False

	def __init__(self, x, y, number, d):
		self.position = x, y
		self.number = int(number)
		self.dist = d

	#returns boolean value based on whether or not the square has a sound or not
	def hasSound(self):
		return self.sound != 0
	
	#returns the sound .wav file for the square
	def getSound(self):
		return self.sound

	#returns the position of the square, in the form of (x,y)
	def getCoords(self):
		return self.position
	
	#returns the square that succeeds the current square
	def getNextSquare(self):
		return self.nextSquare
		
	#returns the sequence number of the square
	def getNumber(self):
		return self.number

	#sets the number for a square
	def setNumber(self, n):
		self.number = n


	#returns boolean value based on whether or not the square this method is called on has a succeeding square
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

	#sets the distance to the value "x" that is sent as an argument
	def setDist(self, x):
		self.dist = x
	
	
