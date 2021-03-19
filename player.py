import pygame

class Player(pygame.sprite.Sprite):
        green = pygame.image.load("green_piece.png")
        blue  = pygame.image.load("blue_piece.png")
        orange = pygame.image.load("orange_piece.png")
        red  = pygame.image.load("red_piece.png")
        all_players = [green, blue, orange, red]
        def __init__(self, string, playnum, x , y):
                pygame.sprite.Sprite.__init__(self)
                self.player_name = string
                self.square = None
                self.playnum = playnum
                self.image = Player.all_players[int(playnum)]
                self.image = pygame.Surface((8,8))
                #self.image.fill((0,0,0))
                self.rect = self.image.get_rect()
                self.initx = x
                self.inity = y
                
                self.rect.center = (x,y)



                #make sure none of the players at the beginning of game are winners
                #self.is_winner = false
        def getName(self):
                return self.player_name
        def getSquare(self):
                return self.square
        def setSquare(self, sq):
                self.square = sq
                return
        def onRoll(self,x,y):
                self.initx = x
                self.inity = y
                #added
                self.rect.center = (self.initx, self.inity)

        def update(self):
                self.image = Player.all_players[int(self.playnum)]
                self.rect.x = self.initx
                self.rect.y = self.inity

