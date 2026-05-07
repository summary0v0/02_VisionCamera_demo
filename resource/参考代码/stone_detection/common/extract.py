import cv2
import numpy as np

# 输入灰度图
def extract_func(img):
    # 第一行的像素
    row_0 = img[0, ...]
    # 最后一行
    row_l = img[-1, ...]
    h, w = img.shape[: 2]
    row = np.zeros_like(row_0)
    for i in range(w):
        row[i] = max(row_0[i], row_l[i])
    # 拼接出背景
    background = np.tile(row, h).reshape(-1, w)
    print(background.shape)

    res = cv2.subtract(img, background)
    return res

if __name__ == '__main__':
    img = cv2.imread(r"D:\tmp\2023-10-18_12-35-15.bmp", 0)
    res = extract_func(img)
