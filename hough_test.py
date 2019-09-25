import scipy.misc
import detectCircles
import matplotlib.pyplot as plt
import smaller_hough

im = scipy.misc.imread('egg.jpg')
radius = 15
use_gradient = 1
centers = detectCircles.detectCircles(im, radius, use_gradient)
print('detect' + str(len(centers)) + ' centers')
xs = []
ys = []
for center in centers:
    xs.append(center[0])
    ys.append(center[1])
plt.imshow(im)
plt.scatter(ys, xs, s=radius**2,c='r')
plt.title('Image with detected circle - use gradient = '+str(use_gradient)+" radius = "+str(radius))
plt.show()



im = scipy.misc.imread('jupiter.jpg')
radius = 50
centers = smaller_hough.detectCircles(im, radius)
xs = []
ys = []
for center in centers:
    xs.append(center[0])
    ys.append(center[1])
plt.imshow(im)
plt.scatter(ys, xs, s=radius**2,c='r')
plt.title('Image with detected circle - use gradient = '+str(use_gradient)+" radius = "+str(radius))
plt.show()