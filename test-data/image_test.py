import cv2 as cv
import numpy as np

image = cv.imread("tri-bike-test-01.jpg")
if image is None:
    print ("No image readed")
    exit()
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)


# lower mask (0-10)
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
mask0 = cv.inRange(hsv, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
mask1 = cv.inRange(hsv, lower_red, upper_red)

# join my masks
mask = mask0+mask1

res = cv.bitwise_and(image, image, mask, mask)

cv.imwrite("out.jpg", res)
