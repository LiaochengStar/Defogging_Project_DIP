# -*- coding: utf-8  -*-
import cv2
img = cv2.imread("../../images/square_fog.jpg")
b, g, r = cv2.split(img)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
b = clahe.apply(b)
g = clahe.apply(g)
r = clahe.apply(r)
image= cv2.merge([b, g, r])
cv2.imshow("Original Trawing", img)
cv2.imshow("CALHE", image)
cv2.waitKey()
