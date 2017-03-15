from __future__ import division

import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

# mu is defined as a triangular membership function with a peak value of 1 at T.
def mu(minimum, maximum, T, x):
	# Rising slope line. Also use when T is the maximum to avoid division by zero.
	if T != minimum and (x < T or T == maximum):
		return (x - minimum)/(T - minimum)
	# Falling slope line. Also use when T is the minimum to avoid division by zero.
	else:
		return 1 - (x - T)/(maximum - T)

def type2threshold(histogram, hedge, minimum, maximum):
	maxUF = 0
	bestT = minimum
	for T in range(minimum, maximum + 1):
		UF = 0
		for x in range(minimum, maximum + 1):
			muSkeleton = mu(minimum, maximum, T, x)
			UF += histogram[x]*((muSkeleton**(1/hedge)) - (muSkeleton**(hedge)))
		if UF > maxUF:
			maxUF = UF
			bestT = T
	return bestT

def rotate_image(image, angle):
  '''Rotate image "angle" degrees.

  How it works:
    - Creates a blank image that fits any rotation of the image. To achieve
      this, set the height and width to be the image's diagonal.
    - Copy the original image to the center of this blank image
    - Rotate using warpAffine, using the newly created image's center
      (the enlarged blank image center)
    - Translate the four corners of the source image in the enlarged image
      using homogenous multiplication of the rotation matrix.
    - Crop the image according to these transformed corners
  '''

  diagonal = int(math.sqrt(pow(image.shape[0], 2) + pow(image.shape[1], 2)))
  offset_x = (diagonal - image.shape[0])/2
  offset_y = (diagonal - image.shape[1])/2
  dst_image = np.zeros((diagonal, diagonal, 3), dtype='uint8')
  image_center = (diagonal/2, diagonal/2)

  R = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  dst_image[offset_x:(offset_x + image.shape[0]), \
            offset_y:(offset_y + image.shape[1]), \
            :] = image
  dst_image = cv2.warpAffine(dst_image, R, (diagonal, diagonal), flags=cv2.INTER_LINEAR)

  # Calculate the rotated bounding rect
  x0 = offset_x
  x1 = offset_x + image.shape[0]
  x2 = offset_x
  x3 = offset_x + image.shape[0]

  y0 = offset_y
  y1 = offset_y
  y2 = offset_y + image.shape[1]
  y3 = offset_y + image.shape[1]

  corners = np.zeros((3,4))
  corners[0,0] = x0
  corners[0,1] = x1
  corners[0,2] = x2
  corners[0,3] = x3
  corners[1,0] = y0
  corners[1,1] = y1
  corners[1,2] = y2
  corners[1,3] = y3
  corners[2:] = 1

  c = np.dot(R, corners)

  x = int(c[0,0])
  y = int(c[1,0])
  left = x
  right = x
  up = y
  down = y

  for i in range(4):
    x = int(c[0,i])
    y = int(c[1,i])
    if (x < left): left = x
    if (x > right): right = x
    if (y < up): up = y
    if (y > down): down = y
  h = down - up
  w = right - left

  cropped = np.zeros((w, h, 3), dtype='uint8')
  cropped[:, :, :] = dst_image[left:(left+w), up:(up+h), :]
  return cropped

# Load a colour image in grayscale and get the dimensions to crop.
img = cv2.imread('actual.jpg', 1)
h, w = img.shape[:2]
print 'H, W:', h, w
img = img[300:2700, 700:3300]
plt.imshow(img, cmap='gray')
plt.show()

# Rotate the image to the upright orientation.
img = rotate_image(img, -90)
plt.imshow(img, cmap='gray')
plt.show()

# Copy this image for later visualization.
boxImg = img.copy()
linesImg = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#centreLineImg = img.copy()

# Increase contrast.
new_img = img.copy()
array_alpha = np.array([10.0])
array_beta = np.array([-50.0])
# Add a beta value to every pixel.
cv2.add(new_img, array_beta, new_img)
# Multiply every pixel value by alpha.
cv2.multiply(new_img, array_alpha, new_img)

