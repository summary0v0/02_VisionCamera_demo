from PyQt5.QtCore import QObject, QThread, pyqtSignal, QWaitCondition, QMutex
import os
import shutil
import time
from common.dbFunction import *
# 部署时打开
from common.my_cam_new import *
from common.trans_ini import *
import serial
import numpy as np
from common.img_process import WhiteProcess, BlackProcess
import cv2
from common.qrcode_reader import *
from common.execute_cad import *
from socket import *

import json
import glob
from fuzzywuzzy import process

# 0都ok，1黑白异常，2彩色异常
flag_cam = 0
error_code = []
# 每次使用前清空文件夹1，2
shutil.rmtree(r"D:/tmp_dir1")
shutil.rmtree(r"D:/tmp_dir2")
os.mkdir(r"D:/tmp_dir1")
os.mkdir(r"D:/tmp_dir2")

import ctypes


def safe_load_cfg(grab_obj, path_str, name):
    """
    加载采集卡配置文件 (.vlcf)
    修正 0xC0000409 崩溃问题
    """
    abs_path = os.path.normpath(os.path.abspath(path_str))

    if not os.path.exists(abs_path):
        print(f"[{name}] 错误：找不到文件 -> {abs_path}")
        return False

    # 尝试多种方式加载，确保不触发底层溢出
    # Windows 环境下，IKap 驱动通常识别 GBK 编码的中文路径
    for enc in ['gbk', 'utf-8']:
        try:
            # 方案 A：使用 ctypes 创建一个明确长度的字符缓冲区 (最安全)
            # 这样可以确保内存块在传递给 DLL 时是规范的
            path_bytes = abs_path.encode(enc)
            # 【修复点 1】: create_string_buffer 会自动补 \x00，不需要手动加 b'\x00'
            char_array = ctypes.create_string_buffer(path_bytes)
            if grab_obj.LoadConfigurationFile(char_array.value):
                print(f"[{name}] .vlcf 加载成功 (Encoding: {enc})")
                return True
        except Exception as e:
            print(f"[{name}] 编码 {enc} 尝试失败: {e}")
            continue

    return False

IKapBoardGrabLineTrigger.GetBoardCount()
board_count = IKapBoardGrabLineTrigger.GetBoardCount()
print(f"系统识别到的板卡数量: {board_count}")
if board_count < 2:
    print("警告：板卡数量不足，可能导致 OpenDevice 失败")
# 在 OpenDevice 之前加入简单的延迟或重试
print("正在检测采集卡服务...")
count = IKapBoardGrabLineTrigger.GetBoardCount()
if count == 0:
    print("错误：未检测到采集卡，请确认 IKapService 已启动且硬件连接正常！")
else:
    print(f"检测到 {count} 张采集卡，准备初始化...")

grab_mono = IKapBoardGrabLineTrigger(r"D:/tmp_dir1")
grab_color = IKapBoardGrabLineTrigger(r"D:/tmp_dir2")
# Open device
if not grab_mono.OpenDevice(0):
    print("MONO: Open device failure")
    error_code.append("黑白相机打开失败！\n")
    flag_cam = 1
if not grab_color.OpenDevice(1):
    print("COLOR: Open device failure")
    error_code.append("彩色相机打开失败！\n")
    flag_cam = 2
with open('./configs/cfg.json', 'r') as f:
    cfg = json.load(f)
mono_cfg_path = cfg['mono_vlcf']
color_cfg_path = cfg['color_vlcf']
# --- 替换 my_thread.py 中从 mono_cfg_path 定义到 StartGrab 之前的代码 ---

# 获取绝对路径
mono_cfg_path = os.path.abspath(cfg['mono_vlcf'])
color_cfg_path = os.path.abspath(cfg['color_vlcf'])

# 1. 加载黑白相机配置
print(f"尝试加载黑白配置: {mono_cfg_path}")
if not safe_load_cfg(grab_mono, mono_cfg_path, "MONO"):
    error_code.append("黑白相机加载配置失败！\n")
    flag_cam = 1
else:
    # ====== 【关键修复点 2】：强制重新设置黑白相机的宽高 ======
    # 尺寸来源于你的文件名：w16384_h24000
    grab_mono.SetResolution(16384, 24000)

    if not grab_mono.SetLineTrigger():
        print("MONO: Set line trigger failure")
        error_code.append("黑白相机设置线触发失败！\n")
        flag_cam = 1
