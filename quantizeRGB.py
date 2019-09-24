import scipy.cluster.vq
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt

def quantizeRGB(origImg, k):
    h,w,d = origImg.shape
    processed = np.reshape(origImg, (w*h, d))
    processed = np.array(processed, dtype=np.float64)
    centroid, labels = scipy.cluster.vq.kmeans2(processed, k)
    for i in range(h*w):
        processed[i] = centroid[labels[i]]
    res = np.reshape(processed, (h,w,d))
    res = res.astype(np.uint8)
    return res, centroid

