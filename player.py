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
                self.image = pygame.Surface((50,50))
                #self.image.fill((0,0,0))
                self.rect = self.image.get_rect()
                self.skip = False


                #SHIFTS to make image in center:
                self.shiftx, self.shifty = self.image.get_size()
                self.shiftx, self.shifty = self.shiftx / 2 , self.shifty / 2
                #Piece x and y
                self.initx = x - self.shiftx
                self.inity = y - self.shifty
                
                self.rect.center = (self.initx, self.inity)

                #For currency
                self.bal = 0



                #make sure none of the players at the beginning of game are winners
                #self.is_winner = false
        def getName(self):
                return self.player_name
        def getBal(self):
                return self.bal
        def getSquare(self):
                return self.square
        def setSquare(self, sq):
                self.square = sq
                return
        def skip(self):
                self.skip = not self.skip
        def skipped(self):
                return self.skip
        def onRoll(self,x,y):
                self.initx = x - self.shiftx
                self.inity = y - self.shifty
                #added
                self.rect.center = (self.initx, self.inity)

        def update(self):
                self.image = Player.all_players[int(self.playnum)]
                self.rect.x = self.initx
                self.rect.y = self.inity

