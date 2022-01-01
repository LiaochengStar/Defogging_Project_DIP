import cv2 as cv
import numpy as np


test = cv.imread("../../images/city_fog.bmp", -1)

B, G, R = cv.split(test)  # get single 8-bits channel
EB = cv.equalizeHist(B)
EG = cv.equalizeHist(G)
ER = cv.equalizeHist(R)
equal_test = cv.merge((EB, EG, ER))  # merge it back
cv.imshow("test", test)
cv.imshow("equal_test", equal_test)
cv.waitKey()

