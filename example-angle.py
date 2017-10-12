import cv
import math


class Target:
    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow(“Target”, 1)
        cv.NamedWindow(“Threshold1”, 1)
        cv.NamedWindow(“Threshold2”, 1)
        cv.NamedWindow(“hsv”, 1)

    def run(self):
        # initiate font
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
        # instantiate images
        hsv_img = cv.CreateImage(cv.GetSize(cv.QueryFrame(self.capture)), 8, 3)
        threshold_img1 = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        threshold_img1a = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        threshold_img2 = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        i = 0
        writer = cv.CreateVideoWriter(“angle_tracking.avi”, cv.CV_FOURCC(‘M’, ’J’, ’P’, ’G’), 30, cv.GetSize(hsv_img), 1)

        while True:
            # capture the image from the cam
            img = cv.QueryFrame(self.capture)
            # convert the image to HSV
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)
            # threshold the image to isolate two colors
            cv.InRangeS(hsv_img, (165, 145, 100),
                        (250, 210, 160), threshold_img1)  # red
            cv.InRangeS(hsv_img, (0, 145, 100), (10, 210, 160),
                        threshold_img1a)  # red again
            # this is combining the two limits for red
            cv.Add(threshold_img1, threshold_img1a, threshold_img1)
            cv.InRangeS(hsv_img, (105, 180, 40),
                        (120, 260, 100), threshold_img2)  # blue
            # determine the moments of the two objects
            threshold_img1 = cv.GetMat(threshold_img1)
            threshold_img2 = cv.GetMat(threshold_img2)
            moments1 = cv.Moments(threshold_img1, 0)
            moments2 = cv.Moments(threshold_img2, 0)
            area1 = cv.GetCentralMoment(moments1, 0, 0)
            area2 = cv.GetCentralMoment(moments2, 0, 0)

            # initialize x and y
            x1, y1, x2, y2 = (1, 2, 3, 4)
            coord_list = [x1, y1, x2, y2]
            for x in coord_list:
                x = 0

                # there can be noise in the video so ignore objects with small areas
                if (area1 > 200000):
                    # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                    x1 = int(cv.GetSpatialMoment(moments1, 1, 0) / area1)
                    y1 = int(cv.GetSpatialMoment(moments1, 0, 1) / area1)
                    # draw circle
                    cv.Circle(img, (x1, y1), 2, (0, 255, 0), 20)
                    # write x and y position
                    # Draw the text
                    cv.PutText(img, str(x1) +”, ”+str(y1), (x1, y1 + 20), font, 255)
                if (area2 > 100000):
                    # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                    x2 = int(cv.GetSpatialMoment(moments2, 1, 0) / area2)
                    y2 = int(cv.GetSpatialMoment(moments2, 0, 1) / area2)
                    # draw circle
                    cv.Circle(img, (x2, y2), 2, (0, 255, 0), 20)
                    # Draw the text
                    cv.PutText(img, str(x2) +”, ”+str(y2), (x2, y2 + 20), font, 255)
                    cv.Line(img, (x1, y1), (x2, y2), (0, 255, 0), 4, cv.CV_AA)
                    # draw line and angle
                    cv.Line(img, (x1, y1), (cv.GetSize(img)[
                            0], y1), (100, 100, 100, 100), 4, cv.CV_AA)
                    x1 = float(x1)
                    y1 = float(y1)
                    x2 = float(x2)
                    y2 = float(y2)
                    angle = int(math.atan((y1 - y2) / (x2 - x1))
                                * 180 / math.pi)
                    cv.PutText(img, str(angle), (int(x1) + 50,
                                                 (int(y2) + int(y1)) / 2), font, 255)
                    # cv.WriteFrame(writer,img)
                    # display frames to users
                    cv.ShowImage(“Target”, img)
                    cv.ShowImage(“Threshold1”, threshold_img1)
                    cv.ShowImage(“Threshold2”, threshold_img2)
                    cv.ShowImage(“hsv”, hsv_img)

            # Listen for ESC or ENTER key
            c = cv.WaitKey(7) % 0x100
            if c == 27 or c == 10:
                break
        cv.DestroyAllWindows()

if __name__ ==”__main__”:
    t = Target()
    t.run()
