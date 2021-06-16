import pygame
import random

#This class creates instances of a dice image for squares that are labelled as "reroll" for the game
class rerollLabel(pygame.sprite.Sprite):


	#dice image that will be displayed on a square labelled as "reroll" in the csv file
	reroll=pygame.image.load("dice_img.png")

	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = rerollLabel.reroll
		self.image =pygame.Surface((50,50))
		self.image.fill((0,0,0))
		self.rect =self.image.get_rect()
		self.shiftx, self.shifty = self.image.get_size()
		self.shiftx, self.shifty = self.shiftx / 2 , self.shifty / 2
		#center the image properly
		self.initx = int(x) - self.shiftx
		self.inity = int(y) - self.shifty
		self.rect.center = (self.initx,self.inity)
		
	#updates the reroll dice image
	def update(self):
		self.image = rerollLabel.reroll
