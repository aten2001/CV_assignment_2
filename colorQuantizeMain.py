import scipy
import quantizeRGB
import quantizeHSV
import matplotlib.pyplot as plt
import computeQuantizationError

img = scipy.misc.imread('fish.jpg')

# Begin test k=3
for k in [3, 6, 15]:
    rgb_quantized_img, rgb_centroids = quantizeRGB.quantizeRGB(img, k)
    hsv_quantized_img, hsv_centroids = quantizeHSV.quantizeHSV(img, k)
    plt.imshow(rgb_quantized_img)
    plt.title('RGB quantized image with k = ' + str(k))
    plt.show()
    plt.imshow(hsv_quantized_img)
    plt.title('HSV quantized image with k = ' + str(k))
    plt.show()

    rgb_error = computeQuantizationError.computeQuantizationError(img, rgb_quantized_img)
    hsv_error = computeQuantizationError.computeQuantizationError(img, hsv_quantized_img)
    print('RGB SSD error with k = ', str(k), ' : ', str(rgb_error))
    print('HSV SSD error with k = ', str(k), ' : ', str(hsv_error))
