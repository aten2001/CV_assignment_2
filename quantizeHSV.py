import scipy.cluster.vq
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
import skimage.color
def quantizeHSV(origImg, k):
    origImg = skimage.color.rgb2hsv(origImg)
    h,w,d = origImg.shape
    processed = np.reshape(origImg, (w*h, d))
    processed = np.array(processed[:,0], dtype=np.float64)
    centroid, labels = scipy.cluster.vq.kmeans2(processed, k)
    for i in range(h*w):
        processed[i] = centroid[labels[i]]
    processed = np.reshape(processed, (h,w))
    res = np.zeros((h,w,d))
    for i in range(h):
        for j in range(w):
            res[i][j][0] = processed[i][j]
            res[i][j][1] = origImg[i][j][1]
            res[i][j][2] = origImg[i][j][2]

    res = skimage.color.hsv2rgb(res)
    return res, centroid