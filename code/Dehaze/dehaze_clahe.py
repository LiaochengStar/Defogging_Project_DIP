# -*- coding: utf-8  -*-
import cv2
image=cv2.imread("../../images/city_fog.png")
b,g,r = cv2.split(image)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
b = clahe.apply(b)
g = clahe.apply(g)
r = clahe.apply(r)
ima= cv2.merge([b,g,r])
cv2.imshow("Original Trawing",image)
cv2.imshow("CALHE",ima)
cv2.waitKey()
