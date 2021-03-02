import square as sq
import player as pl
import numpy as np
import itertools as it
from numpy import genfromtxt


import csv
#import position as pos


class Gameboard:

	gameName = ""
	players = []
	playerCount = None
	curentPlayersTurn = 0 #FOR NOW

	allSquares = []
	duplicateSquares = []

	winningSquare = None
	startSquare = None

	gameOver = False

	def __init__(self, file):
		self.board = file
		self.setUp()

	def setUp(self):
		'''
		data = genfromtxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', delimiter=',')
		data = np.nan_to_num(data) 
		data = np.round(data).astype(int)
		data = np.savetxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', data, fmt="%s")
		'''
		datafile = open('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', 'r')
		data = list(csv.reader(datafile))
		self.gameName = data[1][0]
		self.playerCount = int(data[1][1])
		for i in range(1, len(data)):
			
			square = sq.Square(data[i][2], data[i][3])
			for j in range(len(self.duplicateSquares)):
				if self.duplicateSquares[j] == square:
					square = self.duplicateSquares.pop(j)
					break

			if data[i][4]:
				if data[i][4] == "start":
					self.startSquare = square
				elif data[i][4] == "finish":
					self.winningSquare = square
				square.special = data[i][4]
			self.allSquares.append(square)

			if data[i][5]:
				nextSquare = sq.Square(data[i][5], data[i][6])
				square.nextSquare = nextSquare
				self.duplicateSquares.append(nextSquare)
		for i in range(self.playerCount):
			name = "test" #PROMPT TO ENTER NAME!!!!!!!!!!!!!!!!!!!
			p = pl.Player(name)
			p.setSquare(self.startSquare)
			self.players.append(p)

		self.curentPlayersTurn = it.cycle(self.players)


	def getWinningSquare(self):
		return winningSquare

	def getStartSquare(self):
		return startSquare

	def getPlayerTurn(self):
		return next(self.curentPlayersTurn)

	def wonGame(self, player):
		return player.getSquare() == self.winningSquare

	def endGame(self, player):
		print("Congrats " + player + ", you have won the game!")
		self.gameOver = True

		return #TERMINATE THE GAME!
	def move(self, player, distance):
		
		while not self.gameOver and distance > 1:
			currentSq = player.getSquare()
			if currentSq.hasNextSquare():
				player.setSquare(currentSq.getNextSquare())
				distance -= 1
				if self.wonGame(player):
					self.endGame(player)

			else:
				print("Uh oh, dead end? Something is wrong.")

		return 

	def takeTurn():
		while not self.gameOver:
			player = self.getPlayerTurn()
			roll = 1 #PROMPT A ROLL!!!!!!!!!!!!!!!!!!! int(Math.random)*6 + 1 would make it play itself
			self.move(player, roll)

		return

	'''
	Helps Debug. Prints a 2D array nicely
	'''
	def printTable(self, arr):
		'''
		data = genfromtxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', delimiter=',')
		data = np.nan_to_num(data) 
		data = np.round(data).astype(int)
		data = np.savetxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', data, fmt="%s")
		'''
		for i in arr:
			print(i)
			print()
		return
