import cv2
import numpy as np

# HSV color ranges
ranges = [[(160, 179),(106, 255),(0, 255)], # Red
		[(60, 90),(81, 255),(0, 255)],	# Green
		[(100, 119),(136, 255),(0, 255)]] # Blue

#Clear noise when reading image contours

def clearNoise(img):
	kernel = np.ones((10, 10), np.uint8)
	clrimg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	clrimg = cv2.erode(img, kernel, iterations=1)
	kernel = np.ones((15, 15), np.uint8)
	clrimg = cv2.dilate(img, kernel, iterations=2)
	# Clears noise from image
	return clrimg

#Filter Out Each ColorBand covered Finger

def filterFingers(img):
		
	height = img.shape[0]
	width = img.shape[1]

	imgcropped = img[0:(height/2), (width/2):(width-1)] # Cropping the ROI

	fingerArray = []

	min = np.array([ranges[0][0][0], ranges[0][1][0], ranges[0][2][0]], np.uint8)
	max = np.array([ranges[0][0][1], ranges[0][1][1], ranges[0][2][1]], np.uint8)
	red = cv2.inRange(imgcropped, min, max)
	red = clearNoise(red)
	fingerArray.append(red)

	min = np.array([ranges[1][0][0], ranges[1][1][0], ranges[1][2][0]], np.uint8)
	max = np.array([ranges[1][0][1], ranges[1][1][1], ranges[1][2][1]], np.uint8)
	green = cv2.inRange(imgcropped, min, max)
	green = clearNoise(green)
	fingerArray.append(green)

	min = np.array([ranges[2][0][0], ranges[2][1][0], ranges[2][2][0]], np.uint8)
	max = np.array([ranges[2][0][1], ranges[2][1][1], ranges[2][2][1]], np.uint8)
	blue = cv2.inRange(imgcropped, min, max)
	blue = clearNoise(blue)
	fingerArray.append(blue)

	# Returns an array of three filtered fingers images
	return fingerArray

#Get coordinates of each fingers/bands topmost point

def getPositions(imgArray):
	# Returns the topmost points of filtered blobs from given imgs

	positions=[]

	for img in imgArray:

		contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		if len(contours)<1:
			positions.append((0,0))
			continue


		cnt=contours[0]

		topmost = tuple(cnt[cnt[:,:,1].argmin()][0])

		positions.append(topmost)

	return positions