import numpy as np
import skimage.feature
import skimage.color
import matplotlib.pyplot as plt
import scipy.misc

theta_pace_detect_offset = 80
threshold_no_gradient = 0.8
small_factor = 5
min_distance_between_centers = 10 / small_factor


# Hough with smaller vote space
# Does not include use gradient option, be care
def detectCircles(im, radius):
    edge = skimage.feature.canny(skimage.color.rgb2gray(im), sigma=3)
    plt.imshow(edge)
    plt.show()
    h, w, _ = im.shape
    acc = dict()
    acc_mat = np.zeros((h // small_factor, w // small_factor))
    pace = int(radius * 0.5) + theta_pace_detect_offset
    for i in range(h):
        for j in range(w):
            if edge[i, j]:
                for div in range(pace):
                    theta = 2 * np.pi * div / pace
                    a = int((-radius * np.cos(theta) + i) / small_factor)
                    b = int((radius * np.sin(theta) + j) / small_factor)
                    if isValid(h, w, a, b):
                        acc[(a, b)] = acc.get((a, b), 0) + 1
                        acc_mat[a, b] += 1

    # Getting centers of the circle + post-processing
    threshold = np.max(acc_mat) * threshold_no_gradient
    print(np.max(acc_mat))
    plt.imshow(acc_mat)
    plt.title('Smaller vote space accumulator - Radius = ' + str(radius))
    plt.show()
    acc_sorted = sorted(acc.items(), key=lambda kv: kv[1], reverse=True)
    qualified_center = []
    for k, v in acc_sorted:
        if v < threshold:
            break
        else:
            if not_close_center(k, qualified_center):
                qualified_center.append((k[0] * small_factor, k[1] * small_factor))

    # For constructing binary image with circle on it
    return qualified_center


def not_close_center(pos, set):
    for s in set:
        if (pos[0] - s[0]) ** 2 + (pos[1] - s[1]) ** 2 <= min_distance_between_centers ** 2:
            return False
    return True


def isValid(h, w, a, b):
    if a < 0 or a >= h // small_factor:
        return False
    if b < 0 or b >= w // small_factor:
        return False
    return True