# Obtain intensity gradient image.
sobelx = cv2.Sobel(new_img,cv2.CV_8U,1,0,ksize=3)
sobely = cv2.Sobel(new_img,cv2.CV_8U,0,1,ksize=3)
sobelx = sobelx.astype(np.uint16)
sobely = sobely.astype(np.uint16)
#gradientImg = np.round(np.divide(np.sqrt(np.square(sobelx) + np.square(sobely)), math.sqrt(2)))
gradientImg = np.round(np.divide(sobelx + sobely, 1))

# Obtain a histogram of the intensity gradient.
hist = cv2.calcHist([gradientImg], [0], None, [512], [0, 512])
T = type2threshold(hist, 2, 0, 511)
Tlower = type2threshold(hist, 2, 0, T - 1)
Tupper = type2threshold(hist, 2, T + 1, 511)
h, w = img.shape[:2]
print 'H, W:', h, w
print 'Type 2 threshold, Tlower, Tupper:', T, Tlower, Tupper
#plt.hist(gradientImg.ravel(),256,[0,256]);
#plt.imshow(gradientImg, cmap='gray')
#plt.show()

# Intensity threshold.
ret, thresh = cv2.threshold(new_img, 160, 255, 0)
plt.imshow(thresh, cmap='gray')
plt.show()

kernel = np.ones((10,10),np.uint8)

# Erosion filter.
thresh = cv2.erode(thresh,kernel,iterations = 5)
thresh = cv2.dilate(thresh,kernel,iterations = 5)
plt.imshow(thresh, cmap='gray')
plt.show()

# Dilation filter.
thresh = cv2.dilate(thresh,kernel,iterations = 15)
thresh = cv2.erode(thresh,kernel,iterations = 15)
plt.imshow(thresh, cmap='gray')
plt.show()

# Copy the thresholded image.
filledImg = thresh.copy()
 
# Mask used to flood filling.
# Notice the size needs to be 2 pixels than the image.
h, w = thresh.shape[:2]
floodMask = np.zeros((h+2, w+2), np.uint8)
 
# Floodfill from corners.
cv2.floodFill(filledImg, floodMask, (0,0), 255)
cv2.floodFill(filledImg, floodMask, (0,h-1), 255)
cv2.floodFill(filledImg, floodMask, (w-1,0), 255)
cv2.floodFill(filledImg, floodMask, (w-1,h-1), 255)
plt.imshow(filledImg, cmap='gray')
plt.show()

# Perform edge detection.
edges = cv2.Canny(filledImg, Tlower, Tupper)
#edges = cv2.dilate(edges,kernel,iterations = 1)
plt.imshow(edges, cmap='gray')
plt.show()

contours,hierarchy = cv2.findContours(edges.copy(), 1, 2)
cntrs = contours[0]

# Draw a least area bounding rectangle around the contours.
rect = cv2.minAreaRect(cntrs)
box = cv2.cv.BoxPoints(rect)
box = np.int0(box)
boxCentre = [(box[0,0]+box[1,0]+box[2,0]+box[3,0])/4,(box[0,1]+box[1,1]+box[2,1]+box[3,1])/4]

# Angle is measured clockwise from the vertical. Assume that it is between -45 deg. and 45 deg.
if rect[2] < -45:
	angle = rect[2] + 90
else:
	angle = rect[2]
print 'Bounding Rectangle Angle (degrees):', angle
print 'Bounding Rectangle Centre Horizontal Position (Pixels):', boxCentre[0]
print 'Bounding Rectangle Centre Vertical Position (Pixels):', boxCentre[1]
cv2.drawContours(boxImg, [box], 0, (0,0,255), 2)
plt.imshow(boxImg, cmap='gray')
plt.show()

lines = cv2.HoughLinesP(image=edges,rho=0.1,theta=1*np.pi/720, threshold=10,lines=np.array([]), minLineLength=100,maxLineGap=100)
N = lines[0].shape[0]
for i in range(N):
    x1 = lines[0][i][0]
    y1 = lines[0][i][1]    
    x2 = lines[0][i][2]
    y2 = lines[0][i][3]    
    cv2.line(linesImg,(x1,y1),(x2,y2),(255,0,0),2)
