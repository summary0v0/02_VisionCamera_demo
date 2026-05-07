import random

import cv2
import matplotlib.pyplot as plt
from math import sin, radians, cos
from common.caliper import *
import scipy.signal as signal
from common.extract import extract_func
matplotlib.use('TkAgg')

class WhiteProcess:
    def __init__(self):
        pass
    def process(self, im):
        st = time.time()
        # path = r"E:\Deep_Learning\stone\white\Image-0019.bmp"
        # img = cv2.imread(path, 1)
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        img = im
        img = img[:, 1500: 15000]
        # mtx = np.array([[3.30385899e+05, 0.00000000e+00, 6.75108680e+03],
        #                 [0.00000000e+00, 3.29783002e+05, 6.00653260e+03],
        #                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        # dist = np.array([[-6.22183991e+00, -6.82745891e-01, -6.41526812e-03,
        #                   -2.61660231e-02, -1.26170672e-04]])
        # img = cv2.undistort(img, mtx, dist, None, mtx)
        img_3 = cv2.resize(img.copy(), dsize=(0, 0), fx=0.1, fy=0.1)
        try:
            angle_1 = get_angle(img_3, th=47)
        except:
            return 1
        # angle_1 = 0
        # if angle_1 < 50:
        #     img = cv2.flip(img, 1)
        if angle_1 < 1 or (90 - angle_1) < 1:
            height, width = img.shape[:2]
            angle = 2
            center = (width / 2, height / 2)
            new_H = int(width * abs(sin(radians(angle))) + height * abs(cos(radians(angle))))
            new_W = int(height * abs(sin(radians(angle))) + width * abs(cos(radians(angle))))
            M = cv2.getRotationMatrix2D(center, angle, 1)
            M[0, 2] += (new_W - width) / 2
            M[1, 2] += (new_H - height) / 2
            img = cv2.warpAffine(img, M, dsize=(new_W, new_H), borderValue=0)
        edged = init(img, th=60)
        edged = cv2.erode(edged, kernel=np.ones((3, 3), dtype=np.uint8), iterations=10)
        edged = cv2.dilate(edged, kernel=np.ones((3, 3), dtype=np.uint8), iterations=10)
        image = img.copy()
        # plt.imshow(edged, 'gray')
        # plt.show()

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
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int_(box)

            (x, y), (w, h), angle = rect
        # print(l)
        x, y, w, h = cv2.boundingRect(max_c)
        # img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # 最小外接矩形
        rect = cv2.minAreaRect(max_c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print('box:', box)
        print('angle:', rect[2])
        cv2.polylines(image, [box], True, (0, 255, 50), 2)
        # plt.imshow(image[..., ::-1])
        # plt.show()
        if abs(rect[2] - 90) < 0.2 or abs(rect[2]) < 0.2:
            center = [int(pos) for pos in rect[0]]
            w, h = rect[1]
            print(h, w, center)
            cv2.line(image,
                     (center[0] - int(w / 2) - 100, center[1] + int(h * 5 / 12)),
                     (center[0] + int(w / 2) + 100, center[1] + int(h * 5 / 12)),
                     thickness=3,
                     color=[random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)])
            cv2.line(image,
                     (center[0] - int(w / 2) - 100, center[1] - int(h * 5 / 12)),
                     (center[0] + int(w / 2) + 100, center[1] - int(h * 5 / 12)),
                     thickness=3,
                     color=[random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)])
            cv2.line(image,
                     (center[0] - int(w * 5 / 12), center[1] + int(h / 2) + 100),
                     (center[0] - int(w * 5 / 12), center[1] - int(h / 2) - 100),
                     thickness=3,
                     color=[random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)])
            cv2.line(image,
                     (center[0] + int(w * 5 / 12), center[1] + int(h / 2) + 100),
                     (center[0] + int(w * 5 / 12), center[1] - int(h / 2) - 100),
                     thickness=3,
                     color=[random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)])
        else:
            mask_out_edge = np.zeros((image.shape[0], image.shape[1]), np.uint8)
            cv2.drawContours(mask_out_edge, [max_c], 0, 1, 1)
            # cv2.drawContours(image, [max_c], 0, (0, 255, 0), 1)
            pixel_point1 = cv2.findNonZero(mask_out_edge)
            print("pixel point shape:", pixel_point1.shape)
            # print("pixel point:\n", pixel_point1)
            # point 1
            point1 = (np.min(pixel_point1[..., 0]), pixel_point1[..., 1][np.argmin(pixel_point1[..., 0])][0])
            print(point1)
            # point 2
            point2 = (np.max(pixel_point1[..., 0]), pixel_point1[..., 1][np.argmax(pixel_point1[..., 0])][0])
            print(point2)
            # point 3
            point3 = (pixel_point1[..., 0][np.argmin(pixel_point1[..., 1])][0], np.min(pixel_point1[..., 1]))
            print(point3)
            # point 4
            point4 = (pixel_point1[..., 0][np.argmax(pixel_point1[..., 1])][0], np.max(pixel_point1[..., 1]))
            print(point4)

            center = (int((point1[0] + point2[0]) / 2), int((point3[1] + point4[1]) / 2))

            # cv2.circle(mask_out_edge, point1, 2, 1, -1)
            # cv2.circle(mask_out_edge, point2, 2, 1, -1)
            # cv2.circle(mask_out_edge, point3, 2, 1, -1)
            # cv2.circle(mask_out_edge, point4, 2, 1, -1)

            # 1,3 之间
            list_13 = []
            # 1,4 之间
            list_14 = []
            list_23 = []
            list_24 = []

            # 把各个边的点存储
            for i in range(len(pixel_point1)):
                if point1[0] <= pixel_point1[i][0][0] <= point3[0] and point3[1] <= pixel_point1[i][0][1] <= point1[1]:
                    # print(f'介于1，3的点{pixel_point1[i][0]}')
                    list_13.append(pixel_point1[i][0])
                elif point3[0] <= pixel_point1[i][0][0] <= point2[0] and point3[1] <= pixel_point1[i][0][1] <= point2[
                    1]:
                    # print(f'介于2，3的点{pixel_point1[i][0]}')
                    list_23.append(pixel_point1[i][0])
                elif point4[0] <= pixel_point1[i][0][0] <= point2[0] and point2[1] <= pixel_point1[i][0][1] <= point4[
                    1]:
                    # print(f'介于2，4的点{pixel_point1[i][0]}')
                    list_24.append(pixel_point1[i][0])
                elif point1[0] <= pixel_point1[i][0][0] <= point4[0] and point1[1] <= pixel_point1[i][0][1] <= point4[
                    1]:
                    # print(f'介于1，4的点{pixel_point1[i][0]}')
                    list_14.append(pixel_point1[i][0])

            # x,y差值
            list_14 = np.array(list_14)
            list_13 = np.array(list_13)
            list_23 = np.array(list_23)
            list_24 = np.array(list_24)
            # print(list_13.shape)
            print(f'1,3间x:{np.max(list_13[:, 0]) - np.min(list_13[:, 0])}\n1,3间y:{np.max(list_13[:, 1]) - np.min(list_13[:, 1])}')
            inter_x_13 = np.max(list_13[:, 0]) - np.min(list_13[:, 0])
            inter_y_13 = np.max(list_13[:, 1]) - np.min(list_13[:, 1])
            inter_x_14 = np.max(list_14[:, 0]) - np.min(list_14[:, 0])
            inter_y_14 = np.max(list_14[:, 1]) - np.min(list_14[:, 1])
            # 13的大致方向和42是一样的，可以共用flag
            flag_13 = 1 if inter_x_13 > inter_y_13 else 2
            flag_14 = 1 if inter_x_14 > inter_y_14 else 2
            fit_array_13 = []
            fit_array_14 = []
            fit_array_24 = []
            fit_array_23 = []
            for p in list_13:
                if flag_13 == 1:
                    if point1[0] + inter_x_13 * 0.1 < p[0] < point3[0] - inter_x_13 * 0.1:
                        fit_array_13.append(p)
                elif flag_13 == 2:
                    if point3[1] + inter_y_13 * 0.1 < p[1] < point1[1] - inter_y_13 * 0.1:
                        fit_array_13.append(p)
            for p in list_24:
                if flag_13 == 1:
                    if point4[0] + inter_x_13 * 0.1 < p[0] < point2[0] - inter_x_13 * 0.1:
                        fit_array_24.append(p)
                elif flag_13 == 2:
                    if point2[1] + inter_y_13 * 0.1 < p[1] < point4[1] - inter_y_13 * 0.1:
                        fit_array_24.append(p)
            for p in list_14:
                if flag_14 == 1:
                    if point1[0] + inter_x_14 * 0.1 < p[0] < point4[0] - inter_x_14 * 0.1:
                        fit_array_14.append(p)
                elif flag_14 == 2:
                    if point1[1] + inter_y_14 * 0.1 < p[1] < point4[1] - inter_y_14 * 0.1:
                        fit_array_14.append(p)
            for p in list_23:
                if flag_14 == 1:
                    if point3[0] + inter_x_14 * 0.1 < p[0] < point2[0] - inter_x_14 * 0.1:
                        fit_array_23.append(p)
                elif flag_14 == 2:
                    if point3[1] + inter_y_14 * 0.1 < p[1] < point2[1] - inter_y_14 * 0.1:
                        fit_array_23.append(p)
            fit_array_13 = np.array(fit_array_13)
            fit_array_14 = np.array(fit_array_14)
            fit_array_23 = np.array(fit_array_23)
            fit_array_24 = np.array(fit_array_24)

            for p in fit_array_23:
                cv2.circle(image, p, 2, (0, 0, 255), -1)
            # plt.imshow(image[..., ::-1])
            # plt.show()

            st_end = []

            def paint_line(pts, pt1, pt2):
                line = cv2.fitLine(pts, cv2.DIST_HUBER, 0, 0.01, 0.01)
                k = line[1] / line[0]
                print('k:', k)
                b = line[3] - k[0] * line[2]
                w = 9000
                vx, vy, cx, cy = line
                print(cx)
                cv2.line(image, (int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w)),
                         (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), thickness=1)
                # 边线中点
                mid = (int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2))
                # cv2.circle(image, mid, 20, (5, 0, 255), -1)

                # 1/5处画线
                delta = 1 / 13
                cx = mid[0] + (center[0] - mid[0]) * delta
                cy = mid[1] + (center[1] - mid[1]) * delta
                cv2.circle(image, (int(cx), int(cy)), 5, (255, 0, 0), -1)
                cv2.line(image, (int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w)),
                         (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), thickness=3)
                print(f'起点、终点{(int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w))}')
                st_end.append([(int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w))])


            try:
                paint_line(fit_array_13, point1, point3)
                paint_line(fit_array_24, point2, point4)
                paint_line(fit_array_14, point1, point4)
                paint_line(fit_array_23, point2, point3)
            except:
                return [rect[1][1], rect[1][1], rect[1][0], rect[1][0]]

            cv2.circle(image, point2, 20, (5, 0, 255), -1)
            # 外接矩形的尺寸
            print(rect[1])
            print(st_end)
        print(f'cost:{time.time() - st} s')

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = 255 - img
        img = img.astype(np.float32)
        res = []
        for pt in st_end:
            print('--------------------\n', pt)
            p0 = pt[0]
            p1 = pt[1]
            nsamples, M = build_transform(p0, p1, stride=1 / 4)
            samples = sample_opencv(img, M, nsamples)
            samples = scipy.ndimage.gaussian_filter1d(samples, sigma=8.0)

            gradient = np.diff(samples) * 4
            # gradient[4000: 28000] *= 0.5
            i_falling = np.argmin(gradient)
            i_rising = np.argmax(gradient)
            print(f'falling:{i_falling}, rising:{i_rising}')
            max_index2 = np.argsort(gradient)[-2]
            ji = gradient[signal.argrelextrema(gradient, np.greater)]
            print(max(ji))

            distance = np.abs(i_rising - i_falling) / 4
            # gradient *= 255 / np.abs(gradient).max()
            print(distance)
            res.append(distance)
            # plt.subplot(121), plt.plot(samples.astype(np.float64))
            # plt.subplot(122), plt.plot(gradient.astype(np.float64))
            # plt.show()

        # plt.imshow(image[:, :, ::-1])
        # plt.show()
        if abs(res[0] - res[1]) > 200:
            res[0] = max(res[0], res[1])
            res[1] = max(res[0], res[1])
        if res[0] < 200 and res[1] < 200:
            res[0] = rect[1][1]
            res[1] = rect[1][1]
        if abs(res[2] - res[3]) > 200:
            res[2] = max(res[2], res[3])
            res[2] = max(res[2], res[3])
        if res[2] < 200 and res[3] < 200:
            res[2] = rect[1][0]
            res[3] = rect[1][0]
        return res


