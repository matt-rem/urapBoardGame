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
                self.rect = self.image.get_rect()

                self.skip = False


                #SHIFTS to make image in center:
                self.shiftx, self.shifty = self.image.get_size()
                self.shiftx, self.shifty = self.shiftx / 2 , self.shifty / 2
                #Piece x and y
                self.initx = x - self.shiftx
                self.inity = y - self.shifty
                
                self.rect.center = (self.initx,self.inity)


                #offset to prevent overlapping
                self.x_offset = 3
                self.y_offset = 3

                #For currency
                self.bal = 0


        #returns player's name
        def getName(self):
                return self.player_name


        def getBal(self):
                return self.bal

        #get the square the player is currently on
        def getSquare(self):
                return self.square

        #set the player's new square
        def setSquare(self, sq):
                self.square = sq
                return

        #change the player's position
        def onRoll(self,x,y):
                self.initx = x - self.shiftx
                self.inity = y - self.shifty
                #added
                self.rect.center = (self.initx, self.inity)

        #get the player's x offset value
        def getXOffset(self):
                return self.x_offset

        #get the player's y offset value
        def getYOffset(self):
                return self.y_offset


        #set the player's offset based on which player they are
        def setOffset(self, turn):
                if turn == 1:
                        self.x_offset = -3
                        self.y_offset = 3 
                elif turn == 2:
                        self.x_offset = -3
                        self.y_offset = -3
                elif turn == 3:
                        self.x_offset = 3
                        self.y_offset = -3

        #decides whether the player should be skipping their turn
        def skip_turn(self):
                self.skip = not self.skip

        #return whether the player's turn has been skipped
        def skipped(self):
                return self.skip


        #update the player image
        def update(self):
                self.image = Player.all_players[int(self.playnum)]
                self.rect.x = self.initx
                self.rect.y = self.inity

