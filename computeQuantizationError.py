import math


def computeQuantizationError(origImg, quantizedImg):
    h, w, d = origImg.shape
    sum = 0
    for i in range(h):
        for j in range(w):
            error = (origImg[i, j, 0] - quantizedImg[i, j, 0]) ** 2 + \
                    (origImg[i, j, 1] - quantizedImg[i, j, 1]) ** 2 + \
                    (origImg[i, j, 2] - quantizedImg[i, j, 2]) ** 2
            sum+=error
    return sum
