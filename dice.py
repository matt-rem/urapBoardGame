import pygame
import random

NUM_ROLL_TIMES = 15

class dice(pygame.sprite.Sprite):
	#roll a dice,default image is die with face of 1

	
	
	dice1=pygame.image.load("Dice1.png")
	dice2=pygame.image.load("Dice2.png")
	dice3=pygame.image.load("Dice3.png")
	dice4=pygame.image.load("Dice4.png")
	dice5=pygame.image.load("Dice5.png")
	dice6=pygame.image.load("Dice6.png")
	all_dice = [ None, dice1, dice2, dice3, dice4, dice5, dice6 ]

	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = dice.all_dice[1]
		self.image =pygame.Surface((50,50))
		self.image.fill((0,0,0))
		self.dice_num = 1
		self.rect =self.image.get_rect()

		self.shiftx, self.shifty = self.image.get_size()
		self.shiftx, self.shifty = self.shiftx / 2 , self.shifty / 2
		self.initx = int(x) - self.shiftx
		self.inity = int(y) - self.shifty

		self.num_rolls = 0


		self.rect.center = ( int(x), int(y))
		
	def update(self):

		self.image = dice.all_dice[int(self.dice_num)]
                
	def roll(self):
		self.dice_num = random.randint(1,6)
		return self.dice_num

	def getNumRolls(self):
		return self.num_rolls

	def setNumRolls(self, num):
		self.num_rolls = num

	def decrement(self):
		self.num_rolls -= 1

	def reset(self):
		self.num_rolls = 0


    
