import scipy
import quantizeRGB
import quantizeHSV
import matplotlib.pyplot as plt


img = scipy.misc.imread('fish.jpg')
res, centroid = quantizeHSV.quantizeHSV(img, 7)
plt.imshow(res)
plt.show()
print(centroid)