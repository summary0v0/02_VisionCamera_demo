import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.signal import argrelextrema
import matplotlib
import time
from imutils.contours import sort_contours
import imutils
matplotlib.use('TkAgg')


# contains lots of useful stuff that's also in OpenCV
# https://scipy.github.io/devdocs/ndimage.html


### "business logic" ###################################################

def process(image, th):
    # 图像预处理
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 模糊图像
    kernel = np.ones((5, 5), np.float32) / 25
    gray = cv2.filter2D(gray, -1, kernel)
    # 高斯模糊
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # 二值化
    ret, threshold = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
    # 用canny对二值图像进行边缘检测
    # edged = cv2.Canny(threshold, 0, 1.2 * ret)
    # plt.imshow(threshold, 'gray')
    # plt.show()
    return threshold

def init(image, th):
    edged = process(image, th)
    # roi区域

    return edged

def get_angle(img, th):
    edged = init(img, th)
    # 获取所有轮廓
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 只获取轮廓信息
    cnts = imutils.grab_contours(contours)
    # 轮廓排序
    (cnts, _) = sort_contours(cnts)

    l = []
    max_c = None
    max_area = 0
    for c in cnts:
        l.append(cv2.contourArea(c))
        # 忽略次要轮廓
        if cv2.contourArea(c) < 15000:
            continue
        if cv2.contourArea(c) > max_area:
            max_c = c
            max_area = cv2.contourArea(c)
    # 最小外接矩形
    rect = cv2.minAreaRect(max_c)
    print(rect[2])
    return rect[2]

def build_transform(p0, p1, stride=None, nsamples=None):
    "builds an affine transform with x+ along defined line"
    # use one of stride (in pixels) or nsamples (absolute value)

    (x0, y0) = p0
    (x1, y1) = p1

    dx = x1 - x0
    dy = y1 - y0

    length = np.hypot(dx, dy)

    if nsamples is not None:
        # stride = length / nsamples
        factor = 1 / nsamples

    else:
        if stride is None:
            stride = 1.0

        factor = stride / length
        nsamples = int(round(length / stride))

    # map: src <- dst (use WARP_INVERSE_MAP flag for warpAffine)
    H = np.eye(3, dtype=np.float64)  # homography

    H[0:2, 0] = (dx, dy)  # x unit vector
    H[0:2, 1] = (-dy, dx)  # y unit vector is x rotated by 90 degrees

    H[0:2, 0:2] *= factor

    H[0:2, 2] = (x0, y0)  # translate onto starting point

    # take affine part of homography
    assert np.isclose(a=H[2], b=(0, 0, 1)).all()  # we didn't touch those but let's better check
    A = H[0:2, :]

    return (nsamples, A)


def sample_opencv(im, M, nsamples):
    # use transform to get samples
    # available: INTER_{NEAREST,LINEAR,AREA,CUBIC,LANCOS4)
    samples = cv2.warpAffine(im, M=M, dsize=(nsamples, 1), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_CUBIC)

    # flatten row vector
    samples.shape = (-1,)

    # INTER_CUBIC seems to break down beyond 1/32 sampling (discretizes).
    # there might be fixed point algorithms at work

    return samples


def sample_scipy(im, M, nsamples):
    # coordinates to this function are (i,j) = (y,x)
    # I could permute first and second rows+columns of M, or transpose input+output
    Mp = M.copy()
    Mp[(0, 1), :] = Mp[(1, 0), :]  # permute rows
    Mp[:, (0, 1)] = Mp[:, (1, 0)]  # permute columns

    samples = scipy.ndimage.interpolation.affine_transform(
        input=im, matrix=Mp, output_shape=(1, nsamples),
        order=2,
        # 1: linear (C0, f' is piecewise constant), 2: C1 (f' is piecewise linear), 3: C2... https://en.wikipedia.org/wiki/Smoothness
        mode='nearest'  # border handling
    )

    # flatten row vector
    samples.shape = (-1,)

    return samples


### command line parsing utility functions #############################

def parse_linestr(arg):
    pieces = arg.split(",")
    pieces = [float(el) for el in pieces]
    x0, y0, x1, y1 = pieces
    return ((x0, y0), (x1, y1))


