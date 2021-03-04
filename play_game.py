import math
import random
import csv
from PIL import Image
import pygame
#from pygame import mixer

# Intialize the pygame
pygame.init()

#get the height and width of the board game image we want to use
#im = Image.open('/Users/klalgudi/Desktop/mygame/board_game.jpg')
im = Image.open('board_game.jpg')
w, h = im.size 

# create 2 1-dimensional arrays to store x,y positions of every square
arrx =[]
arry= []

# create the screen
screen = pygame.display.set_mode((w,h))

# open sample.csv (which should have the x,y coordinates of the squares)
with open('sample.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

#put the x, y values into arr, the 2  1-dimensional arrays
for i in range(len(data)):
  arrx.append(data[i][2])
  arry.append(data[i][3])


# Background
background = pygame.image.load('board_game.jpg')

#Load dice and token images
dice1=pygame.image.load("dice1.png")
dice2=pygame.image.load("dice2.png")
dice3=pygame.image.load("dice3.png")
dice4=pygame.image.load("dice4.png")
dice5=pygame.image.load("dice5.png")
dice6=pygame.image.load("dice6.png")

#Only 2 players for now
player1=pygame.image.load("blue_piece.png")
player2=pygame.image.load("green_piece.png")


#function to load correct dice image 
def dice(a):
    if a==1:
        a=dice1
    elif a==2:
        a=dice2
    elif a==3:
        a=dice3
    elif a==4:
        a=dice4
    elif a==5:
        a=dice5
    elif a==6:
        a=dice6

    #draw the correct image at the dice position we found in the csv
    screen.blit(a,(int(arrx[len(data)-1]),int(arry[len(data)-1])))

#draw the player at the x, y position
def move(a,x,y):
    if a==1:
        b=player1
    elif a==2:
        b=player2
    
    screen.blit(b,(int(x),int(y)))


#code runs until the value becomes false
#this happens when the player quits the game or the game is over    
running = True

#start with dice image 1 (one dot)
a= 1
#start with it being player 1's turn
turn = 1

#b is player 1
#c is player 2
b=1
c=2

#I tried to make sure one does not completely overlap the other on the start square
#i, j are the initial position for player 1
i = int(arrx[1]) + 10
j = int(arry[1]) - 70

#l, m are the initial position for player 2
l = int(arrx[1]) + 10
m = int(arry[1]) - 40

#both start at square 1 on the board
sqr1 = 1
sqr2 = 1
winner = False
#do this until the game ends or a player wins
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background,(0,0))
    
    #calls method that "paints" the dice at the dice position taken from the csv
    dice(a)

    #"paints" players at positions (i, j) for player1, and (l, m) for player2 
    move(b,i,j)
    move(c,l,m)
    

    roll =None

    #get all the events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if the event is a space bar (the space bar is pressed)    
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #get a random number between 1 and 6
            roll = random.randint(1,6)


            #if it is player 1's turn and not on the finish square
            if turn == 1 and winner == False:
              #find the square player 1 must move to
              sqr1 = sqr1 + roll
              #if the square is beyond the finish square, place player on finish and we end the game
              #experimented with delay
              
              #print('sqr 1 = ', str(sqr1))
              if sqr1 >= len(data) - 2:

                
                i = arrx[len(data)-2]
                j = arry[len(data)-2]
                winner = True
                
              else:  
                #find the x, y coordinate for that square
                i = arrx[sqr1]
                j = arry[sqr1]
                #set turn to player 2
                turn = 2

              
              

            #if it is player 2's turn then we do exactly the same thing as above
            elif turn == 2 and winner == False:
              #find the square player 2 must move to
              sqr2 = sqr2 + roll
              #if the square is beyond the finish square, place player on finish and we end the game
              #print('sqr 2 = ', str(sqr2))
              if sqr2 >= len(data) - 2:
                
                l = arrx[len(data)-2]
                m = arry[len(data)-2]
                winner = True
                
              else:
                #find the x, y coordinate for that square  
                l = arrx[sqr2]
                m = arry[sqr2]
                #set turn to player 1
                turn = 1
              
   
    #first check if roll has a value
    #if yes, set it to the randomly generated dice value so that the corresponding dice image is painted
    if roll:
       if roll == 6:
         a=6
       if roll == 5:
         a=5
       if roll == 4:
         a=4
       if roll == 3:
         a=3
       if roll == 2:
         a=2
       if roll == 1:
         a=1
    
    
    #updates the entire screen
    pygame.display.flip()




