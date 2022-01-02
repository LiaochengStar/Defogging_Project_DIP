import cv2 as cv

img = cv.imread("../../images/square_fog.jpg", -1)
B, G, R = cv.split(img)  # get single 8-bits channel
EB = cv.equalizeHist(B)
EG = cv.equalizeHist(G)
ER = cv.equalizeHist(R)
equal_img = cv.merge((EB, EG, ER))  # merge it back
cv.imshow("img", img)
cv.imshow("equal_img", equal_img)
cv.waitKey()

