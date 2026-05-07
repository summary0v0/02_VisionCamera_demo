import dxfgrabber
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
import time
import os
import matplotlib
matplotlib.use('TkAgg')

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return cv_img

def init_canvas(cad_path=None):
    # 是否已存在
    exist_bmp = False
    if cad_path is None:
        return
    else:
        # 记录cad的名字，后面缓存图片时使用
        # 后续再读入相同名字的，直接调取相同名字的模拟图
        cad_name = cad_path.split('\\')[-1].split('/')[-1].split('.')[0]
        p = './' + cad_name + '.bmp'
        if os.path.exists(p):
            print('该CAD图片已存在')
            exist_bmp = True
        else:
            print('新建CAD图片')

    dxf = dxfgrabber.readfile(cad_path)
    for layer in dxf.layers:
        print(layer.name, layer.color, layer.linetype)

    tmp_x = []
    tmp_y = []

    start_pt = []
    end_pt = []
    text_pt = []
    text = []

    # 横竖线
    row_line = []
    col_line = []

    # 交点
    cross_pt = []

    for e in dxf.entities:
        # print(e.dxftype,e.layer)
        if e.dxftype == 'LINE':
            start_pt.append([int(e.start[0] / 10), int(e.start[1] / 10)])
            end_pt.append([int(e.end[0] / 10), int(e.end[1] / 10)])

            if start_pt[-1][1] == end_pt[-1][1]:
                row_line.append([start_pt[-1], end_pt[-1]])
            elif start_pt[-1][0] == end_pt[-1][0]:
                col_line.append([start_pt[-1], end_pt[-1]])

            tmp_x.append(int(e.start[0] / 10))
            tmp_x.append(int(e.end[0] / 10))
            tmp_y.append(int(e.start[1] / 10))
            tmp_y.append(int(e.end[1] / 10))

        if e.dxftype == 'LWPOLYLINE':
            if len(e.points) != 4:
                continue
            # p1, p2, p3, p4 = e.points
            tmp_x.append(int(e.points[-1][0] / 10))
            tmp_y.append(int(e.points[-1][1] / 10))
            for i in range(3):
                tmp_x.append(int(e.points[i][0] / 10))
                tmp_y.append(int(e.points[i][1] / 10))
                for j in range(i + 1, 4):
                    # 判断四个点中哪两个是一个竖线
                    if e.points[i][0] == e.points[j][0]:
                        start_pt.append([int(e.points[i][0] / 10), int(e.points[i][1] / 10)])
                        end_pt.append([int(e.points[j][0] / 10), int(e.points[j][1] / 10)])
                        col_line.append([start_pt[-1], end_pt[-1]])
                    # 判断四个点中哪两个是一个横线
                    elif e.points[i][1] == e.points[j][1]:
                        start_pt.append([int(e.points[i][0] / 10), int(e.points[i][1] / 10)])
                        end_pt.append([int(e.points[j][0] / 10), int(e.points[j][1] / 10)])
                        row_line.append([start_pt[-1], end_pt[-1]])

        if e.dxftype == 'TEXT':
            if hasattr(e, 'text'):
                _flag = False
                # 文字
                for s in e.text:
                    if u'\u4e00' <= s <= u'\u9fff':
                        _flag = True
                        break
                if _flag is False:
                    text.append(e.text)
                    # 坐标
                    text_pt.append([int(e.insert[0] / 10), int(e.insert[1] / 10)])

    # print(text)
    min_x = min(tmp_x)
    min_y = min(tmp_y)
    width = max(tmp_x) - min_x
    height = max(tmp_y) - min_y
    height += 50
    width += 50
    print(height, width)

    for i in range(len(start_pt)):
        start_pt[i][0] -= (min_x - 5)
        start_pt[i][1] -= (min_y - 5)
        # print(start_pt[i][1])
        start_pt[i][1] = height - start_pt[i][1]
    for i in range(len(end_pt)):
        end_pt[i][0] -= (min_x - 5)
        end_pt[i][1] -= (min_y - 5)
        end_pt[i][1] = height - end_pt[i][1]
    for i in range(len(text_pt)):
        text_pt[i][0] -= (min_x - 5)
        text_pt[i][1] -= (min_y - 5)
        text_pt[i][1] = height - text_pt[i][1]

    for r_l in row_line:
        # row
        # 起始x
        r_x_s = min(r_l[0][0], r_l[1][0])
        r_x_e = max(r_l[0][0], r_l[1][0])
        # y
        r_y = r_l[0][1]
        for c_l in col_line:
            c_x = c_l[0][0]
            c_y_s = min(c_l[0][1], c_l[1][1])
            c_y_e = max(c_l[0][1], c_l[1][1])
            # 判断交点
            # col的x是否落在row的x区间内
            if r_x_s <= c_x <= r_x_e:
                # row的y是否落在col的y区间内
                if c_y_s <= r_y <= c_y_e:
                    cross_pt.append([c_x, r_y])

    # print(cross_pt)
    # 按y排序row
    # 升序
    row_line_ascend_y = sorted(row_line, key=lambda x: x[0][1])
    # 降序
    row_line_descend_y = sorted(row_line, key=lambda x: x[0][1], reverse=True)
    # 按x排序col
    col_line_ascend_x = sorted(col_line, key=lambda x: x[0][0])
    col_line_descend_x = sorted(col_line, key=lambda x: x[0][0], reverse=True)

    # print(col_line_ascend_x)
    # print(row_line_ascend_y)

    canvas = np.ones((height, width, 3), np.uint8)
    canvas.fill(255)

    # for i in range(len(start_pt)):
    #     canvas = cv2.line(
    #         canvas, (start_pt[i][0], start_pt[i][1]), (end_pt[i][0], end_pt[i][1]), (0, 0, 0), 1
    #     )
    for i in range(len(row_line)):
        canvas = cv2.line(
            canvas, row_line[i][0], row_line[i][1], (0, 0, 0), 2
        )
    for i in range(len(col_line)):
        canvas = cv2.line(
            canvas, col_line[i][0], col_line[i][1], (0, 0, 0), 2
        )
    for pt in cross_pt:
        canvas = cv2.circle(canvas, pt, 3, (0, 0, 255), -1)
    for i in range(len(text)):
        canvas = cv2.putText(canvas, text[i], text_pt[i], cv2.FONT_HERSHEY_COMPLEX, 0.5,
                             (0, 0, 0), 1)

    if exist_bmp is False:
        cv2.imencode('.bmp', canvas)[1].tofile(p)

    return canvas, row_line_ascend_y, row_line_descend_y, col_line_ascend_x, col_line_descend_x, text_pt, text, p

