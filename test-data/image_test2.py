import cv2
import numpy as np
import sys
import imutils

color = sys.argv[1]               # COLOR (red, yellow, blue)
color_span = int(sys.argv[2])   # SPAN OF COLOR
image_to_load = sys.argv[3]     # IMAGE TO LOAD

# Return hue for given color
def getHue(rgb, color_span):
    hsv_color = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    hue = hsv_color[0][0][0]
    # print ("Hue: " + str(hue) + ", Color span: " + str(color_span))
    if hue >= color_span:
        lower_hue = hue - color_span
        upper_hue = hue + color_span
        # print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
    else:
        lower_hue = hue
        upper_hue = hue
        # print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
    hue_return = [lower_hue, upper_hue]
    return hue_return

# Return angle for points
def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

# Open file
def openFile(file):
    image = cv2.imread(image_to_load)
    if image is None:
        print ("No image readed")
        exit()
    return image

# get RGB for color mane
def getRGB(color):
    rgb = np.uint8([[[0,0,0]]])
    if(color == "red"):
        rgb = np.uint8([[[0,0,255]]])

    if(color == "yellow"):
        rgb = np.uint8([[[0,255,255]]])

    if(color == "blue"):
        rgb = np.uint8([[[255,0,0]]])
    return rgb

# Return shape in given color
def findShapeInColor(frame, color, color_span):
    orderedJoints = []
    hue = getHue(getRGB(color), color_span)
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([hue[0], 100, 100], dtype=np.uint8)
    upper_color = np.array([hue[1], 255, 255], dtype=np.uint8)
    mask = cv2.inRange(image_hsv, lower_color, upper_color)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    mask = cv2.GaussianBlur(mask, (3,3),0)

    cv2.imwrite("hsv.jpg", image_hsv)
    cv2.imwrite("res.jpg", res)
    cv2.imwrite("mask.jpg", mask)

    _, thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.04*cv2.arcLength(cnt,True),True)
        if cv2.contourArea(cnt) < 140:
		continue
        if len(approx)==5:
            # print "pentagon"
            orderedJoints.insert(0, [cnt])
        elif len(approx)==3:
            # print "triangle"
            orderedJoints.insert(0, [cnt])
        elif len(approx)==4:
            # print "square"
            orderedJoints.insert(1, [cnt])
        elif len(approx) >= 7:
            # print "circle"
            orderedJoints.insert(2, [cnt])

    # print len(orderedJoints)
    return orderedJoints

frame = openFile(image_to_load)
hand = findShapeInColor(frame, "red", color_span)
leg = findShapeInColor(frame, "yellow", color_span)
foot = findShapeInColor(frame, "blue", color_span)

for c in hand:
    cv2.drawContours(frame,c,0,(0,255,0),2)
for c in leg:
    cv2.drawContours(frame,c,0,(0,255,0),2)
for c in foot:
    cv2.drawContours(frame,c,0,(0,255,0),2)

cv2.imwrite("out.jpg", frame)
