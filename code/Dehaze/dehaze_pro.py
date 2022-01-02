import os

import cv2
import math
import numpy as np

def DarkChannel(img, sky_img, sz, t=4):

    h,w=sky_img.shape
    dc=np.zeros([h, w])
    for i in range(h):
        for j in range(w):
            b, g, r = img[i, j, :][0], img[i, j, :][1], img[i, j, :][2]
            if sky_img[i, j] == 1:
                dc[i, j]=t+min(b, g, r)*(1-t)
            else:
                dc[i, j]=min(b, g, r)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
    dark = cv2.erode(dc, kernel)
    return dark

def getSkyImg(process_image):
    imGray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(imGray, 20, 100)
    cv2.imshow("edges", edges)
    row, column = edges.shape
    sky_image = np.ones([row, column])
    scene_image = np.zeros([row, column])
    for c in range(column):
        line = edges[:, c].copy()
        line_ = edges[:, c].copy()
        temp = 0
        for i in range(row):
            if line[i] != 0:
                temp = 1
            if temp == 0:
                line[i] = 1
                line_[i] = 0
            else:
                line[i] = 0
                line_[i] = 1
            sky_image[:, c] = line
            scene_image[:, c] = line_
    return sky_image
def AtmLight(img, dark):
    [h, w] = img.shape[:2]
    imsz = h * w
    numpx = int(max(math.floor(imsz / 1000), 1))
    darkvec = dark.reshape(imsz)
    imvec = img.reshape(imsz, 3)

    indices = darkvec.argsort()
    indices = indices[imsz - numpx::]

    atmsum = np.zeros([1, 3])
    for ind in range(1, numpx):
        atmsum = atmsum + imvec[indices[ind]]

    A = atmsum / numpx
    return A


def TransmissionEstimate(img, A, sky_image, sz):
    omega = 0.95
    im3 = np.empty(img.shape, img.dtype)

    for ind in range(0, 3):
        im3[:, :, ind] = img[:, :, ind] / A[0, ind]

    transmission = 1 - omega * DarkChannel(im3, sky_image,sz)
    return transmission


def Guidedfilter(img, p, r, eps):
    mean_I = cv2.boxFilter(img, cv2.CV_64F, (r, r))
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    mean_Ip = cv2.boxFilter(img * p, cv2.CV_64F, (r, r))
    cov_Ip = mean_Ip - mean_I * mean_p

    mean_II = cv2.boxFilter(img * img, cv2.CV_64F, (r, r))
    var_I = mean_II - mean_I * mean_I

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))

    q = mean_a * img + mean_b
    return q


def TransmissionRefine(img, et):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float64(gray) / 255
    r = 60
    eps = 0.0001
    t = Guidedfilter(gray, et, r, eps)

    return t


def Recover(img, t, A, tx=0.1):
    res = np.empty(img.shape, img.dtype)
    t = cv2.max(t, tx)

    for ind in range(0, 3):
        res[:, :, ind] = (img[:, :, ind] - A[0, ind]) / t + A[0, ind]

    return res


if __name__ == '__main__':
    import sys

    try:
        fn = sys.argv[1]
    except:
        fn = '../../images/square_fog.jpg'
    def nothing(*argv):
        pass


    src = cv2.imread(fn)
    sky_image=getSkyImg(src)
    I = src.astype('float64') / 255
    dark = DarkChannel(I, sky_image, 15)
    A = AtmLight(I, dark)
    te = TransmissionEstimate(I, A, sky_image, 15)
    t = TransmissionRefine(src, te)
    J = Recover(I, t, A, 0.1)
    #
    cv2.imshow("dark", dark)
    cv2.imshow("t", t)
    cv2.imshow("sky", sky_image)
    cv2.imshow('I', src)
    cv2.imshow('J', J)
    cv2.waitKey()