print N
plt.imshow(linesImg, cmap='gray')
plt.show()

lines = lines[0]
nonOrthogonalLineCount = 0
# Get longest 2 lines detected.
leftLengthSqrd = 0
rightLengthSqrd = 0
leftIndex = -1
rightIndex = -1
for i in range(len(lines)):
	# Get only lines that are roughly close to vertical.
	# TODO: Change this to an angle tolerance instead of x?
	if abs(lines[i,2]-lines[i,0]) < 50:
		lineLengthSqrd = ((lines[i,2]-lines[i,0])*(lines[i,2]-lines[i,0])+(lines[i,3]-lines[i,1])*(lines[i,3]-lines[i,1]))
		lineAvgX = (lines[i,2]+lines[i,0])/2
		if lineAvgX < w/2 and lineLengthSqrd > leftLengthSqrd:
			leftLengthSqrd = lineLengthSqrd
			leftIndex = i
		elif lineAvgX > w/2 and lineLengthSqrd > rightLengthSqrd:
			rightLengthSqrd = lineLengthSqrd
			rightIndex = i
	if (abs(lines[i,2]-lines[i,0]) > 0) and (abs(lines[i,3]-lines[i,1]) > 0):
		nonOrthogonalLineCount += 1
	lineList = [lines[i,0],lines[i,1]],[lines[i,2],lines[i,3]]
	lineCntr = np.array(lineList)
	#cv2.drawContours(lineThreshImg, [lineCntr], -1, (255,0,0), 2)
# Create contours for the two longest lines.
leftLineList = [lines[leftIndex,0],lines[leftIndex,1]],[lines[leftIndex,2],lines[leftIndex,3]]
rightLineList = [lines[rightIndex,0],lines[rightIndex,1]],[lines[rightIndex,2],lines[rightIndex,3]]
leftLineCntr = np.array(leftLineList)
rightLineCntr = np.array(rightLineList)
# Swap the leftLineCntr points if they are mismatched to the order of rightLineCntr points.
if np.linalg.norm(rightLineCntr[0]-leftLineCntr[0]) > np.linalg.norm(rightLineCntr[0]-leftLineCntr[1]):
	# Copy used because for some reason numpy array values don't follow Python tuple swapping.
	leftLineCntr[0], leftLineCntr[1] = leftLineCntr[1].copy(), leftLineCntr[0].copy()
# Approximate a centerline as the average between the two longest lines.
centreLineList = [(int)((leftLineCntr[0,0]+rightLineCntr[0,0])/2),
				  #min(leftLineCntr[0,1], rightLineCntr[0,1])], \
				  (int)((leftLineCntr[0,1]+rightLineCntr[0,1])/2)], \
				 [(int)((leftLineCntr[1,0]+rightLineCntr[1,0])/2),
				  (int)((leftLineCntr[1,1]+rightLineCntr[1,1])/2)]
				  #max(leftLineCntr[1,1], rightLineCntr[1,1])]
centreLineCntr = np.array(centreLineList)
lineImg = np.zeros((h, w), np.uint8)
#centreLineCntr[1,0] += 50	# REMOVE THIS AFTER TESTING ANGLES
print leftLineCntr
print rightLineCntr
print centreLineCntr
cv2.drawContours(lineImg, [leftLineCntr], -1, (255,0,0), 2)
cv2.drawContours(lineImg, [rightLineCntr], -1, (255,0,0), 2)
cv2.drawContours(lineImg, [centreLineCntr], -1, (255,255,255), 2)

# Arrange centre line with bottom (y) point first when measuring angle.
if centreLineCntr[0,1] > centreLineCntr[1,1]:
	centreLineCntr[0], centreLineCntr[1] = centreLineCntr[1].copy(), centreLineCntr[0].copy()
# Determine line angle using regular atan, since only quadrants 1 and 4 are desired
# (shifts to quadrants 1 and 2 after adjustment).
if centreLineCntr[0,0] == centreLineCntr[1,0]:
	angle = 0
