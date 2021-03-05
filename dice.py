import pygame
import random

class dice(pygame.sprite.Sprite):
	"""roll a dice,default image is die with face of 1"""
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
		self.rect.center = ( int(x), int(y))
		
	def update(self):

		self.image = dice.all_dice[int(self.dice_num)]
                
	def roll(self):
		self.dice_num = random.randint(1,6)
		return self.dice_num
    
