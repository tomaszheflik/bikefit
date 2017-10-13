import cv2
import numpy as np
import sys
import imutils
import datetime

image_to_load = sys.argv[1]     # IMAGE TO LOAD
DEBUG = False
# Return hue for given color
def getHue(rgb, color_span):
    hsv_color = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    hue = hsv_color[0][0][0]
    if DEBUG: print ("Hue: " + str(hue) + ", Color span: " + str(color_span))
    if hue >= color_span:
        lower_hue = hue - color_span
        upper_hue = hue + color_span
        if DEBUG: print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
    elif(hue == 0):
        lower_hue = 0
        upper_hue = color_span
        if DEBUG: print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
    else:
        lower_hue = hue
        upper_hue = hue
        if DEBUG: print ("Lower Hue: " + str(lower_hue) + ", Upper Hue: " + str(upper_hue))
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
    if(color == "green"):
        rgb = np.uint8([[[0,255,0]]])
    return rgb

# Return shape in given color
def findShapeInColor(frame, color, color_span):
    t1 = datetime.datetime.now()
    tmpJoints = {}
    orderedJoints = []

    hue = getHue(getRGB(color), color_span)
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([hue[0], 100, 100], dtype=np.uint8)
    upper_color = np.array([hue[1], 255, 255], dtype=np.uint8)
    mask = cv2.inRange(image_hsv, lower_color, upper_color)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    mask = cv2.GaussianBlur(mask, (1,1),0)

    cv2.imwrite("hsv.jpg", image_hsv)
    # cv2.imwrite("res.jpg", res)
    cv2.imwrite("mask.jpg", mask)

    _, thresh = cv2.threshold(mask.copy(),127,255,cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
        if DEBUG:
            cv2.drawContours(res,[cnt],0,(0,165,255),1)
            cv2.imwrite("res.jpg", res)
        if cv2.contourArea(cnt) < 70 or cv2.contourArea(cnt) > 180:
            if DEBUG: print("Skipping area:" + str(cv2.contourArea(cnt))+ "Approx: " + str(len(approx)))
            continue

        if len(approx)==5:
            if DEBUG: print("pentagon " + str(len(approx)))
            tmpJoints['circle'] = cnt
        elif len(approx)==3:
            if DEBUG: print("triangle " + str(len(approx)))
            tmpJoints['triangle'] = cnt
        elif len(approx)==4:
            if DEBUG: print("square " + str(len(approx)))
            tmpJoints['square'] = cnt
        elif len(approx) >= 7:
            if DEBUG: print("circle " + str(len(approx)))
            tmpJoints['circle'] = cnt

    if 'triangle' in tmpJoints: orderedJoints.append(tmpJoints['triangle'])
    if 'circle' in tmpJoints: orderedJoints.append(tmpJoints['circle'])
    if 'square' in tmpJoints: orderedJoints.append(tmpJoints['square'])
    t2 = datetime.datetime.now()
    timeMetric = t2 - t1
    print("Video.Frame.Time."+ color + ": " + str(timeMetric))
    return orderedJoints

#
# MAIN STARY
#

# Load sinble frame
frame = openFile(image_to_load)

# Get body componennt by color and build skeleton
body = []
joints = []
for item in findShapeInColor(frame, "green", 4): body.append(item)
for item in findShapeInColor(frame, "yellow", 2): body.append(item)
for item in findShapeInColor(frame, "blue", 4): body.append(item)
if DEBUG: print body
for item in body:
    M = cv2.moments(item)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    joints.append([cx,cy])

# print joints
iter = 0
for joint in joints:
    if iter > 0:
        cv2.line(frame, (oldjoint[0],oldjoint[1]), (joint[0],joint[1]), (255,0,0),2)
    iter=iter+1
    cv2.circle(frame,(joint[0],joint[1]),10,(0,255,0),1) # draw the outer circle
    cv2.circle(frame,(joint[0],joint[1]),2,(0,0,255),2) # draw the center of the circle
    cv2.putText(frame,str(iter), (joint[0]+10,joint[1]+10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,255,255))
    oldjoint = joint
cv2.imwrite("image.jpg", frame)