else:
	print -1.0*(centreLineCntr[1,1]-centreLineCntr[0,1])/(centreLineCntr[1,0]-centreLineCntr[0,0])
	# Compensate for reading from top left by negating y values.
	angle = (math.atan(-1.0*(centreLineCntr[1,1]-centreLineCntr[0,1])/(centreLineCntr[1,0]-centreLineCntr[0,0]))*180/math.pi)
	# Measure angle from vertical, where a positive value indictes CCW rotation.
	if angle < 0:
		angle += 90
	else:
		angle -= 90
print 'Centre Line Angle (degrees):', angle
leftAvgX = (leftLineCntr[0,0]+leftLineCntr[1,0])/2
rightAvgX = (rightLineCntr[0,0]+rightLineCntr[1,0])/2
centreAvgX = (centreLineCntr[0,0]+centreLineCntr[1,0])/2
print 'Centre Line Average Horizontal Position (Pixels):', centreAvgX
print 'Left Line Average Horizontal Position (Pixels):', leftAvgX
print 'Right Line Average Horizontal Position (Pixels):', rightAvgX
print 'Non-orthogonal Line Count:', nonOrthogonalLineCount
plt.imshow(lineImg, cmap='gray')
plt.show()

'''
Corner pixel coordinates:
Lower left: (160, 2325)
Lower right: (2210, 2300)
Upper left: (165, 255)
Upper right: (2215, 270)

Board dimensions:
30 in. x 30 in. = 762 mm x 762 mm

Vertical lines (measured from left):
xDist= (x - 162)/(2212 - 162) * (762 mm)
Horizontal lines (measured from top):
yDist = (y - 262)/(2312 - 262) * (762 mm)
'''
leftEdgeDist = (leftAvgX - 162)/(2212 - 162) * 762
rightEdgeDist = (rightAvgX - 162)/(2212 - 162) * 762
print 'Left Edge Position (mm):', leftEdgeDist
print 'Right Edge Position (mm:', rightEdgeDist

leftFoldPixel = (int)((leftAvgX + centreAvgX)/2)
rightFoldPixel = (int)((rightAvgX + centreAvgX)/2)
crossFoldPixel = (int)(boxCentre[1])
print 'Left Fold Position (Pixels):', leftFoldPixel
print 'Right Fold Position (Pixels):', rightFoldPixel
print 'Cross Fold Position (Pixels):', crossFoldPixel
leftXDist = (leftFoldPixel - 162)/(2212 - 162) * 762
rightXDist = (rightFoldPixel - 162)/(2212 - 162) * 762
crossYDist = (crossFoldPixel - 262)/(2312 - 262) * 762
print 'Left Fold Position (mm):', leftXDist
print 'Right Fold Position (mm):', rightXDist
print 'Cross Fold Position (mm):', crossYDist

exit()

# RANDOM TESTING BELOW

# Find edges using Canny edge detection and threshold and dilate the result.
edges = cv2.Canny(new_img,270,270)
ret,thresh = cv2.threshold(edges,127,255,0)

kernel = np.ones((10,10),np.uint8)
thresh = cv2.dilate(thresh,kernel,iterations = 1)
#thresh = cv2.erode(thresh,kernel,iterations = 1)

edges = cv2.dilate(edges,kernel,iterations = 3)

contours,hierarchy = cv2.findContours(thresh.copy(), 1, 2)
maxCntrLength = 0
#print 'Number of contours:', len(contours)
for index in range(len(contours)):
	if len(contours[index]) > maxCntrLength:
		cntrs = contours[index]
		maxCntrLength = len(contours[index])
	#print 'Current contour length:', len(contours[index])
#cntrs = contours[0]
#print len(cntrs)

# Draw a least area bounding rectangle around the contours. POSSIBLY UNEEDED
rect = cv2.minAreaRect(cntrs)
box = cv2.cv.BoxPoints(rect)
box = np.int0(box)
boxCentre = [(box[0,0]+box[1,0]+box[2,0]+box[3,0])/4,(box[0,1]+box[1,1]+box[2,1]+box[3,1])/4]

#print rect[2]
cv2.drawContours(boxImg, [box], 0, (0,0,255), 2)
cv2.imwrite('boxImg.jpg', boxImg)