def handle_dxf(row_line_ascend_y, row_line_descend_y, col_line_ascend_x, col_line_descend_x, text_pt, text_list, img=None, text=None, paste_img=None, img_path=None):
    canvas = img
    # 查找text对应索引
    if text not in text_list:
        print('error')
        return
    text_index = text_list.index(text)
    t_pt = text_pt[text_index]
    # 给text找格子
    col_left = None
    col_right = None
    row_top = None
    row_bottom = None
    # 1、找左边的竖线
    # 遍历x降序的col，找第一个x小于text的x的线
    for c_l in col_line_descend_x:
        if c_l[0][0] < t_pt[0]:
            # 判断text的y在不在col的y区间
            if min(c_l[0][1], c_l[1][1]) <= t_pt[1] <= max(c_l[0][1], c_l[1][1]):
                col_left = c_l
                break
            else:
                continue
    # 2、找右边的竖线
    # 遍历x升序的col，找第一个x大于text的x的线
    for c_l in col_line_ascend_x:
        if c_l[0][0] > t_pt[0]:
            # 判断text的y在不在col的y区间
            if min(c_l[0][1], c_l[1][1]) <= t_pt[1] <= max(c_l[0][1], c_l[1][1]):
                col_right = c_l
                break
            else:
                continue
    # 3、找上边的竖线
    # 遍历y降序的row，找第一个y小于text的y的线
    for r_l in row_line_descend_y:
        if r_l[0][1] < t_pt[1]:
            # 判断text的x在不在row的x区间
            if min(r_l[0][0], r_l[1][0]) <= t_pt[0] <= max(r_l[0][0], r_l[1][0]):
                row_top = r_l
                break
            else:
                continue
    # 4、找底边的竖线
    # 遍历y升序的row，找第一个y大于text的y的线
    for r_l in row_line_ascend_y:
        if r_l[0][1] > t_pt[1]:
            # 判断text的x在不在row的x区间
            if min(r_l[0][0], r_l[1][0]) <= t_pt[0] <= max(r_l[0][0], r_l[1][0]):
                row_bottom = r_l
                break
            else:
                continue

    # print(t_pt)
    # print(i)
    # 格子左上右下坐标
    if None in [col_left, col_right, row_top, row_bottom]:
        print(col_left, col_right, row_top, row_bottom)
        return
    grid_top_left = [col_left[0][0], row_top[0][1]]
    grid_bottom_right = [col_right[0][0], row_bottom[0][1]]
    cv2.rectangle(canvas, grid_top_left, grid_bottom_right, (255, 0, 0), -1)
    # paste_img = cv2.imread(r"E:\Deep_Learning\stone\black\Image-0007.bmp")
    paste_img = cv2.resize(paste_img,
                           (grid_bottom_right[0] - grid_top_left[0], grid_bottom_right[1] - grid_top_left[1]))
    canvas[grid_top_left[1]: grid_bottom_right[1], grid_top_left[0]: grid_bottom_right[0]] = paste_img

    # plt.imshow(canvas, 'gray')
    # plt.savefig('./cad.jpg', dpi=2000)
    cv2.imencode('.bmp', canvas)[1].tofile(img_path)
    # plt.show()
        # time.sleep(10)

if __name__ == '__main__':
    paste_img = cv2.imread(r'D:\stone_detection\color\2023-10-18_13-55-20.jpg')
    canvas, x_ao, y_ao, x_do, y_do, text_pt, text_list, im_p = init_canvas(cad_path=r"Y:\2024-01-02\Hotel06越南富国岛酒店卫生间墙地面.dxf")
    print(text_list)
    if os.path.exists(im_p):
        canvas = cv_imread(im_p)
    handle_dxf(x_ao, y_ao, x_do, y_do, text_pt, text_list, canvas, 'P4', paste_img=paste_img, img_path=im_p)