print(f"黑白相机配置: {mono_cfg_path} 加载成功")
# 2. 加载彩色相机配置
print(f"尝试加载彩色配置: {color_cfg_path}")
if not safe_load_cfg(grab_color, color_cfg_path, "COLOR"):
    error_code.append("彩色相机加载配置失败！\n")
    flag_cam = 2
else:
    # ====== 【关键修复点 3】：强制重新设置彩色相机的宽高 ======
    # 尺寸来源于你的文件名：w8320_h24000
    grab_color.SetResolution(8320, 24000)

    if not grab_color.SetLineTrigger():
        print("COLOR: Set line trigger failure")
        error_code.append("彩色相机设置线触发失败！\n")
        flag_cam = 2
print(f"彩色相机配置: {mono_cfg_path} 加载成功")
# 3. 启动拍摄 (只有在没有致命错误时尝试)
if flag_cam == 0:
    print("准备启动黑白相机底层采集...")
    if not grab_mono.StartGrab(0):
        error_code.append("黑白相机开始拍摄失败！\n")

    # 加入 2 秒的延迟，让黑白相机的内存环和总线先稳定下来
    time.sleep(2)

    print("准备启动彩色相机底层采集...")
    if not grab_color.StartGrab(0):
        error_code.append("彩色相机开始拍摄失败！\n")

# 判断文件夹存在
dirs = ["D:/tmp_dir1/", "D:/tmp_dir2/", "D:/stone_detection/mono/", "D:/stone_detection/color/"]
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)

# 扫码器的结果
qr_list = []

