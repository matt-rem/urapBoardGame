import pygame
import random

#This class creates instances of an "X" image for squares that are labelled as "skip" for the game
class skipLabel(pygame.sprite.Sprite):

	#"X" image that will be displayed on a square labelled as "skip" in the csv file
	skip=pygame.image.load("x_img.png")

	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = skipLabel.skip
		self.image =pygame.Surface((50,50))
		self.image.fill((0,0,0))
		self.rect =self.image.get_rect()
		self.shiftx, self.shifty = self.image.get_size()
		self.shiftx, self.shifty = self.shiftx / 2 , self.shifty / 2
		#center the image properly
		self.initx = int(x) - self.shiftx
		self.inity = int(y) - self.shifty
		self.rect.center = (self.initx,self.inity)
		
	#updates the skip "X" image
	def update(self):
		self.image = skipLabel.skip