contoursPoly = [cv2.approxPolyDP(cnt, 3, True) for cnt in cntrs]
contourImg = np.zeros((h, w, 3), np.uint8)
perimeter=[]
for cnt in contoursPoly[1:]:
    perimeter.append(cv2.arcLength(cnt,True))
maxindex = perimeter.index(max(perimeter))
#centreLine = cv2.fitLine(cntrs,distType=cv2.cv.CV_DIST_L2,param=0,reps=0.01,aeps=0.01)
#cv2.line(centreLineImg, (centreLine[0], centreLine[1]), (centreLine[2], centreLine[3]), (0,255,0), 2)
#cv2.imwrite('centreLineImg.jpg', centreLineImg)

#cv2.drawContours(contourImg, contoursPoly, maxindex + 1, (255,0,0), -1)
cv2.polylines(contourImg, [cntrs], True, (0,255,255))
contourImg = cv2.dilate(contourImg,kernel,iterations = 3)
contourImg = cv2.cvtColor(contourImg, cv2.COLOR_BGR2GRAY)

# Get hough lines for the edges with large maximum gap to aim for long lines along length of shirt.
minLineLength = 100 #img.shape[1] - 300
lineThreshImg = np.zeros((h,w),np.uint8)
lines = cv2.HoughLinesP(contourImg, 0.02, np.pi/180, 10, np.array([]), minLineLength, 100)
lines = None
if lines != None:
	lines = lines[0]
	nonOrthogonalLineCount = 0
	# Get longest 2 lines detected.
	leftLengthSqrd = 0
	rightLengthSqrd = 0
	leftIndex = -1
	rightIndex = -1
	for i in range(len(lines)):
		# Get only lines that are roughly close to vertical.
		# TODO: Change this to an angle tolerance instead of x?
		if abs(lines[i,2]-lines[i,0]) < 50:
			lineLengthSqrd = ((lines[i,2]-lines[i,0])*(lines[i,2]-lines[i,0])+(lines[i,3]-lines[i,1])*(lines[i,3]-lines[i,1]))
			lineAvgX = (lines[i,2]+lines[i,0])/2
			if lineAvgX < w/2 and lineLengthSqrd > leftLengthSqrd:
				leftLengthSqrd = lineLengthSqrd
				leftIndex = i
			elif lineAvgX > w/2 and lineLengthSqrd > rightLengthSqrd:
				rightLengthSqrd = lineLengthSqrd
				rightIndex = i
		if (abs(lines[i,2]-lines[i,0]) > 0) and (abs(lines[i,3]-lines[i,1]) > 0):
			nonOrthogonalLineCount += 1
		lineList = [lines[i,0],lines[i,1]],[lines[i,2],lines[i,3]]
		lineCntr = np.array(lineList)
		cv2.drawContours(lineThreshImg, [lineCntr], -1, (255,0,0), 2)
	# Create contours for the two longest lines.
	leftLineList = [lines[leftIndex,0],lines[leftIndex,1]],[lines[leftIndex,2],lines[leftIndex,3]]
	rightLineList = [lines[rightIndex,0],lines[rightIndex,1]],[lines[rightIndex,2],lines[rightIndex,3]]
	leftLineCntr = np.array(leftLineList)
	rightLineCntr = np.array(rightLineList)
	# Swap the leftLineCntr points if they are mismatched to the order of rightLineCntr points.
	if np.linalg.norm(rightLineCntr[0]-leftLineCntr[0]) > np.linalg.norm(rightLineCntr[0]-leftLineCntr[1]):
		# Copy used because for some reason numpy array values don't follow Python tuple swapping.
		leftLineCntr[0], leftLineCntr[1] = leftLineCntr[1].copy(), leftLineCntr[0].copy()
	# Approximate a centerline as the average between the two longest lines.
	centreLineList = [(leftLineCntr[0,0]+rightLineCntr[0,0])/2,
					  (leftLineCntr[0,1]+rightLineCntr[0,1])/2],	\
					 [(leftLineCntr[1,0]+rightLineCntr[1,0])/2,
					  (leftLineCntr[1,1]+rightLineCntr[1,1])/2]
	centreLineCntr = np.array(centreLineList)
	lineImg = np.zeros((h, w), np.uint8)
	#centreLineCntr[1,0] += 50	# REMOVE THIS AFTER TESTING ANGLES
	cv2.drawContours(lineImg, [leftLineCntr], -1, (255,0,0), 2)
	cv2.drawContours(lineImg, [rightLineCntr], -1, (255,0,0), 2)
	cv2.drawContours(lineImg, [centreLineCntr], -1, (255,255,255), 2)

	# Arrange centre line with bottom (y) point first when measuring angle.
	if centreLineCntr[0,1] > centreLineCntr[1,1]:
		centreLineCntr[0], centreLineCntr[1] = centreLineCntr[1].copy(), centreLineCntr[0].copy()
	# Determine line angle using regular atan, since only quadrants 1 and 4 are desired
	# (shifts to quadrants 1 and 2 after adjustment).
	if centreLineCntr[0,0] == centreLineCntr[1,0]:
		angle = 0
	else:
		print -1.0*(centreLineCntr[1,1]-centreLineCntr[0,1])/(centreLineCntr[1,0]-centreLineCntr[0,0])
		# Compensate for reading from top left by negating y values.
		angle = (math.atan(-1.0*(centreLineCntr[1,1]-centreLineCntr[0,1])/(centreLineCntr[1,0]-centreLineCntr[0,0]))*180/math.pi)
		# Measure angle from vertical, where a positive value indictes CCW rotation.
		if angle < 0:
			angle += 90
		else:
			angle -= 90
	print 'Centre Line Angle (degrees):', angle
	centreAvgX = (centreLineCntr[0,0]+centreLineCntr[1,0])/2
	print 'Centre Line Average Horizontal Position (Pixels):', centreAvgX
	print 'Non-orthogonal Line Count:', nonOrthogonalLineCount
