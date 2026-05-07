import cv2
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import re
import numpy as np
from func_timeout import func_set_timeout
import time
import matplotlib.pyplot as plt

class CvWechatDetector():
    def __init__(self, path_to_model="D:/app_24/stone_detection/stone_detection/common/"):
        super().__init__()
        self.detector = cv2.wechat_qrcode.WeChatQRCode(path_to_model + "detect.prototxt",
                                                       path_to_model + "detect.caffemodel",
                                                       path_to_model + "sr.prototxt",
                                                       path_to_model + "sr.caffemodel")

    def detect(self, image):
        decoded_info, corners = self.detector.detectAndDecode(image)
        if len(decoded_info) == 0:
            return False, np.array([])
        corners = np.array(corners).reshape(-1, 4, 2)
        self.decoded_info = decoded_info
        self.detected_corners = corners
        return True, corners

    def decode(self, image):
        if len(self.decoded_info) == 0:
            return 0, [], None
        return True, self.decoded_info, self.detected_corners

@func_set_timeout(25) # 设定函数执行时间
def qr_reader(img):
    merge_res = img.copy()
    # merge_res = cv2.cvtColor(merge_res, cv2.COLOR_GRAY2BGR)
    # 第一行的像素
    row_0 = img[0, ...]
    # 最后一行
    row_l = img[-1, ...]
    h, w = img.shape
    row = np.zeros_like(row_0)
    for i in range(w):
        row[i] = max(row_0[i], row_l[i])
    # 拼接出背景
    background = np.tile(row, h).reshape(-1, w)
    print(background.shape)

    res = cv2.subtract(img, background)

    # plt.imshow(res, 'gray')
    # plt.show()

    kernel = np.ones((5, 5), np.float32) / 25
    gray = cv2.filter2D(res, -1, kernel)
    # 高斯模糊
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # 二值化
    ret, threshold = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    threshold = cv2.dilate(threshold, kernel=np.ones((3, 3), dtype=np.uint8), iterations=10)
    # plt.imshow(threshold, 'gray')
    # plt.show()

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 不合并
    max_area = 0
    for c in contours:
        # 忽略次要轮廓
        if cv2.contourArea(c) < 15000:
            continue
        if cv2.contourArea(c) > max_area:
            max_c = c
            max_area = cv2.contourArea(c)

    # 合并轮廓
    merge_list = []
    for cnt in contours:
        if cv2.contourArea(cnt) < 100:
            # print(cv2.contourArea(cnt))
            continue
        # print(cv2.contourArea(cnt))
        merge_list.append(cnt)
    if len(merge_list) >= 2:
        contours_merge = np.vstack([merge_list[0], merge_list[1]])
        for i in range(2, len(merge_list)):
            contours_merge = np.vstack([contours_merge, merge_list[i]])
    else:
        contours_merge = merge_list[0]

    # 通过最小外接矩形获取角度
    rect = cv2.minAreaRect(contours_merge)
    print(rect[2])
    # input()

    # 外接矩形
    x, y, w, h = cv2.boundingRect(contours_merge)
    hh = 1500
    # cv2.rectangle(merge_res, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # 石板区域
    roi = merge_res[y: y + h, x: x + w]
    # plt.imshow(roi[..., ::-1])
    # plt.show()
    # 二值化石板
    _, roi_thr = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY)
    # plt.imshow(roi_thr, 'gray')
    # plt.show()
    qr_wechat = CvWechatDetector()
    height, width = roi.shape[:2]

    # 先测四个角
    # 左上
    region = roi_thr[:min(hh, height), :min(hh, width)]

    wechat_ret, wechat_corners = qr_wechat.detect(region)
    print('res:', wechat_ret, wechat_corners)
    if wechat_ret:
        info = qr_wechat.decode(region)
        print('wechat: ', info)
        return (True, info)

    #
    # 右上
    region = roi_thr[:min(hh, height), max(0, width - hh):width]
    # plt.imshow(region, 'gray')
    # plt.show()
    wechat_ret, wechat_corners = qr_wechat.detect(region)
    print('res:', wechat_ret, wechat_corners)
    if wechat_ret:
        info = qr_wechat.decode(region)
        print('wechat: ', info)
        return (True, info)

    #
    # 左下
    region = roi_thr[max(0, height - hh):height, :min(hh, width)]
    wechat_ret, wechat_corners = qr_wechat.detect(region)
    print('res:', wechat_ret, wechat_corners)
    if wechat_ret:
        info = qr_wechat.decode(region)
        print('wechat: ', info)
        return (True, info)

    #
    # 右下
    region = roi_thr[max(0, height - hh):height, max(0, width - hh):width]
    wechat_ret, wechat_corners = qr_wechat.detect(region)
    print('res:', wechat_ret, wechat_corners)
    if wechat_ret:
        info = qr_wechat.decode(region)
        print('wechat: ', info)
        return (True, info)


    # 四角没检出
    roi = merge_res[y: y + h + hh, x: x + w + hh]
    # 二值化石板
    _, roi_thr = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY)
    height, width = roi.shape[:2]

    exit_flag = False
    for delta in range(0, 400, 100):
        if exit_flag:
            break
        for h in range(height // hh):
            if exit_flag:
                break
            for w in range(width // hh):
                if delta + (h + 1) * hh >= height or delta + (w + 1) * hh >= width:
                    break
                region = roi_thr[delta + h * hh: delta + (h + 1) * hh, delta + w * hh: delta + (w + 1) * hh]
                # plt.imshow(region, 'gray')
                # plt.show()
                wechat_ret, wechat_corners = qr_wechat.detect(region)
                print('res:', wechat_ret, wechat_corners)
                if wechat_ret:
                    info = qr_wechat.decode(region)
                    print('wechat: ', info)
                    exit_flag = True
                    return (True, info)
    return (False,)


def get_qr_info(data):
    s_t = time.time()
    dimension = []
    if data == 0:
        return [(-1, -1)]
    else:
        for i in range(5):
            if len(dimension) == 0:
                edge_options = Options()
                prefs = {
                    'profile.default_content_setting_values': {
                        'images': 2,
                    }
                }
                edge_options.add_experimental_option('prefs', prefs)
                edge_options.add_argument("--headless")
                driver = webdriver.Edge(options=edge_options)

                driver.get(data)
                sleep(0.5)
                # 获取当前页的句柄
                main_windows = driver.current_window_handle
                # 获取所有打开的句柄
                all_windows = driver.window_handles
                # 循环获取到的句柄，如果不等于当前页的句柄则切换到此句柄，因为页面进行跳转，但是句柄仍停留在第一页，所以切换到新页句柄进行操作
                for handle in all_windows:
                    print(len(all_windows))
                    if handle != main_windows:
                        print(123)
                        driver.switch_to.window(handle)

                # print(driver.title)
                title = driver.title
                pageSource = driver.page_source
                print(str(pageSource))
                # ex = '<span>(\d+(?:\.\d+)?)\*(\d+(?:\.\d+)?)㎜<\/span>'
                ex = r">(\S+)\*(\S+)㎜<"
                dimension = re.findall(ex, str(pageSource), re.S)
                print(dimension)

                driver.close()
                if len(dimension) != 0:
                    ex = r">(\S+)</label>"
                    # 所属项目
                    xm = re.findall(ex, str(pageSource), re.S)[1]
                    print(xm)
                    print(time.time() - s_t)
                    return [title, dimension, xm]
        return [(-1, -1)]


if __name__ == '__main__':
    # import xlrd
    # from xlutils.copy import copy
    # import os
    # def write2excel(msg, path, col):
    #     file = xlrd.open_workbook(path)
    #     excel = copy(wb=file)
    #     excel_table = excel.get_sheet(0)
    #     table = file.sheets()[0]
    #     nrows = table.nrows
    #     ncols = table.ncols
    #     # print(nrows, ncols)
    #     for i in range(col):
    #         excel_table.write(nrows, i, msg[i])
    #     excel.save(path)
    # root = r"E:\Deep_Learning\stone\qr_bug"
    # img_list = os.listdir(root)
    # for n in img_list:
    #     img_path = root + '/' + n
    #     img = cv2.imread(img_path, 0)
    #     data = qr_reader(img)
    #     print(data)
    #     # 提取到了网址
    #     if data[0]:
    #         # 可能解析不出网址
    #         try:
    #             print(data[1][1][0])
    #             res = get_qr_info(data[1][1][0])
    #             print(res)
    #             title = res[0]
    #             size = res[1][0]
    #             print(title, size)
    #             size1 = float(size[0])
    #             size2 = float(size[1])
    #             # print(f'max:{max(size1, size2)}, min:{min(size1, size2)}')
    #             size1, size2 = max(size1, size2), min(size1, size2)
    #             # input()
    #             msg = [n, title, size1, size2]
    #             write2excel(msg, r"C:\Users\陈思遥\Desktop\results2.xls", 4)
    #         except:
    #             write2excel([n, 'null', 'null', 'null'], r"C:\Users\陈思遥\Desktop\results2.xls", 4)
    #     else:
    #         write2excel([n, 'null', 'null', 'null'], r"C:\Users\陈思遥\Desktop\results2.xls", 4)

    # img_path = r'D:\tmp\2023-10-18_16-06-22.bmp'
    # img = cv2.imread(img_path, 0)
    # data = qr_reader(img)
    data = 'https://webapp.fab-cloud.com/lts/a?b=1701961315342929985&bt=4'
    res = get_qr_info(data)
    print(res)

