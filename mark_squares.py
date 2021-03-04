#Code from GeeksForGeeks: https://www.geeksforgeeks.org/displaying-the-coordinates-of-the-points-clicked-on-the-image-using-python-opencv/

# importing the modules 
import cv2
import csv 

#square position number
sq_num = 1

#first time opens a csv file (the csv file must already exist)
with open('sample.csv', mode='w') as sfile:
           f_writer = csv.writer(sfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           f_writer.writerow(['Game Name','Player Count','x coordinate', 'y coordinate', 'type','next square', 'next x ','next y'])   




#click to display the square position, as well as the x, y coordinate of mouse click (preferrably the user should
#click in the center of the square on the board)
def click_event(event, x, y, flags, params): 
    global sq_num;
      # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX
        
       
        #append to already open csv file
        #write x, y of mouse click, square position, next square gets square position +1
        with open('sample.csv', mode='a') as sfile:
           f_writer = csv.writer(sfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           f_writer.writerow(['','',x, y, sq_num, sq_num+1,'',''])

        #on the image show the square position number's x, y coordinate
        cv2.putText(img,str(sq_num) + ':' + '('+str(x) + ',' +
                    str(y)+')', (x,y), font, 
                    0.5, (0, 0, 0), 2) 
        cv2.imshow('image', img)

        #increment the square position for the next click
        sq_num += 1
    
  
# driver function 
if __name__=="__main__": 
  
    # reading the image
    #hard coded for now 
    img = cv2.imread('board_game.jpg', 1) 
  
    # displaying the image 
    cv2.imshow('image', img) 
  
    # setting mouse hadler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('image', click_event) 
  
    # press space bar to exit 
    #cv2.waitKey(0)
    cv2.waitKey(0) 
  
    # close the window 
    cv2.destroyAllWindows() 

