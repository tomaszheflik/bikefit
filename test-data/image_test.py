import cv2
import numpy as np
import sys

red = sys.argv[1]               # RED COLOE
green = sys.argv[2]             # GREEN COLOR
blue = sys.argv[3]              # BLUE COLOR
color_span = int(sys.argv[4])   # SPAN OF COLOR
image_to_load = sys.argv[5]     # IMAGE TO LOAD

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

image = cv2.imread(image_to_load)
if image is None:
    print ("No image readed")
    exit()
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_color = np.array([lower_hue, 100, 100], dtype=np.uint8)
upper_color = np.array([upper_hue, 255, 255], dtype=np.uint8)
mask = cv2.inRange(image_hsv, lower_color, upper_color)
res = cv2.bitwise_and(image, image, mask=mask)

# find circles and mark them
#res = cv2.medianBlur(res, 11)
res = cv2.GaussianBlur(res, (19,19),0)


cimg = cv2.cvtColor(res,cv2.COLOR_RGB2GRAY)
# cimg1 = cv2.cvtColor(cimg,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,15,param1=50,param2=18,minRadius=5,maxRadius=10)
circles = np.uint16(np.around(circles))
iter = 0
for i in circles[0,:]:
        iter=iter+1
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle
        cv2.circle(image,(i[0],i[1]),2,(0,0,255),2) # draw the center of the circle
        cv2.putText(image,str(iter), (i[0]+i[2],i[1]+i[2]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,255,255))


cv2.imwrite("out.jpg", res)
cv2.imwrite("hsv.jpg", image_hsv)
cv2.imwrite("mask.jpg", mask)
cv2.imwrite("circle.jpg", image)
