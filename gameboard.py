import square as sq
import player as pl
import numpy as np
import dice as d
import itertools as it
#import GUI
#from PIL import Image
import math
import pygame #used for GUI

from numpy import genfromtxt

import csv
#import position as pos


class Gameboard:

	gameName = ""
	players = []

	playerCount = None
	currentPlayersTurn = 0 #FOR NOW

	allSquares = []
	duplicateSquares = [] # Used in setup to prevent duplicate squares

	winningSquare = None
	startSquare = None
	dicePosX = 0
	dicePosY = 0
	gameOver = False

	def __init__(self, file, list_names):
		self.board = file #IMG file for board
		self.list_names = list_names.split(",")
		self.list_names = sorted(self.list_names)
		print(self.list_names)
		self.setUp() #Sets up all Squares and players and puts players to starting squares.


	def setUp(self):#Sets up all Squares and players and puts players to starting squares.
		'''
		data = genfromtxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', delimiter=',')
		data = np.nan_to_num(data) 
		data = np.round(data).astype(int)
		data = np.savetxt('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', data, fmt="%s")
		'''
		#datafile = open('Sample CSV File Template for BoardGameGenerator - Sheet1.csv', 'r') #Opens the csv file w/info
		with open('sample.csv', newline='') as csvfile:
                        data = list(csv.reader(csvfile))
		
		self.gameName = data[1][0]
		#print(self.gameName)
		#self.printTable(data)
		self.playerCount = int(data[1][1])
		#print(self.playerCount)
		#ignore last row
		self.allSquares.append(None)
		for i in range(2, len(data)): #Adds all the squares to allSquares, sets .nextquare, .special, and the x and y cooridantes properly. Also sets winningSquare and startSquare.

			
			square = sq.Square(data[i][2], data[i][3], data[i][4])
			# if there are duplicates squares maybe a square is missing and an exception should be thrown? 
			'''for j in range(len(self.duplicateSquares)):
				if self.duplicateSquares[j] == square:
					square = self.duplicateSquares.pop(j)
					break
                        '''
			if data[i][6]:
				if data[i][6] == "start":
					self.startSquare = square
				elif data[i][6] == "finish":
					self.winningSquare = square
				elif data[i][6] == "ladder":
					square.misc1 = int(data[i][7])
				square.special = data[i][6]
			self.allSquares.append(square)

			#Below is messed up but unused so whatever.
			if data[i][5]:
				nextSquare = sq.Square(data[i][5], data[i][6], data[i][5])
				square.nextSquare = nextSquare
				self.duplicateSquares.append(nextSquare)
		'''a = len(data) -1		
		global dicePosX
		dicePosX = data[int(a)][2]
		global dicePosY
		dicePosY = data[int(a)][3]
		print(dicePosX)
		print(dicePosY)'''
                                
		#for i in range(self.playerCount): #Names each player and sets their square to the first square
		#	name = "test" #PROMPT TO ENTER NAME!!!!!!!!!!!!!!!!!!!
		#	p = pl.Player(name,i, 3 , 3)
		#	p.setSquare(self.startSquare)
		#	self.players.append(p)

		#self.curentPlayersTurn = it.cycle(self.players)
                



	def getWinningSquare(self):
		return self.winningSquare

	def getStartSquare(self):
		return self.startSquare

	def getPlayerTurn(self, arr):
		return next(arr)

	def wonGame(self, player, roll):
		return player.getSquare().getNumber() + roll >= self.winningSquare.getNumber()

	def endGame(self, player):
		print("! ! !")
		print("Congrats Player " + player.getName() + ", you have won the game!")
		print("! ! !")
		self.gameOver = True
		quit()

		return #TERMINATE THE GAME!
	#Actually takes the turn for the player. 
	def takeTurn(self, player, distance):
		
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

	def moveToSquare(self, player, roll):
		return Gameboard.allSquares[player.getSquare().getNumber() + roll]

	#Checks if the game has been won and if not allows a player to take his or her turn.
	def play(self,str):
		#print(str)
		pygame.init() #initialize pygame
		pygame.display.set_caption(self.gameName)
	
		background = pygame.image.load(self.board)
		#get the width of the board
		background_x = background.get_size()[0]
		#get the height of the board
		background_y = background.get_size()[1]
		#screen size will be the size of the board
		screen = pygame.display.set_mode((background_x,background_y))
		#get dice coordinates
		y = Gameboard.allSquares[len(Gameboard.allSquares)-1].getCoords()
		#get start coordinates
		z = Gameboard.allSquares[1].getCoords()
		
		running =True
		all_sprites = pygame.sprite.Group()
		mydice = d.dice(y[0],y[1])


		for i in range(len(self.list_names)):
			pl_num = i
			pl_name = "test {num}".format(num=pl_num)
			if i == 0:
				self.players.append(pl.Player(self.list_names[i], i, int(z[0]), int(z[0])))
			elif i == 1:
				self.players.append(pl.Player(self.list_names[i], i, int(z[0]), int(z[0]) + 30))
			elif i == 2:
				self.players.append(pl.Player(self.list_names[i], i, int(z[0]) - 40, int(z[0])))
			elif i == 3:
				self.players.append(pl.Player(self.list_names[i], i, int(z[0]) - 40, int(z[0]) + 30))

			self.players[i].setSquare(self.getStartSquare())


			all_sprites.add(self.players[i])

		all_sprites.add(mydice)
		turn = 0

		winner = False
		winner_num = 0
        
		finish_sq = self.getWinningSquare()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					#roll the dice
					dice_roll = mydice.roll()
					#if a winner has not been declared yet
					if not winner:
						newxy = None
						#if the player will land on a square with a sequence number equal to or beyond the finish square
						if (self.wonGame(self.players[turn], dice_roll)):
							#set winner to true
							winner = True
							winner_num = turn
							#get the coordinates of the final square (finish square)
							newxy = self.getWinningSquare().getCoords()
						
						#if no player has reached finish square
						else:
							#set the player's square to the square they will land on
							self.players[turn].setSquare(self.moveToSquare(self.players[turn], dice_roll))                  
							#points to the square the player will move to
							newSquare = self.players[turn].getSquare()
							#Resolve any special rules
							token = self.players[turn].getSquare().doSpecial()
							if token != "resolved" and token:
								#the next square the player will move to is assigned here
								newSquare = Gameboard.allSquares[token]
								self.players[turn].setSquare(newSquare)

							#get the coordinates for the  square you need to go to
							newxy = newSquare.getCoords()
							
						#put the player on the square they will be moved to
						self.players[turn].onRoll(int(newxy[0]),int(newxy[1]))
						#change to the next player's turn
						turn = (turn + 1) % len(self.list_names)
						
			#if the winner is true, end the game
			if winner:
				self.endGame(self.players[winner_num])          
			                                  
			                
			all_sprites.update()
			                
			screen.fill((0,0,0))
			#all_sprites.draw(screen)

			screen.blit(background,(0,0))
			all_sprites.draw(screen)
			pygame.display.update()
			#player = self.getPlayerTurn()
			#roll = 1 #PROMPT A ROLL!!!!!!!!!!!!!!!!!!! int(Math.random)*6 + 1 would make it play itself
			#self.takeTurn(player, roll)

		return

	'''
	Helps Debug. Prints a 2D array nicely
	'''
	def printTable(self, arr):
		for i in arr:
			print(i)
			print()
		return