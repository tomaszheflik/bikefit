import cv2 as cv
import numpy as np
import sys

red = sys.argv[1]
green = sys.argv[2]
blue = sys.argv[3]
color_span = int(sys.argv[4])
image_to_load = sys.argv[5]

color = np.uint8([[[blue, green, red]]])
hsv_color = cv.cvtColor(color, cv.COLOR_BGR2HSV)
hue = hsv_color[0][0][0]
print ("Hue: " + str(hue) + ", Color span: " + str(color_span))

if hue >= color_span:
    lower_hue = hue - color_span
    upper_hue = hue + color_span
    print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
else:
    lower_hue = hue
    upper_hue = hue
    print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))

image = cv.imread(image_to_load)
if image is None:
    print ("No image readed")
    exit()

image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
lower_color = np.array([lower_hue, 100, 100], dtype=np.uint8)
upper_color = np.array([upper_hue, 255, 255], dtype=np.uint8)
mask = cv.inRange(image_hsv, lower_color, upper_color)

res = cv.bitwise_and(image, image, mask=mask)

cv.imwrite("out.jpg", res)
cv.imwrite("hsv.jpg", image_hsv)
cv.imwrite("mask.jpg", mask)