# 监视文件夹
class WatchDogThread(QThread):

    sizeSignal = pyqtSignal(object)
    # 黑色图片报警
    errorSignal = pyqtSignal(object)
    # cad
    cadSignal = pyqtSignal(object)
    # 获得图片
    getSignal = pyqtSignal(object)
    # 项目
    proSignal = pyqtSignal(object)
    # 更新
    updateSignal = pyqtSignal(object)
    updateSignal_2 = pyqtSignal(object)

    def __init__(self, parent=None, ID=None, use_color=1, cad_path=None):
        super(WatchDogThread, self).__init__(parent)
        self._isPause = False
        self._value = 0
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        # 上传缓存
        self.upload = []
        # 读码的位置缓存
        self.loc = []
        self.mono_height = 15000
        self.mono_width = 16384
        self.color_height = 12000
        self.color_width = 8320
        # 编号
        self.id_prefix = time.strftime('%Y%m%d', time.localtime()) + '0000'
        self.id = ID + 1

        self.h_delta = 0.09477
        self.w_delta = 0.09477

        self.type = -1
        # 是否等待彩色相机，默认使用
        self.use_color_cam = use_color
        # cad路径
        self.cad_path = cad_path
        # 画布
        self.canvas = None
        print(f'看门狗类初始化成功')

    def pause(self):
        self._isPause = True

    def resume(self):
        self._isPause = False
        self.cond.wakeAll()
        # 【修复点 1】：增加 cad_path 非空判断，防止 split 崩溃
        if self.cad_path:
            # 查找是否存在cad name的bmp,不存在就新建
            cad_name = self.cad_path.split('/')[-1].split('.')[0]
            p = './' + cad_name + '.bmp'
            if os.path.exists(p):
                canvas = cv_imread(p)
            else:
                canvas, x_ao, y_ao, x_do, y_do, text_pt, text_list, _ = init_canvas(self.cad_path)
            self.canvas = canvas
            self.cadSignal.emit([1, cad_name])
        else:
            print("警告：CAD 路径为空，跳过画布唤醒初始化")

    def run(self):
        # 相机异常就传递异常值
        if flag_cam != 0:
            self.errorSignal.emit(error_code)
            print(error_code)
        w_p = WhiteProcess()
        b_p = BlackProcess()
        # ==================== 核心修复点 ====================
        # 拦截 cad_path 为 None 的情况，防止崩溃并赋予安全的初始值
        if not self.cad_path:
            print("警告：启动时未检测到 CAD 文件路径，看门狗已空载运行等待输入...")
            cad_name = "default_cad"
            p = './default_cad.bmp'
            canvas = None
            x_ao = y_ao = x_do = y_do = 0
            text_pt = []
            text_list = []  # 赋空列表，防止后续匹配时报错
        else:
            # 查找是否存在cad name的bmp,不存在就新建
            cad_name = self.cad_path.split('/')[-1].split('.')[0]
            p = './' + cad_name + '.bmp'

            canvas, x_ao, y_ao, x_do, y_do, text_pt, text_list, _ = init_canvas(self.cad_path)
            if os.path.exists(p):
                canvas = cv_imread(p)
        # ====================================================

        self.canvas = canvas
        # self.cadSignal.emit([1, cad_name])
        while True:
            # 线程锁on
            self.mutex.lock()
            if self._isPause:
                print('暂停')
                self.cond.wait(self.mutex)
            # 类别没选择则跳过
            if self.type != -1:
                # print('白色') if self.type == 0 else print('黑色')
                dir1_path = "D:/tmp_dir1"
                dir2_path = "D:/tmp_dir2"
                mono_path = "D:/stone_detection/mono"
                color_path = "D:/stone_detection/color"
                mono = os.listdir(dir1_path)
                color = os.listdir(dir2_path)

                # 处理黑白
                if len(mono):
                    self.getSignal.emit('黑白相机采图')
                    tmp_dict = {
                        'id': None,
                        'mono_path': None,
                        'color_path': None,
                        'scan_height': None,
                        'scan_width': None,
                        'area': None,
                        'qr_height': None,
                        'qr_width': None
                    }
                    # insertdata(mono_path + '/' + mono[0], 1, 1, 1)
                    if mono[0][-3:] == 'raw':
                        mono_img = np.fromfile(dir1_path + '/' + mono[0], dtype='uint8')
                        # 将raw转换
                        mono_img = mono_img.reshape(-1, self.mono_width, 1)
                    else:
                        time.sleep(3)
                        mono_img = cv2.imread(dir1_path + '/' + mono[0], 0)
                    _mono = mono_img.copy()
                    # _mono = cv2.resize(_mono, dsize=(0, 0), fx = 0.1, fy=0.1)
                    # 去除0行
                    _mono = _mono[[not np.all(_mono[i] == 0) for i in range(_mono.shape[0])], ...]
                    # 保存处理好的黑白图片到正式目录，并备份原始图到 tmp 目录
                    _path_mono =  mono_path + '/' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.bmp'

                    cv2.imwrite('D:/tmp/' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.bmp', mono_img)

                    cv2.imwrite(_path_mono, _mono)
                    print('save_mono')

                    tmp_dict['mono_path'] = _path_mono
                    # 彩色的地址先放黑白的，后面如果是使用彩色的则会被修改
                    tmp_dict['color_path'] = _path_mono
                    # id
                    tmp_dict['id'] = int(self.id_prefix) + self.id
                    self.id += 1
                    print(f'处理黑白图像宽高')
                    # TODO:处理黑白图像宽高
                    # 处理图像
                    # try:
                    #     if self.type == 0:
                    #         res_mono = w_p.process(mono_img)
                    #     elif self.type == 1:
                    #         res_mono = b_p.process(mono_img)
                    # except Exception as e:
                    #     print(e)
                    #     res_mono = [0, 0, 0, 0]
                    print(mono_img.shape)
                    _mono = cv2.imread(_path_mono, 0)
                    try:
                        if self.type == 0:
                            print('使用白色')
                            res_mono = w_p.process(_mono)
                        elif self.type == 1:
                            print('使用褐色')
                            # mono_img = np.squeeze(_mono)
                            res_mono = b_p.process(_mono)
                        print(res_mono)
                    except:
                        # 报警信号
                        # self.errorSignal.emit(['处理黑白异常'])
                        self.getSignal.emit('处理黑白异常')
                        time.sleep(1)
                        os.remove(dir1_path + '/' + mono[0])
                        print('move1')
                        # 线程锁off
                        self.mutex.unlock()
                        continue
                    if res_mono == 1:
                        # 报警信号
                        # self.errorSignal.emit(['处理黑白异常'])
                        time.sleep(1)
                        os.remove(dir1_path + '/' + mono[0])
                        print('move1')
                        # 线程锁off
                        self.mutex.unlock()
                        continue
                    _h = (res_mono[0] + res_mono[1]) / 2 * self.h_delta
                    _w = (res_mono[2] + res_mono[3]) / 2 * self.w_delta
                    tmp_dict['scan_height'] = '%.1f'%max(_h, _w)
                    tmp_dict['scan_width'] = '%.1f'%min(_h, _w)
                    tmp_dict['area'] =' %.1f'%(_h * 0.01 * _w * 0.01)

                    os.remove(dir1_path + '/' + mono[0])
                    print('move1')
                    self.upload.append(tmp_dict)
                    self.getSignal.emit('处理二维码中...')
                    # 二维码处理放在黑白相机中
                    data = [False]
                    # 如果扫描器没有读到码
                    if len(qr_list) == 0:
                        try:
                            data = qr_reader(_mono)
                        except Exception as e:
                            print('--->超时', e)
                            self.getSignal.emit('处理超时')
                            data = [False]
                    else:
                        url = qr_list.pop(0)
                        data = [True, [True, [url]]]
                    print(data)
                    # true：提取到了网址
                    title = 0
                    size1 = size2 = 0
                    if data[0]:
                        # 可能解析不出网址
                        try:
                            print(data[1][1][0])
                            res = get_qr_info(data[1][1][0])
                            print(res)
                            title = res[0]
                            size = res[1][0]
                            # 项目/
                            project = res[2]
                            # self.proSignal.emit(project)

                            # 比较读到的项目名称和cad_name
                            if project != cad_name:
                                # 不一样的话进行查找
                                all_cad = glob.glob('Y:/**/*.dxf', recursive=True)
                                all_img = glob.glob('Y:/**/*.jpg', recursive=True) + glob.glob('Y:/**/*.png',
                                                                                               recursive=True)
                                # 提取出名字
                                _c = [c.split('\\')[-1].split('/')[-1].split('.')[0] for c in all_cad]
                                # 匹配
                                out = process.extract(project, _c, limit=4)
                                print(out)

                                first = out[0][0]
                                print(first)
                                # 得分最高的cad路径
                                new_cad_path = all_cad[_c.index(first)]
                                print('新的CAD路径：', new_cad_path)
                                p = './' + first + '.bmp'
                                # 初始化cad
                                self.cad_path = new_cad_path
                                canvas, x_ao, y_ao, x_do, y_do, text_pt, text_list, _ = init_canvas(self.cad_path)
                                self.canvas = canvas
                                print('重新初始化cad')
                                # 更新给主页面
                                self.updateSignal.emit(self.cad_path)
                                print('主界面更新')
                                # cad的名称更新
                                cad_name = first

                                # 更新图片
                                _img = [c.split('\\')[-1].split('/')[-1].split('.')[0] for c in all_img]
                                out_img = process.extract(project, _img, limit=4)
                                first_img = out_img[0][0]
                                new_img_path = all_img[_img.index(first_img)]
                                self.updateSignal_2.emit(new_img_path)


                            print(title, size)
                            size1 = float(size[0])
                            size2 = float(size[1])
                            # print(f'max:{max(size1, size2)}, min:{min(size1, size2)}')
                            size1, size2 = max(size1, size2), min(size1, size2)
                        except Exception as e:
                            print(e)
                            print('url解析错误')
                            # self.getSignal.emit('网络异常')
                    tmp_dict['qr_height'] = size1
                    tmp_dict['qr_width'] = size2
                    # 更新cad
                    if title != 0 and title in text_list:
                        loc = text_list.index(title)
                        self.loc.append(loc)
                        mono_img = cv2.cvtColor(_mono, cv2.COLOR_GRAY2BGR)
                        handle_dxf(x_ao, y_ao, x_do, y_do, text_pt, text_list, self.canvas, text_list[loc],
                                   paste_img=mono_img, img_path=p)
                        self.cadSignal.emit([1, cad_name])
                        self.getSignal.emit('二维码读取成功')
                    else:
                        self.cadSignal.emit([0, cad_name])
                        self.getSignal.emit('二维码读取失败')
                        if title not in text_list and title != 0:
                            self.getSignal.emit('CAD信息不匹配')

                # 不使用彩色相机
                if len(self.upload) and self.use_color_cam == 0:
                    tmp_dict = self.upload.pop(0)
                    # 弹出就不管了
                    insertdata(
                        tmp_dict['id'],
                        tmp_dict['color_path'],
                        tmp_dict['qr_height'],
                        tmp_dict['qr_width'],
                        tmp_dict['area'],
                        tmp_dict['mono_path'],
                        tmp_dict['scan_height'],
                        tmp_dict['scan_width']
                    )
                    # 通知主进程这一次图像处理完成
                    self.sizeSignal.emit(1)

                # 处理异常的彩色图 1为异常
                if len(color):
                    wrong_color_flag = 0
                    while not wrong_color_flag and len(color):
                        if color[0][-3:] == 'raw':
                            color_img = np.fromfile(dir2_path + '/' + color[0], dtype='uint8')
                            color_img = color_img.reshape(-1, self.color_width, 3)
                            color_img = color_img[[not np.all(color_img[i] == 0) for i in range(color_img.shape[0])], ...]
                            x, y = color_img.shape[: 2]
                            if max(x, y) == 24000:
                                # 删除
                                os.remove(dir2_path + '/' + color[0])
                                color = os.listdir(dir2_path)
                                print('处理彩色异常')
                                self.getSignal.emit('处理彩色异常')
                            else:
                                wrong_color_flag = 1


                # 使用彩色相机
                if len(color) and len(self.upload) and self.use_color_cam == 1:
                    self.getSignal.emit('彩色相机采图')
                    print('move2')
                    tmp_dict = self.upload.pop(0)

                    # 将彩色图像处理并存储
                    if color[0][-3:] == 'raw':
                        color_img = np.fromfile(dir2_path + '/' + color[0], dtype='uint8')
                        color_img = color_img.reshape(-1, self.color_width, 3)
                    else:
                        color_img = cv2.imread(dir2_path + '/' + color[0])
                    _color = color_img.copy()
                    # _color = cv2.resize(_color, dsize=(0, 0), fx=0.1, fy=0.1)
                    # 去除0行
                    _color = _color[[not np.all(_color[i] == 0) for i in range(_color.shape[0])], ...]
                    # 彩色填充CAD
                    if title != 0 and title in text_list:
                        loc = text_list.index(title)
                        handle_dxf(x_ao, y_ao, x_do, y_do, text_pt, text_list, self.canvas, text_list[loc],
                                   paste_img=_color, img_path=p)
                        self.cadSignal.emit([1, cad_name])
                    _path_color = color_path + '/' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.bmp'
                    cv2.imwrite(_path_color, _color)
                    tmp_dict['color_path'] = _path_color

                    # jpg
                    _path_color = _path_color.replace('bmp', 'jpg')
                    x, y = _color.shape[: 2]
                    _color = cv2.resize(_color, (int(y / 10), int(x / 10)))
                    cv2.imwrite(_path_color, _color)

                    cv2.imwrite('D:/tmp/' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.bmp', color_img)

                    insertdata(
                        tmp_dict['id'],
                        tmp_dict['color_path'],
                        tmp_dict['qr_height'],
                        tmp_dict['qr_width'],
                        tmp_dict['area'],
                        tmp_dict['mono_path'],
                        tmp_dict['scan_height'],
                        tmp_dict['scan_width']
                    )
                    os.remove(dir2_path + '/' + color[0])
                    print('move2')
                    # 通知主进程这一次图像处理完成
                    self.sizeSignal.emit(1)

                    # paste_img = cv2.imread(r'D:\stone_detection\color\2023-10-11_16-48-34.jpg')

                    # self.cadSignal.emit([1, cad_name])

            time.sleep(1)
            # 线程锁off
            self.mutex.unlock()


# class InitThread(QThread):
#     initSignal = pyqtSignal(object)
#     errorSignal = pyqtSignal(object)
#
#     def run(self):
#         # 1. 检查基础环境
#         if flag_cam != 0:
#             self.errorSignal.emit(error_code)
#             return
#
#         # 2. 准备配置路径
#         try:
#             mono_ini_path = os.path.normpath(os.path.abspath(cfg['mono_ini']))
#             # 使用 common.trans_ini 里的函数解析文件
#             mono_cmds = ini_file(mono_ini_path)
#         except Exception as e:
#             self.errorSignal.emit([f"读取INI文件失败: {e}"])
#             return
#
#         # 3. 配置串口 (请确认 COM 号是否正确)
#         try:
#             # 增加 timeout 防止程序死锁
#             ser_mono = serial.Serial("COM10", 9600, timeout=1)
#             self.initSignal.emit('开始写入黑白相机参数...')
#
#             for cmd in mono_cmds:
#                 # 预处理命令：移除末尾换行并统一加 \r (相机通用结束符)
#                 clean_cmd = cmd.strip().split('#')[0]  # 移除注释部分
#                 if not clean_cmd: continue
#
#                 final_cmd = clean_cmd + '\r'
#
#                 # 写入串口
#                 ser_mono.write(final_cmd.encode('utf-8'))
#                 print(f"Sending to MONO: {clean_cmd}")
#
#                 # 等待相机响应（握手）
#                 time.sleep(0.2)
#                 res = ser_mono.read_all().decode('utf-8', errors='ignore')
#
#                 if res:
#                     self.initSignal.emit(f"相机返回: {res.strip()}")
#                 else:
#                     # 如果没返回，尝试重发一次
#                     ser_mono.write(final_cmd.encode('utf-8'))
#                     time.sleep(0.5)
#
#             ser_mono.close()
#             self.initSignal.emit('黑白相机参数写入完成')
#
#         except Exception as e:
#             self.errorSignal.emit([f"串口通信故障: {e}"])


class InitThread(QThread):

    initSignal = pyqtSignal(object)
    errorSignal = pyqtSignal(object)

    def __init__(self, parent=None, ID=None):
        super(InitThread, self).__init__(parent)


    def run(self):
        # 相机异常就传递异常值
        if flag_cam != 0:
            self.errorSignal.emit(error_code)
            print(error_code)

        mono_ini_path = cfg['mono_ini']
        color_ini_path = cfg['color_ini']
        mono_ini = ini_file(mono_ini_path)
        color_ini = ini_file(color_ini_path)
        ser_mono = serial.Serial("COM10", 9600)
        ser_color = serial.Serial("COM20", 9600)
        self.initSignal.emit('配置黑白相机')
        for cmd in mono_ini:
            cmd = cmd[: -2] + '\r'
            ser_mono.write(cmd.encode('utf-8'))
            self.initSignal.emit(cmd[: -2])
            print(cmd.encode('utf-8'))
            time.sleep(0.5)
            res = ser_mono.read_all()
            if len(res) == 0:
                ser_mono.write(cmd.encode('utf-8'))
                time.sleep(2)
            print(res)
            self.initSignal.emit(str(res))
        ser_mono.close()
        self.initSignal.emit('配置彩色相机')
        for cmd in color_ini:
            cmd = cmd[: -2] + '\r'
            ser_color.write(cmd.encode('utf-8'))
            self.initSignal.emit(cmd[: -2])
            print(cmd.encode('utf-8'))
            time.sleep(0.5)
            res = ser_color.read_all()
            if len(res) == 0:
                ser_color.write(cmd.encode('utf-8'))
                time.sleep(2)
            print(res)
            self.initSignal.emit(str(res))
        ser_color.close()
        self.initSignal.emit('配置完成')


class CadThread(QThread):

    cadSignal = pyqtSignal(object)

    def __init__(self):
        super(CadThread, self).__init__()

    def run(self):
        canvas, x_ao, y_ao, x_do, y_do, text_pt, text_list = init_canvas()
        self.cadSignal.emit(1)
        paste_img = cv2.imread(r'D:\stone_detection\color\2023-10-11_16-48-34.jpg')
        for t in text_list:
            time.sleep(2)
            handle_dxf(x_ao, y_ao, x_do, y_do, text_pt, text_list, canvas, t, paste_img=paste_img)
            self.cadSignal.emit(1)


# 扫码器x4
class QRThread1(QThread):
    qrSignal = pyqtSignal(object)
    def __init__(self):
        super(QRThread1, self).__init__()
        self.tcp_client_socket_1 = socket(AF_INET, SOCK_STREAM)
        self.server_ip_1 = '192.168.1.240'
        self.server_port = 8849

    def run(self) -> None:
        try:
            self.tcp_client_socket_1.connect((self.server_ip_1, self.server_port))
        except Exception as e:
            print('qr1 error', e)
            self.qrSignal.emit('扫码器1无法连接')
            return
        print('qr1 ready!')
        self.qrSignal.emit('扫码器1已连接')
        while True:
            recvData_1 = self.tcp_client_socket_1.recv(1024)
            if recvData_1 != '':
                url = recvData_1.decode('gbk').replace('\n', '').replace('\r', '')
                print('1_接收到的数据为:', url)
                if url not in qr_list:
                    qr_list.append(url)
            time.sleep(0.1)
            # print(qr_list)

class QRThread2(QThread):
    qrSignal = pyqtSignal(object)
    def __init__(self):
        super(QRThread2, self).__init__()
        self.tcp_client_socket_1 = socket(AF_INET, SOCK_STREAM)
        self.server_ip_1 = '192.168.1.241'
        self.server_port = 8849

    def run(self) -> None:
        try:
            self.tcp_client_socket_1.connect((self.server_ip_1, self.server_port))
        except Exception as e:
            print('qr2 error ', e)
            self.qrSignal.emit('扫码器2无法连接')
            return
        print('qr2 ready!')
        self.qrSignal.emit('扫码器2已连接')
        while True:
            recvData_1 = self.tcp_client_socket_1.recv(1024)
            if recvData_1 != '':
                url = recvData_1.decode('gbk').replace('\n', '').replace('\r', '')
                print('2_接收到的数据为:', url)
                if url not in qr_list:
                    qr_list.append(url)
            time.sleep(0.1)

class QRThread3(QThread):
    qrSignal = pyqtSignal(object)
    def __init__(self):
        super(QRThread3, self).__init__()
        self.tcp_client_socket_1 = socket(AF_INET, SOCK_STREAM)
        self.server_ip_1 = '192.168.1.242'
        self.server_port = 8849

    def run(self) -> None:
        try:
            self.tcp_client_socket_1.connect((self.server_ip_1, self.server_port))
        except Exception as e:
            print('qr3 error ', e)
            self.qrSignal.emit('扫码器3无法连接')
            return
        print('qr3 ready!')
        self.qrSignal.emit('扫码器3已连接')
        while True:
            recvData_1 = self.tcp_client_socket_1.recv(1024)
            if recvData_1 != '':
                url = recvData_1.decode('gbk').replace('\n', '').replace('\r', '')
                print('3_接收到的数据为:', url)
                if url not in qr_list:
                    qr_list.append(url)
            time.sleep(0.1)

class QRThread4(QThread):
    qrSignal = pyqtSignal(object)
    def __init__(self):
        super(QRThread4, self).__init__()
        self.tcp_client_socket_1 = socket(AF_INET, SOCK_STREAM)
        self.server_ip_1 = '192.168.1.243'
        self.server_port = 8849

    def run(self) -> None:
        try:
            self.tcp_client_socket_1.connect((self.server_ip_1, self.server_port))
        except Exception as e:
            print('qr4 error ', e)
            self.qrSignal.emit('扫码器4无法连接')
            return
        print('qr4 ready!')
        self.qrSignal.emit('扫码器4已连接')
        while True:
            recvData_1 = self.tcp_client_socket_1.recv(1024)
            if recvData_1 != '':
                url = recvData_1.decode('gbk').replace('\n', '').replace('\r', '')
                print('4_接收到的数据为:', url)
                if url not in qr_list:
                    qr_list.append(url)
            time.sleep(0.1)

class QRThread5(QThread):
    qrSignal = pyqtSignal(object)
    def __init__(self):
        super(QRThread5, self).__init__()
        self.tcp_client_socket_1 = socket(AF_INET, SOCK_STREAM)
        self.server_ip_1 = '192.168.1.244'
        self.server_port = 8849

    def run(self) -> None:
        try:
            self.tcp_client_socket_1.connect((self.server_ip_1, self.server_port))
        except Exception as e:
            print('qr5 error ', e)
            self.qrSignal.emit('扫码器5无法连接')
            return
        print('qr5 ready!')
        self.qrSignal.emit('扫码器5已连接')
        while True:
            recvData_1 = self.tcp_client_socket_1.recv(1024)
            if recvData_1 != '':
                url = recvData_1.decode('gbk').replace('\n', '').replace('\r', '')
                print('5_接收到的数据为:', url)
                if url not in qr_list:
                    qr_list.append(url)
            time.sleep(0.1)