class BlackProcess:
    def __init__(self):
        pass
    def process(self, im):
        st = time.time()
        im = extract_func(im)
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        img = im
        # img = img[:, 1000: 15000]
        # img_3 = cv2.resize(img.copy(), dsize=(0, 0), fx=0.1, fy=0.1)
        img_3 = img.copy()
        angle_1 = get_angle(img_3, th=5)
        if angle_1 < 50:
            img = cv2.flip(img, 1)
        if angle_1 < 10 or (90 - angle_1) < 10:
            height, width = img.shape[:2]
            center = (width / 2, height / 2)
            M = cv2.getRotationMatrix2D(center, 5, 1)
            heightNew = int(width * abs(sin(radians(5))) + height * abs(cos(radians(5))))
            widthNew = int(height * abs(sin(radians(5))) + width * abs(cos(radians(5))))
            M[0, 2] += (widthNew - width) / 2
            M[1, 2] += (heightNew - height) / 2
            img = cv2.warpAffine(img, M, dsize=(widthNew, heightNew), borderValue=0)
        # plt.imshow(img[..., ::-1])
        # plt.show()
        img_2 = img.copy()
        # img_2 = cv2.resize(img_2, dsize=(0, 0), fx=0.2, fy=0.2)
        edged = init(img_2, th=5)
        # plt.imshow(edged, 'gray')
        # plt.show()
        edged = cv2.dilate(edged, kernel=np.ones((3, 3), dtype=np.uint8), iterations=10)
        erode = cv2.erode(edged, kernel=np.ones((3, 3), dtype=np.uint8), iterations=30)
        di = cv2.dilate(erode, kernel=np.ones((3, 3), dtype=np.uint8), iterations=30)
        image = img.copy()
        # plt.imshow(di, 'gray')
        # plt.show()

        # 获取所有轮廓
        contours = cv2.findContours(di.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
        # 合并轮廓
        merge_list = []
        for cnt in cnts:
            if cv2.contourArea(cnt) < 90000:
                print(cv2.contourArea(cnt))
                continue
            # print(cv2.contourArea(cnt))
            merge_list.append(cnt)
        if len(merge_list) >= 2:
            contours_merge = np.vstack([merge_list[0], merge_list[1]])
            for i in range(2, len(merge_list)):
                contours_merge = np.vstack([contours_merge, merge_list[i]])
        else:
            contours_merge = merge_list[0]
        # 最小外接矩形
        rect = cv2.minAreaRect(contours_merge)
        new_rect = ((rect[0][0] * 5, rect[0][1] * 5), (rect[1][0] * 5 + 100, rect[1][1] * 5 + 100), rect[2])
        # rect = ((rect[0][0], rect[0][1]), (rect[1][0] + 100, rect[1][1] + 100), rect[2])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # print('box:', box)
        # print('angle:', rect[2])

        center = [int(pos) for pos in rect[0]]
        x, y, w, h = cv2.boundingRect(max_c)
        # x, y, w, h = x * 5, y * 5, w * 5, h * 5
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        # cv2.drawContours(image, [box], 0, (0, 0, 255), 10)
        # plt.imshow(image[..., ::-1])
        # plt.show()

        # 取最小外接矩形的点的信息
        mask = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        cv2.drawContours(mask, [box], 0, 255, 1)
        # plt.imshow(mask, 'gray')
        # plt.show()
        all_points = cv2.findNonZero(mask)
        # x min
        point1 = (np.min(all_points[..., 0]), all_points[..., 1][np.argmin(all_points[..., 0])][0])
        print(point1)
        # point 2 x max
        point2 = (np.max(all_points[..., 0]), all_points[..., 1][np.argmax(all_points[..., 0])][0])
        print(point2)
        # point 3 y min
        point3 = (all_points[..., 0][np.argmin(all_points[..., 1])][0], np.min(all_points[..., 1]))
        print(point3)
        # point 4 y max
        point4 = (all_points[..., 0][np.argmax(all_points[..., 1])][0], np.max(all_points[..., 1]))
        print(point4)

        # cv2.circle(image, point2, 5, (0, 0, 255), -1)
        # plt.imshow(image[..., ::-1])
        # plt.show()

        # 外接矩形上的点向边缘逼近
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        m = 400
        to_del = set()
        line_13_1 = []
        line_13_2 = []
        line_23_1 = []
        line_23_2 = []
        line_24_1 = []
        line_24_2 = []
        line_14_1 = []
        line_14_2 = []
        for i in range(len(all_points)):
            flag = False
            if image[all_points[i][0][1]][all_points[i][0][0]] >= 30:
                flag = True
            if point1[0] <= all_points[i][0][0] <= point3[0] and point3[1] <= all_points[i][0][1] <= point1[1]:
                # print(f'介于1，3的点{all_points[i][0]}, 灰度值是{image[all_points[i][0][1]][all_points[i][0][0]]}')
                for j in range(1, m):
                    if image[all_points[i][0][1] + j][all_points[i][0][0]] > image[all_points[i][0][1]][
                        all_points[i][0][0]] + 15 or image[all_points[i][0][1]][all_points[i][0][0]] >= 30:
                        all_points[i][0][1] += j
                        flag = True
                        break
                if flag is True:
                    if point1[0] + (point3[0] - point1[0]) * 5 / 6 <= all_points[i][0][0] <= point3[0] - (
                            point3[0] - point1[0]) * 1 / 80:
                        line_13_2.append(all_points[i][0])
                    if point1[0] + (point3[0] - point1[0]) * 1 / 80 <= all_points[i][0][0] <= point1[0] + (
                            point3[0] - point1[0]) * 1 / 6:
                        line_13_1.append(all_points[i][0])


            elif point3[0] <= all_points[i][0][0] <= point2[0] and point3[1] <= all_points[i][0][1] <= point2[1]:
                for j in range(1, m):
                    if image[all_points[i][0][1]][all_points[i][0][0] - j] > image[all_points[i][0][1]][
                        all_points[i][0][0]] + 15:
                        all_points[i][0][0] -= j
                        flag = True
                        break
                if flag is True:
                    if point3[1] + (point2[1] - point3[1]) * 5 / 6 <= all_points[i][0][1] <= point2[1] - (
                            point2[1] - point3[1]) * 1 / 80:
                        line_23_2.append(all_points[i][0])
                    if point3[1] + (point2[1] - point3[1]) * 1 / 80 <= all_points[i][0][1] <= point3[1] + (
                            point2[1] - point3[1]) * 1 / 6:
                        line_23_1.append(all_points[i][0])

            elif point4[0] <= all_points[i][0][0] <= point2[0] and point2[1] <= all_points[i][0][1] <= point4[1]:
                for j in range(1, m):
                    if image[all_points[i][0][1] - j][all_points[i][0][0]] > image[all_points[i][0][1]][
                        all_points[i][0][0]] + 15:
                        all_points[i][0][1] -= j
                        flag = True
                        break
                if flag is True:
                    if point4[0] + (point2[0] - point4[0]) * 5 / 6 <= all_points[i][0][0] <= point2[0] - (
                            point2[0] - point4[0]) * 1 / 80:
                        line_24_2.append(all_points[i][0])
                    if point4[0] + (point2[0] - point4[0]) * 1 / 80 <= all_points[i][0][0] <= point4[0] + (
                            point2[0] - point4[0]) * 1 / 6:
                        line_24_1.append(all_points[i][0])

            elif point1[0] <= all_points[i][0][0] <= point4[0] and point1[1] <= all_points[i][0][1] <= point4[1]:
                for j in range(1, m):
                    if image[all_points[i][0][1]][all_points[i][0][0] + j] > image[all_points[i][0][1]][
                        all_points[i][0][0]] + 15:
                        all_points[i][0][0] += j
                        flag = True
                        break
                if flag is True:
                    if point1[1] + (point4[1] - point1[1]) * 5 / 6 <= all_points[i][0][1] <= point4[1] - (
                            point4[1] - point1[1]) * 1 / 80:
                        line_14_2.append(all_points[i][0])
                    if point1[1] + (point4[1] - point1[1]) * 1 / 80 <= all_points[i][0][1] <= point1[1] + (
                            point4[1] - point1[1]) * 1 / 6:
                        line_14_1.append(all_points[i][0])
            if flag is False:
                to_del.add(i)
        to_del = list(to_del)
        to_del.sort()
        all_points = np.delete(all_points, to_del, axis=0)
        # print(to_del)
        # for i in to_del:
        #     print(image[all_points[i][0][1]][all_points[i][0][0]])
        # for i in range(50):
        #     print(image[all_points[4717][0][1] + i][all_points[4717][0][0]])

        # cv2.polylines(img, [all_points], True, (0, 0, 255), 1)
        print(len(all_points))
        # print(line_13)

        line_13_1 = np.array(line_13_1)
        line_13_2 = np.array(line_13_2)
        line_23_1 = np.array(line_23_1)
        line_23_2 = np.array(line_23_2)
        line_24_1 = np.array(line_24_1)
        line_24_2 = np.array(line_24_2)
        line_14_1 = np.array(line_14_1)
        line_14_2 = np.array(line_14_2)


        def paint_line(pts, pt1=None, pt2=None):
            line = cv2.fitLine(pts, cv2.DIST_HUBER, 0, 0.01, 0.01)
            k = line[1] / line[0]
            print('k:', k)
            b = line[3] - k[0] * line[2]
            w = 600
            vx, vy, cx, cy = line
            if pt1 is not None:
                w = 4000
                mid = (int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2))
                delta = 1 / 30
                cx = mid[0] + (center[0] - mid[0]) * delta
                cy = mid[1] + (center[1] - mid[1]) * delta
            print(cx)
            cv2.line(img, (int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w)),
                     (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), thickness=10)

            print(f'起点、终点{(int(cx - vx * w), int(cy - vy * w)), (int(cx + vx * w), int(cy + vy * w))}')

            return [int(cx - vx * w), int(cy - vy * w), int(cx + vx * w), int(cy + vy * w)]

        def cross_point(line1, line2):  # 计算交点函数
            x1 = line1[0]  # 取四点坐标
            y1 = line1[1]
            x2 = line1[2]
            y2 = line1[3]

            x3 = line2[0]
            y3 = line2[1]
            x4 = line2[2]
            y4 = line2[3]

            k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
            b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键
            if (x4 - x3) == 0:  # L2直线斜率不存在操作
                k2 = None
                b2 = 0
            else:
                k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在操作
                b2 = y3 * 1.0 - x3 * k2 * 1.0
            if k2 == None:
                x = x3
            else:
                x = (b2 - b1) * 1.0 / (k1 - k2)
            y = k1 * x * 1.0 + b1 * 1.0
            # return [int(x), int(y)]
            return [x, y]

        def cal_distance(pt1, pt2):
            return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

        for i in range(len(all_points)):
            cv2.circle(img, tuple(all_points[i][0]), 1, (0, 0, 255), -1)

        try:
            l_131 = paint_line(line_13_1)
            l_132 = paint_line(line_13_2)
            l_231 = paint_line(line_23_1)
            l_232 = paint_line(line_23_2)
            l_241 = paint_line(line_24_1)
            l_242 = paint_line(line_24_2)
            l_141 = paint_line(line_14_1)
            l_142 = paint_line(line_14_2)
            # line_13 =
            l_13 = paint_line(np.append(line_13_1, line_13_2, axis=0), point1, point3)
            l_23 = paint_line(np.append(line_23_1, line_23_2, axis=0), point2, point3)
            l_24 = paint_line(np.append(line_24_1, line_24_2, axis=0), point2, point4)
            l_14 = paint_line(np.append(line_14_1, line_14_2, axis=0), point1, point4)
        except Exception as e:
            print(e)
            return [rect[1][1], rect[1][1], rect[1][0], rect[1][0]]

        print(cross_point(l_131, l_14))
        # cv2.circle(img, tuple(cross_point(l_131, l_14)), 3, (0, 0, 255), 3)
        # cv2.circle(img, tuple(cross_point(l_241, l_14)), 3, (0, 0, 255), 3)
        #
        # cv2.circle(img, tuple(cross_point(l_132, l_23)), 3, (0, 0, 255), 3)
        # cv2.circle(img, tuple(cross_point(l_242, l_23)), 3, (0, 0, 255), 3)
        #
        # cv2.circle(img, tuple(cross_point(l_141, l_13)), 3, (0, 0, 255), 3)
        # cv2.circle(img, tuple(cross_point(l_231, l_13)), 3, (0, 0, 255), 3)
        #
        # cv2.circle(img, tuple(cross_point(l_142, l_24)), 3, (0, 0, 255), 3)
        # cv2.circle(img, tuple(cross_point(l_232, l_24)), 3, (0, 0, 255), 3)

        # plt.imshow(img[..., ::-1])
        # plt.show()

        h1 = cal_distance(cross_point(l_131, l_14), cross_point(l_241, l_14))
        h2 = cal_distance(cross_point(l_132, l_23), cross_point(l_242, l_23))
        w1 = cal_distance(cross_point(l_141, l_13), cross_point(l_231, l_13))
        w2 = cal_distance(cross_point(l_142, l_24), cross_point(l_232, l_24))
        print([h1, h2, w1, w2])
        if abs(h1 - h2) > 500:
            h1 = max(h1, h2)
            h2 = max(h1, h2)
        if abs(w1 - w2) > 500:
            w1 = max(w1, w2)
            w2 = max(w1, w2)
        return [h1, h2, w1, w2]

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

    b_p = BlackProcess()
    w_p = WhiteProcess()
    img = cv2.imread(r"D:\stone_detection\mono\2024-01-25_15-47-20.bmp", 0)
    # img = img[[not np.all(img[i] == 0) for i in range(img.shape[0])], ...]
    # b_p.process(img)
    # res = w_p.process(img)
    res = b_p.process(img)
    for i in res:
        print(i*0.09477)

    # root = r"E:\Deep_Learning\stone\1018_1"
    # img_list = os.listdir(root)
    # for n in img_list:
    #     img_path = root + '/' + n
    #     img = cv2.imread(img_path, 0)
    #     res = b_p.process(img)
    #     for i in res:
    #         print(i*0.09477)
    #     size1 = (res[0] + res[1]) * 0.09477 / 2
    #     size2 = (res[2] + res[3]) * 0.09477 / 2
    #     size1, size2 = max(size1, size2), min(size1, size2)
    #     size1 = '%.1f'%size1
    #     size2 = '%.1f' % size2
    #     write2excel([n, size1, size2], r"C:\Users\陈思遥\Desktop\results2.xls", 3)