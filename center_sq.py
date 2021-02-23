# import the necessary packages
import argparse
import imutils
import cv2

import numpy as np

# construct the argument parse and parse the arguments
'''ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())'''
# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread('color_board.png')


#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

#thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.threshold(sharpen,160,255, cv2.THRESH_BINARY_INV)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)


cv2.imshow('thresh', thresh)
# find contours in the thresholded image
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
print(str(len(cnts)))
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	if(M["m00"]!=0):
	   cX = int(M["m10"] / M["m00"])
	   cY = int(M["m01"] / M["m00"])
	else:
		cX, cY = 0,0  
	# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	# show the image
	cv2.imshow("Image", image)
	cv2.waitKey(0)