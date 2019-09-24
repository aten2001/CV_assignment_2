import numpy as np
import skimage.feature
import skimage.color
import matplotlib.pyplot as plt
import scipy.misc

min_distance_between_centers = 10
theta_pace_detect_offset = 80
threshold_no_gradient = 30
theta_pace_draw = 100
def detectCircles(im, radius, useGradient):
    edge = skimage.feature.canny(skimage.color.rgb2gray(im), sigma=3)
    h, w, _ = im.shape
    acc = dict()
    acc_mat = np.zeros((h, w))
    pace = int(radius * 0.5) + theta_pace_detect_offset
    if useGradient == 0:
        threshold = threshold_no_gradient
        for i in range(h):
            for j in range(w):
                if edge[i, j]:
                    for div in range(pace):
                        theta = 2 * np.pi * div / pace
                        a = int(-radius * np.cos(theta) + i)
                        b = int(radius * np.sin(theta) + j)
                        if isValid(h, w, a, b):
                            acc[(a, b)] = acc.get((a, b), 0) + 1
                            acc_mat[a, b] += 1
    if useGradient == 1:
        threshold = 4
        gradient_map = np.gradient(skimage.color.rgb2gray(im))
        theta_map = np.arctan(gradient_map[1]/gradient_map[0])
        for i in range(h):
            for j in range(w):
                if edge[i, j]:
                    theta = theta_map[i,j]
                    if not theta == theta:
                        theta = np.pi/2
                    a = int(-radius * np.cos(theta) + i)
                    b = int(radius * np.sin(theta) + j)
                    if isValid(h, w, a, b):
                        acc[(a, b)] = acc.get((a, b), 0) + 1
                        acc_mat[a, b] += 1


    # Getting centers of the circle + post-processing
    print(np.max(acc_mat))
    plt.imshow(acc_mat, cmap='gray')
    plt.show()
    acc_sorted = sorted(acc.items(), key=lambda kv: kv[1], reverse=True)
    qualified_center = set()
    for k, v in acc_sorted:
        if v < threshold:
            break
        else:
            if not_close_center(k, qualified_center):
                qualified_center.add(k)

    # For constructing binary image with circle on it
    new_img = np.zeros((h, w), dtype=np.uint8)
    for center in qualified_center:
        for theta_div in range(theta_pace_draw):
            theta = 2 * np.pi * theta_div / theta_pace_draw
            i = int(radius * np.cos(theta) + center[0])
            j = int(radius * np.sin(theta) + center[1])
            if isValid(h, w, i, j):
                new_img[i, j] = 255
    return new_img


def not_close_center(pos, set):
    for s in set:
        if (pos[0] - s[0]) ** 2 + (pos[1] - s[1]) ** 2 <= min_distance_between_centers ** 2:
            return False
    return True


def isValid(h, w, a, b):
    if a < 0 or a >= h:
        return False
    if b < 0 or b >= w:
        return False
    return True


im = scipy.misc.imread('egg.jpg')
plt.imshow(im)
plt.show()
plt.imshow(detectCircles(im, 4, 0), cmap='gray')
plt.show()
