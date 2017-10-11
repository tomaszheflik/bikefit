import cv2 as cv
import numpy as nu

# Read test file
image = cv2.imread("tri-bike-test.jpg")

# Convert to HSV color range
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define red color of red in HSV
higher_red = nu.array([0,0,255], dtype=nu.uint8)
lower_red = nu.array([20,20,190], dtype=nu.uint8)

# Threshold image to get only red colr
mask = cv.inRange(hsv, lower_red, higher_red)

# Mask original image
res = cv.bitwise_and(image, image, mask=mask)

cv.imwrite('out.jpg')
