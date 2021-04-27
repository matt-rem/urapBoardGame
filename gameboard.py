import square as sq
import player as pl
import numpy as np
import dice as d
import itertools as it

import math
import pygame 
import os, subprocess, sys


from numpy import genfromtxt

from playsound import playsound
#WAV OR MP3 FILES ONLY

import csv

MIN_VALUE_NEG = -1
MIN_VALUE_ZERO = 0
NUM_ROLL_TIMES = 15
FIXED_TIME = 20

class Gameboard:

	gameName = ""
	players = []

	playerCount = None
	bots = 0
	maxPlayerCount = None
	currentPlayersTurn = 0 #FOR NOW

	allSquares = []
	duplicateSquares = [] # Used in setup to prevent duplicate squares

	winningSquare = None
	startSquare = None
	dicePosX = MIN_VALUE_ZERO
	dicePosY = MIN_VALUE_ZERO
	gameOver = False
	list_names = []

	def __init__(self, file, exact_roll):
		self.board = file #IMG file for board
		#self.list_names = list_names.split(",")
		#self.list_names = sorted(self.list_names)



		if (exact_roll == "true"):
			self.exact_roll = True
		else:
			self.exact_roll = False

		
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
		self.maxPlayerCount = int(data[1][1])
		self.playerCount = int(input("Enter the number of players: "))
		for i in range(self.playerCount):
			self.list_names.append(input("Enter the name of player " + str(i + 1) + ": "))
		self.bots = int(input("Enter the number of computers you'd like to play with: "))
		for i in range(self.bots):
			self.list_names.append("Computer Bot " + str(i + 1))

		'''if self.playerCount != len(self.list_names):
			print("number of players and the number of player names you send must be the same!")
			quit()
		elif self.playerCount not in range(2, self.maxPlayerCount):
			print("game must have between 2 to 4 players!")
			quit()
		elif len(self.list_names) not in range(2, self.maxPlayerCount):
			print("you must provide between 2 to 4 player names!")
			quit()'''
		#print(self.playerCount)
		#ignore last row


		d_count = len(range(2, len(data)))-2
		print("COUNT = ", d_count)
		self.allSquares.append(None)
		for i in range(2, len(data)): #Adds all the squares to allSquares, sets .nextquare, .special, and the x and y cooridantes properly. Also sets winningSquare and startSquare.

			
			square = sq.Square(data[i][2], data[i][3], data[i][4], d_count)
			# if there are duplicates squares maybe a square is missing and an exception should be thrown? 
			'''for j in range(len(self.duplicateSquares)):
				if self.duplicateSquares[j] == square:
					square = self.duplicateSquares.pop(j)
					break
                        '''
            #Updates special squares.
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
			d_count -= 1
			if data[i][5]:
				nextSquare = sq.Square(data[i][5], data[i][6], data[i][5], d_count)
				square.nextSquare = nextSquare
				self.duplicateSquares.append(nextSquare)



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

		#add the players to the list
		for i in range(len(self.list_names)):
			pl_num = i
			pl_name = "test {num}".format(num=pl_num)
			if i == 0:
				a = pl.Player(self.list_names[i], i, int(z[0]), int(z[1]))
				if a.getName()[0:8] == "Computer":
					a.setBot()

				self.players.append(a)
			elif i == 1:
				a = pl.Player(self.list_names[i], i, int(z[0]), int(z[1]))
				if a.getName()[0:8] == "Computer":
					a.setBot()

				self.players.append(a)
			elif i == 2:
				a = pl.Player(self.list_names[i], i, int(z[0]), int(z[1]))
				if a.getName()[0:8] == "Computer":
					a.setBot()

				self.players.append(a)
			elif i == 3:
				a = pl.Player(self.list_names[i], i, int(z[0]), int(z[1]))
				if a.getName()[0:8] == "Computer":
					a.setBot()

				self.players.append(a)

			self.players[i].setSquare(self.getStartSquare())


			all_sprites.add(self.players[i])

		all_sprites.add(mydice)
		turn = MIN_VALUE_ZERO

		winner = False
		winner_num = MIN_VALUE_ZERO

		mydice.reset()
		steps_to_move = MIN_VALUE_NEG


		while running:
			

			clockobject = pygame.time.Clock()
			clockobject.tick(FIXED_TIME)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					#Reroll Or No
					reroll = False
					#roll_times = NUM_ROLL_TIMES
					mydice.setNumRolls(15)

					
				#If the key pressed is R
				elif event.type == pygame.KEYDOWN and event.key == 114:
					with open('rules.txt') as f: 
						opener = "open" if sys.platform == "darwin" else "xdg-open"
						subprocess.call([opener, 'rules.txt'])
						for line in f:
							print(line.strip())
					

			#if roll_times has been set to 15 (if the dice has not been rolled yet)
			if mydice.getNumRolls() > 0:
					#roll the dice and save the value
					steps_to_move = mydice.roll()
					#decrease roll times
					mydice.decrement()

			#if roll times has gone down to 0 (if the dice has been rolled)
			else:
				#reset the values
				mydice.reset()

				if self.player.isBot():
					#Roll for the player. FIXME


				#if this player's turn needs to be skipped
				if self.players[turn].skipped():
					self.players[turn].skip_turn()
					turn = (turn + 1) % len(self.list_names)

				#if the player can make a valid move
				elif steps_to_move <= self.players[turn].getSquare().getDist() and steps_to_move > 0:
					#set the player's square to the very next square (this move will be repeated dice roll number of times)
					self.players[turn].setSquare(self.moveToSquare(self.players[turn], 1))
					slidexy = self.players[turn].getSquare().getCoords()

					self.players[turn].setOffset(turn)

					self.players[turn].onRoll(int(slidexy[0]) + self.players[turn].getXOffset(),int(slidexy[1]) + self.players[turn].getYOffset())

					#decrease dice_roll till the player lands on the square they need to land on
					steps_to_move -= 1

				#if you have moved to a special square/ are done moving
				elif steps_to_move == 0:
					#check to see if player has landed on special square
					token = self.players[turn].getSquare().doSpecial()
					if token != "resolved" and token:

						#player attribute skip becomes true.
						if token == "skip":
							print("skipping for player ", turn)
							self.players[turn].skip_turn()

						#we don't update the turn counter
						elif token == "reroll":
							print("rolling again for player ", turn)
							reroll = True
						else:
							print("ladder for player ", turn)
							jumpSquare = Gameboard.allSquares[token]
							self.players[turn].setSquare(jumpSquare)
							jumpxy = jumpSquare.getCoords()
							self.players[turn].setOffset(turn)
							self.players[turn].onRoll(int(jumpxy[0]) + self.players[turn].getXOffset(),int(jumpxy[1]) + self.players[turn].getYOffset())
					steps_to_move = MIN_VALUE_NEG

					#before we switch turns: check if the game is over
					if self.players[turn].getSquare() == self.getWinningSquare():
						self.endGame(self.players[turn])

					#if this player is not on a reroll square
					if not reroll:
						turn = (turn + 1) % len(self.list_names)
					#turn = (turn + 1) % len(self.list_names)

				
				#If you roll more than needed to get to the winning square, and need an exact roll
				elif steps_to_move > self.players[turn].getSquare().getDist() and steps_to_move > 0 and self.exact_roll:
					print("exact roll = ", self.exact_roll)

					steps_to_move = MIN_VALUE_NEG
					print("oops you cant move player", turn ,"!")
					turn = (turn + 1) % len(self.list_names)

				#If you roll more than needed to get to the winning square, but do not need an exact roll
				elif steps_to_move > self.players[turn].getSquare().getDist() and steps_to_move > 0 and not self.exact_roll:
					print("not exact roll")
					self.endGame(self.players[turn])


					
			#if winner:
				#self.endGame(self.players[winner_num])  

			                                  
			                
			all_sprites.update()
			                
			screen.fill((0,0,0))
			#all_sprites.draw(screen)

			screen.blit(background,(0,0))

			all_sprites.draw(screen)
			pygame.display.update()
			#player = self.getPlayerTurn()
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
