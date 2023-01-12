
import cv2
import cv2 as cv
import numpy as np
from imutils import perspective
from scipy.spatial import distance as dist


def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5


def cnt_area(cnt):
    area = cv2.contourArea(cnt)
    return area


class MeasurementThread:
    diameter = 7.6

    def __init__(self):

        self.cv = cv

    def show_sludge_height(self, image):
        roiImg = image
        # cv2.imwrite("D:/test/" + "%d.jpg" % self.time, image)

        garryImg = self.cv.cvtColor(roiImg, cv.COLOR_BGR2GRAY)
        garryImg = self.cv.cvtColor(garryImg, cv.COLOR_GRAY2BGR)

        garryImg = self.cv.GaussianBlur(garryImg, (3, 3), 0)

        ret, thresh = self.cv.threshold(garryImg, 60, 255, cv2.THRESH_BINARY)

        thresh = self.cv.dilate(thresh, None, iterations=11)
        thresh = self.cv.erode(thresh, None, iterations=10)

        edged = self.cv.Canny(thresh, 70, 100)

        contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cnt_area, reverse=False)

        i, dimA = 0, 0
        for contour in contours:
            if 900 < self.cv.contourArea(contour):

                i += 1

                # 计算轮廓选择框
                orig = garryImg.copy()

                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                box = np.array(box)

                box = perspective.order_points(box)

                cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

                for (x, y) in box:
                    cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

                    (tl, tr, br, bl) = box
                    (tltrX, tltrY) = midpoint(tl, tr)
                    (blbrX, blbrY) = midpoint(bl, br)

                    (tlblX, tlblY) = midpoint(tl, bl)
                    (trbrX, trbrY) = midpoint(tr, br)

                    # 计算中点间的欧氏距离
                    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                    pixelsPerMetric = dB / MeasurementThread.diameter
                    # 计算物体大小
                    dimA = dA / pixelsPerMetric
        # import datetime
        # print(datetime.datetime.now(), dimA)
        # images_path = 'D:/test/{path}.jpg'.format(path=datetime.datetime.now().strftime("%S_%f"))
        # cv2.imwrite(images_path, image)
        return dimA
