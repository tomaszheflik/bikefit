import cv2
import numpy as np
import sys

red = sys.argv[1]
green = sys.argv[2]
blue = sys.argv[3]
color_span = int(sys.argv[4])
image_to_load = sys.argv[5]

color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
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

image_r = cv2.imread(image_to_load)
if image_r is None:
    print ("No image readed")
    exit()
image = cv2.medianBlur(image_r, 3)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_color = np.array([lower_hue, 100, 100], dtype=np.uint8)
upper_color = np.array([upper_hue, 255, 255], dtype=np.uint8)
mask = cv2.inRange(image_hsv, lower_color, upper_color)
res = cv2.bitwise_and(image, image, mask=mask)

cv2.imwrite("out.jpg", res)
cv2.imwrite("hsv.jpg", image_hsv)
cv2.imwrite("mask.jpg", mask)
