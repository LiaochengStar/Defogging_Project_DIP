
import cv2
import math
import numpy as np

def DarkChannel(img, sz):
    b, g, r = cv2.split(img)
    dc = cv2.min(cv2.min(r, g), b)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))
    dark = cv2.erode(dc, kernel)
    return dark


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


def TransmissionEstimate(img, A, sz):
    omega = 0.95
    im3 = np.empty(img.shape, img.dtype)

    for ind in range(0, 3):
        im3[:, :, ind] = img[:, :, ind] / A[0, ind]

    transmission = 1 - omega * DarkChannel(im3, sz);
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
    I = src.astype('float64') / 255
    dark = DarkChannel(I, 15)
    A = AtmLight(I, dark)
    te = TransmissionEstimate(I, A, 15)
    t = TransmissionRefine(src, te)
    J = Recover(I, t, A, 0.1)

    cv2.imshow("dark", dark)
    cv2.imshow("t", t)
    cv2.imshow('I', src)
    cv2.imshow('J', J)
    cv2.waitKey()
