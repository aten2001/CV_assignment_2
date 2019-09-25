import numpy as np
import skimage.feature
import skimage.color
import matplotlib.pyplot as plt
import scipy.misc

min_distance_between_centers = 10
theta_pace_detect_offset = 80
threshold_no_gradient = 25
threshold_gradient = 8
theta_pace_draw = 100


def detectCircles(im, radius, useGradient):
    edge = skimage.feature.canny(skimage.color.rgb2gray(im), sigma=3)
    plt.imshow(edge)
    plt.show()
    h, w, _ = im.shape
    acc = dict()
    acc_mat = np.zeros((h, w))
    pace = int(radius * 0.5) + theta_pace_detect_offset
    if useGradient == 0:
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
        gradient_map = np.gradient(skimage.color.rgb2gray(im))
        theta_map = np.arctan(-gradient_map[1]/gradient_map[0])
        for i in range(h):
            for j in range(w):
                if edge[i, j]:
                    theta = theta_map[i,j]
                    if not theta == theta:
                        theta = np.pi/2
                    a = int(-radius * np.cos(theta) + i)
                    b = int(radius * np.sin(theta) + j)
                    for augmented_a_b in augment_a_b(a,b):
                        a_aug = augmented_a_b[0]
                        b_aug = augmented_a_b[1]
                        if isValid(h, w, a_aug, b_aug):
                            acc[(a_aug, b_aug)] = acc.get((a_aug, b_aug), 0) + 1
                            acc_mat[a_aug, b_aug] += 1


    # Getting centers of the circle + post-processing
    threshold = np.max(acc_mat) * 0.9
    print(np.max(acc_mat))
    plt.imshow(acc_mat)
    plt.title('Accumulator - Use gradient = '+str(useGradient)+' Radius = '+str(radius))
    plt.show()
    acc_sorted = sorted(acc.items(), key=lambda kv: kv[1], reverse=True)
    qualified_center = []
    for k, v in acc_sorted:
        if v < threshold:
            break
        else:
            if not_close_center(k, qualified_center):
                qualified_center.append(k)

    return qualified_center


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

def augment_a_b(a,b):
    res = []
    augment = [[-1,-1],[-1,0],[-1,1],
               [0,-1],[0,0],[0,1],
               [1,-1],[1,0],[1,1]]
    for aug in augment:
        res.append((a+aug[0], b+aug[1]))
    return res

