import cv2
import numpy as np
import sys

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <foto a ser avaliada>"
		sys.exit(1)
	dataFile = sys.argv[1]

	img = cv2.imread(dataFile)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	minLineLength = 100
	maxLineGap = 10

	lines = cv2.HoughLinesP(edges,1,np.pi*45/180,100,minLineLength,maxLineGap)

	horizontalCounter = 0
	verticalCounter = 0
	diagonalCounter = 0
	for x1,y1,x2,y2 in lines[0]:
	    #print str(x1) + " " + str(x2) + " " + str(y1) + " " + str(y2)
	    #cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	    #cv2.line(img, (581, 309), (581, 279), (0,255,0),2)
	    #cv2.line(img, (578, 280), (578, 230), (0,255,0),2)
	    #cv2.line(img, (5, 433), (17, 421), (0,255,0),2)
	    #cv2.line(img, (129, 152), (143, 152), (0,255,0),2)
	    if x1 == x2:
		verticalCounter += 1
	    elif y1 == y2:
		horizontalCounter += 1
	    else:
		diagonalCounter += 1
	
	print dataFile + "\t" + str(diagonalCounter) + "\t" + str(horizontalCounter) + "\t" + str(verticalCounter)
	#cv2.imwrite('houghlines5.jpg',img)