#cv2.drawContours(img,[cntrs],-1,(0,255,0),2)

# Plot images in subplots.
plt.subplot(331),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(332),plt.imshow(new_img,cmap = 'gray')
plt.title('Increased Contrast'), plt.xticks([]), plt.yticks([])
plt.subplot(333),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.subplot(334),plt.imshow(contourImg,cmap = 'gray')
plt.title('Contours'), plt.xticks([]), plt.yticks([])
plt.subplot(335),plt.imshow(thresh,cmap = 'gray')
plt.title('Threshold'), plt.xticks([]), plt.yticks([])
if 'lineImg' in globals():
	lineImg = cv2.dilate(lineImg, kernel, iterations = 3)
	plt.subplot(336),plt.imshow(lineImg,cmap = 'gray')
	plt.title('Longest Line'), plt.xticks([]), plt.yticks([])
plt.subplot(337),plt.imshow(lineThreshImg,cmap = 'gray')
plt.title('Threshold with Lines'), plt.xticks([]), plt.yticks([])

plt.show()

cv2.imwrite('contours.jpg', contourImg)

# ARC LENGTH
#print cv2.arcLength(cntrs,True)

# APPROXIMATE POLYLINE FOR CONTOURS
#epsilon = 0.1*cv2.arcLength(cntrs,True)
#approx = cv2.approxPolyDP(cntrs,epsilon,True)

# APPROXIMATE FIT LINE
#rows,cols = img.shape[:2]
#[vx,vy,x,y] = cv2.fitLine(cntrs, cv2.cv.CV_DIST_L2,0,0.01,0.01)
#lefty = int((-x*vy/vx) + y)
#righty = int(((cols-x)*vy/vx)+y)
#cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)

# HULL
#hull = cv2.convexHull(cntrs)
#cv2.drawContours(img, [hull], -1, (0,255,0),2)

# FILE WRITING
#f = open('imgdata.txt', 'w')
#for i in range((edges.size/edges[0].size)):
#	for j in range(edges[0].size):
#		if edges[i][j] > 0:
#			f.write('1')
#		else:
#			f.write('0')
#	f.write('\n')
#f.close()

# SHOW IMAGE
# cv2.imshow('image',img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()