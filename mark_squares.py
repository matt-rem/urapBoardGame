#Code from GeeksForGeeks: https://www.geeksforgeeks.org/displaying-the-coordinates-of-the-points-clicked-on-the-image-using-python-opencv/

# importing the modules 
import cv2
import csv 
import sys

#square position number
sq_num = 1
undoCount = 0

#first time opens a csv file (the csv file must already exist)
'''
with open('sample.csv', mode='w') as sfile:
    f_writer = csv.writer(sfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f_writer.writerow(['Game Name','Player Count','x coordinate', 'y coordinate', 'type','next square', 'next x ','next y'])
    name = input("Enter the name of the game: ")
    playercount = input("Enter the number of players: ")
    f_writer.writerow([name, playercount,'', '', '','', '','', ''])
'''
dataArray = []

name = input("Enter the name of the game: ")
playercount = input("Enter the maximum number of players: ")
dataArray.append(['Game Name','Max Player Count','x coordinate', 'y coordinate', 'Square Number','Next Square Number', 'type', 'misc1', 'misc2'])
dataArray.append([name, playercount,'', '', '', '', '', '', ''])
#click to display the square position, as well as the x, y coordinate of mouse click (preferrably the user should
#click in the center of the square on the board)
def click_event(event, x, y, flags, params): 
    global sq_num;
      # checking for left mouse clicks 
    global undoCount;
    #if event != 0:
        #print(event, "going in")
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX
        
       
        #append to already open csv file
        #write x, y of mouse click, square position, next square gets square position +1
        '''
        with open('sample.csv', mode='a') as sfile:
           f_writer = csv.writer(sfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           f_writer.writerow(['','',x, y, sq_num, sq_num + 1,'','', ''])
        '''
        dataArray.append(['','', x, y, sq_num, sq_num + 1,'','', ''])

        if undoCount == 0:
            #on the image show the square position number's x, y coordinate
            cv2.putText(img,str(sq_num), (x,y), font, 
                        0.5, (0, 0, 0), 2) 
        else:
            #on the image show the square position number's x, y coordinate
            #print("UNDO")
            cv2.putText(img,str(sq_num), (x,y), font, 
                        0.5, (255, 0, 0), 2)   
            undoCount -= 1
        cv2.imshow('image', img)


        #increment the square position for the next click
        sq_num += 1
    
  
        
    
  
# driver function 
if __name__=="__main__": 
  
    # reading the image
    #hard coded for now EDIT: Not anymore see below.
    imgname = str(sys.argv[1])
    print("Click on the center of each square.")


    img = cv2.imread(imgname, 1) #sys.argv[0] =  testBoard.jpg (RUN TERMINAL W/ python mark_squares.py testBoard.jpg)

  
    # displaying the image 
    cv2.imshow('image', img) 
  
    # setting mouse hadler for the image 
    # and calling the click_event() function 


    cv2.setMouseCallback('image', click_event) 
  
    # press any key to exit 
    #cv2.waitKey(0)
    running = True
    while running:
        k = cv2.waitKey(0);
        #print(k)
        #Press escape for exit from program
        if k == 27:
            #print(dataArray)
            #Delete old csv file
            f = open("sample.csv", "w")
            f.truncate()
            f.close()


            #Final edits: Sets square 1 as start, square n as dice, and square n - 1 as finish
            for i in range(2, len(dataArray)):
                #print(dataArray[i][4], first)
                if int(dataArray[i][4]) == 1:
                    dataArray[i][6] = "start"
                if int(dataArray[i][4]) == len(dataArray) - 3:
                    dataArray[i][6] = "finish"
                if int(dataArray[i][4]) == len(dataArray) - 2:
                    dataArray[i][6] = "dice"

            #Write into csv file
            with open('sample.csv', mode='a') as sfile:
                f_writer = csv.writer(sfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in dataArray:
                    f_writer.writerow(i)
            
          
            # close the window 
            cv2.destroyAllWindows() 
            running = False
        # Press L for ladder
        if k == 108: 
            # displaying the coordinates 
            # on the image window 
            #print(dataArray)
            first = input("Enter number of the first square of the ladder or slide: ")
            second = input("Enter number of the second square of the ladder or slide: ")
            
            #Sets the square's (first) special to ladder which takes in on eargument (second)
            for i in range(2, len(dataArray)):
                #print(dataArray[i][4], first)
                if int(dataArray[i][4]) == int(first):
                    dataArray[i][6] = "ladder"
                    dataArray[i][7] = second
                    break
        #Press backspace for undo. Can only undo if you numbered a square. Cannot undo ladders.
        if k == 127: 
            if len(dataArray) > 2:
                undoCount += 1
                sq_num -= 1
                dataArray.pop()

