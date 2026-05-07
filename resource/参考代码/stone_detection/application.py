import os
import faulthandler
faulthandler.enable()
import platform
import subprocess     # 用于执行系统命令
from io import BytesIO   # 用于处理字节流，通常用于从内存中读取或写入数据
from PyQt5.QtGui import QPixmap   # 提供了创建和控制应用界面所需的图形界面功能
import requests       # 用于发送HTTP请求，处理网络通信
from LoginWindow import LoginWindow  #
from common.HardwareController import HardwareController, HardwareControllerUI
from PyQt5 import QtWidgets, QtGui, QtCore  # 提供了创建和控制应用界面所需的图形界面功能
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QHeaderView, QAbstractItemView, QTableWidgetItem, \
    QLabel, QGraphicsScene, QGraphicsPixmapItem, QCheckBox, QWidget, QFileDialog, QMessageBox, QComboBox, QButtonGroup  # 提供了创建和控制应用界面所需的图形界面功能
from PyQt5.QtWidgets import QFileDialog   # 提供文件对话框功能
from PyQt5.QtCore import QDate, QTimer  # 提供了核心的非GUI功能，如时间和日期处理
import sys   # 提供对Python解释器使用或维护的一些变量和函数的访问
from interface import Ui_MainWindow  # 导入用户界面类
import cv2
import time

from my_thread import *    # 导入自定义线程模块

from common.dbFunction import *   # 导入数据库功能模块
from PIL import Image   # 用于图像处理
from common.my_html import *  # 导入自定义HTML处理模块
from selenium import webdriver   # 用于自动化浏览器操作
from selenium.webdriver.edge.options import Options  # 用于配置Edge浏览器选项
import pyautogui
from common.cloud_sever import upload   # 导入云服务器上传功能
from tip import Ui_Tip   # 导入提示窗口类
import src_rc
import traceback   # 用于捕获和打印异常信息，帮助调试程序
from PIL import ImageFile
import json  # 用于处理JSON数据
import glob  # 用于查找符合特定规则的文件路径名，常用于批量处理文件
from common.MainIntegration import MainHardwareIntegration    # 导入主硬件集成模块
from tempfile import NamedTemporaryFile

ImageFile.LOAD_TRUNCATED_IMAGES = True # 允许加载截断的图像文件
Image.MAX_IMAGE_PIXELS = None   # 取消图像像素限制，防止处理大图时出现错误
LOG_FILE_PATH = "log"  # 日志文件目录
LOG_USER_PATH = "log_user_management.txt"

# 指定量尺图片临时下载目录
download_dir = "temp_images"
os.makedirs(download_dir, exist_ok=True)  # 如果目录不存在就创建

# 用于记录用户操作的日志
def log_user_action(username: str, action_type: str, target_user: str = None, result: str = None):
    """
    简单写日志到 log.txt
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_info = f"Target: {target_user}" if target_user else "Target: None"
    log_line = f"[{timestamp}] User: {username}, Action: {action_type}, {target_info}, Result: {result}\n"
    with open(os.path.join(LOG_FILE_PATH, LOG_USER_PATH), "a", encoding="utf-8") as f:
        f.write(log_line)

# 同时继承自 PyQt 的 QMainWindow（提供窗口行为和事件处理）和由 Qt Designer 生成的 Ui_MainWindow（只包含 setupUi(self) 等界面布局方法）。
# 通常做法是继承两者后在构造函数里调用 setupUi(self) 把界面元素安装到 QMainWindow 实例上。
# 注意：构造函数里应用 super().__init__() 来正确初始化父类（目前代码里 super(QMainWindow, self).__init__() 是不对的，会导致初始化顺序问题）。示例如下：#
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, current_user=None, current_user_role=None):
        super(QMainWindow, self).__init__()
        self.current_user = current_user
        self.current_user_role = current_user_role
        # 【登录页面】
        print("执行Window类初始化....")
        self.setWindowTitle("登录 / 注册 / 修改密码")
        self.setGeometry(600, 300, 400, 250)
        print("Window类初始化完成....")
        self.setupUi(self)  # 用 self.setupUi(self) 把 Designer 生成的界面绑定到当前窗口实例，再初始化 cad_img_path。
        # 不要立即执行，给 UI 一点渲染时间，防止初始化崩溃导致窗口闪现
        QTimer.singleShot(500, self.init_hardware_integration)
        # 1. 硬件控制页面
        # 初始化硬件控制集成模块
        self.init_hardware_integration()
        # 可选：添加一些额外的业务逻辑初始化
        self.init_business_logic()

        # cad图片
        self.cad_img_path = None
        # 面积统计/片数统计，默认前者
        self.area_num = 1
        # 原始图片/量尺图片，默认前者
        self.raw_measure = 1
        # sql数据
        self.datas = []
        # 首页
        self.stackedWidget.setCurrentIndex(0)
        self.beautification()
        self.init_data()
        # 是否启动了扫描
        self.scan = False
        # 当前选中的行
        self.row_selected = None

        # 看门狗
        self.watch_dog = WatchDogThread(ID=len(self.datas))
        self.watch_dog.start()
        self.start_n = 0
        # 用于记录有没有start过

        # 初始化
        self.ini_cam = InitThread()

        # qr1
        try:
            self.qr1 = QRThread1()
            self.qr1.start()
            self.qr2 = QRThread2()
            self.qr2.start()
            self.qr3 = QRThread3()
            self.qr3.start()
            self.qr4 = QRThread4()
            self.qr4.start()
            self.qr5 = QRThread5()
            self.qr5.start()
        except Exception as e:
            print('qr: ', e)

        # cad
        # self.cad_t = CadThread()
        # self.cad_t.start()

        # 状态
        self.scanStatusLabel.setText(
            "<html><head/><body><p>当前状态：&nbsp; <span style=\" color:rgb(0, 0, 255);\">{}</span></p></body></html>".format(
                '停止中'))

        self.signal_connect()

        # self.ini_cam.start()
        # 读取配置文件
        with open('configs/cfg.json', 'r') as f:
            self.cfg = json.load(f)
            f.close()
        self.mono_vlcf = self.cfg['mono_vlcf']
        self.mono_ini = self.cfg['mono_ini']
        self.color_vlcf = self.cfg['color_vlcf']
        self.color_ini = self.cfg['color_ini']
        self.show_setting()

        self.use_color = self.cfg['color_cam']
        # 不使用彩色相机
        if self.use_color == 0:
            self.watch_dog.use_color_cam = 0
            self.pushButton.setText('打开')
        else:
            self.pushButton.setText('关闭')
        # 设置一个cad_path，如果没有选择，不允许开始扫描
        # cad_path需要传参给watch dog
        # none--》现在给一个默认值
        self.cad_path = 'C:/Users/Administrator/Desktop/1017/测试CAD.dxf'
        if not os.path.exists(self.cad_path):
            print('default cad error!')
            self.cad_path = None
        # self.watch_dog.cad_path = self.cad_path

        # 加载用户信息
        self.load_user_table()

        # 根据用户权限判断是否能查看用户信息
        if self.current_user_role not in ('superadmin', 'admin'):
            self.userCtlBtn.setDisabled(True)  # 禁用按钮，用户无法点击
            self.userCtlBtn.setToolTip("您没有权限访问用户信息页面")
        else:
            self.userCtlBtn.setDisabled(False)  # 超级管理员或管理员可以使用

        # 【缺陷检测】每隔 3 秒刷新一次缺陷数据
        self.defect_refresh_timer = QTimer(self)
        self.defect_refresh_timer.timeout.connect(self.populate_defect_page)
        self.defect_refresh_timer.start(3000)  # 3000 毫秒 = 3 秒

        # 【切割数据】
        # 1️⃣ 设置初始日期
        today = datetime.today()
        self.cutStartDateEdit.setDate(QDate(2025, 9, 1))  # 默认2025, 9, 1
        self.cutEndDateEdit.setDate(QDate(today.year, today.month, today.day))  # 默认今天
        self.scanStartDateEdit.setDate(QDate(2025, 9, 1))  # 默认2025, 9, 1
        self.scanEndDateEdit.setDate(QDate(today.year, today.month, today.day))  # 默认今天

        # 【切割数据】初始化
        self.query_cutting_data()

        # 【界面初始化】
        # 需要互斥的按钮
        buttons = [
            self.homeBtn, self.hardwareCtrlBtn, self.cutDataBtn, self.scanDataBtn,
            self.cadBtn, self.defectDetectBtn, self.settingsBtn, self.userCtlBtn
        ]

        # 设置可选中
        self.homeBtn.setCheckable(True)

        # 创建互斥组
        self.group = QButtonGroup(self)      # 确保在同一时间只有一个按钮处于选中状态。
        self.group.setExclusive(True)
        for btn in buttons:
            self.group.addButton(btn)

        self.on_scan_start_date_changed()
        self.on_cut_start_date_changed()

        self.load_table_data()

        # 调用动态生成看板方法
        self.inject_scanner_ui()

    # 该函数把界面控件的信号（事件）连接到对应的处理函数（槽），使用户交互能触发程序逻辑。
    def signal_connect(self):

        # 【扫描数据页面】
        self.scanQueryBtn.clicked.connect(self.load_table_data)
        self.scanResetBtn.clicked.connect(self.on_scan_start_date_changed)
        self.scanStartDateEdit.dateChanged.connect(self.on_scan_start_date_changed)
        self.scanDataTable.cellClicked.connect(self.on_scan_table_row_selected)
        self.scanOriginalBtn.clicked.connect(lambda: self.refresh_scan_image("original"))
        self.scanRulerBtn.clicked.connect(lambda: self.refresh_scan_image("ruler"))

        # 点击事件获取所选内容、行列
        self.scanDataTable.cellPressed.connect(self.show_pic)
        self.scanViewLargeBtn.clicked.connect(self.on_scan_view_large)

        self.scanRulerBtn.clicked.connect(lambda: self.button_switch(1))
        self.scanOriginalBtn.clicked.connect(lambda: self.button_switch(2))
        self.areaStatsTBtn.clicked.connect(lambda: self.button_switch("area"))
        self.countStatsTBtn.clicked.connect(lambda: self.button_switch("count"))
        # 打印
        # self.toolButton_23.clicked.connect(self.printer)
        # 开始扫描
        self.scanStartBtn.clicked.connect(lambda: self.button_switch(5))
        # 切换页面
        # self.toolButton_28.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # 【用户信息页面】
        self.deleUserInfoTBtn.clicked.connect(self.on_delete_user_clicked)
        self.refreshUserInfoTBtn.clicked.connect(self.load_user_table)
        self.updateUserInfoTBtn.clicked.connect(self.on_update_user_clicked)

        # 【切割数据页面】
        self.cutDataQueryTBtn.clicked.connect(self.query_cutting_data)
        self.dateResetTBtn.clicked.connect(self.reset_date_range)
        self.cutStartDateEdit.dateChanged.connect(self.on_cut_start_date_changed)

        self.homeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.hardwareCtrlBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.cutDataBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.scanDataBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.cadBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.defectDetectBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.settingsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.userCtlBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.closeBtn.clicked.connect(self.close)

        # CAD页面空间绑定(懒得改昵称了，耗子尾汁 = = )

        # 上传
        # self.toolButton_24.clicked.connect(self.select2upload)
        # 更改图片
        self.toolButton_7.clicked.connect(self.show_cad)
        # 更改cad
        self.toolButton_10.clicked.connect(self.select_cad)
        # cad大图
        self.toolButton_6.clicked.connect(self.open_cad_img)

        # self.watch_dog.cadSignal.connect(self.simulation_cad)

        # 设置
        self.toolButton_11.clicked.connect(lambda: self.modify_setting(0))
        self.toolButton_12.clicked.connect(lambda: self.modify_setting(1))
        self.toolButton_14.clicked.connect(lambda: self.modify_setting(2))
        self.toolButton_13.clicked.connect(lambda: self.modify_setting(3))
        self.toolButton.clicked.connect(lambda: self.modify_setting(4))
        # 打开文件夹
        self.toolButton_8.clicked.connect(lambda: os.startfile('D:/stone_detection/color'))
        # 彩色相机开关
        self.pushButton.clicked.connect(self.change_color_status)
        # 重置cadn
        self.toolButton_15.clicked.connect(self.del_cad_bmp)
        self.pushButton_2.clicked.connect(lambda: self.ini_cam.start())
        # 查看绘制的cad
        self.toolButton_16.clicked.connect(self.open_canvas)

        # 【硬件控制页面】
        self.connect_all_btn.clicked.connect(self.quick_start_all_hardware)
        self.disconnect_all_btn.clicked.connect(self.emergency_stop_all_hardware)


    # 初始化【扫描页面】数据信息
    def init_data(self):

        if self.areaStatsTBtn.isChecked():
            # 如果area面积统计按钮为checked
            result = get_scan_areas()
            today = result["today_area"] or 0
            total = result["total_area"] or 0
            self.totalScanLabel.setText(str(total) + "m²")
            self.todayScanLabel.setText(str(today) + "m²")
        else:
            result = get_scan_counts()
            today = result["today_count"] or 0
            total = result["total_count"] or 0
            self.totalScanLabel.setText(str(total) + "片")
            self.todayScanLabel.setText(str(today) + "片")

    # 美化
    # 列宽根据内容自动调整，可以用resizeColumnsToContents()；
    def beautification(self):
        self.scanDataTable.verticalHeader().setDefaultSectionSize(200)
        self.scanDataTable.setColumnWidth(2, 300)
        self.scanDataTable.setColumnWidth(3, 150)
        self.scanDataTable.setColumnWidth(4, 150)

    # self.datas中放置的是数据库查询出来的数据
    # self.raw_measure
    def show_pic(self, row, col):
        self.row_selected = row
        if row >= len(self.datas):
            return

        scene = QGraphicsScene()
        if self.raw_measure == 2:
            # print(self.datas[row][8])
            # print(os.path.exists(self.datas[row][8]))
            pix = QtGui.QPixmap(self.datas[row][8]).scaled(self.graphicsView.size(), aspectRatioMode=Qt.KeepAspectRatio)

        elif self.raw_measure == 1:
            # print(self.datas[row][1])
            pix = QtGui.QPixmap(self.datas[row][1]).scaled(self.graphicsView.size(), aspectRatioMode=Qt.KeepAspectRatio)

        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)
        self.graphicsView.setScene(scene)

    # 打印
    # 此方法把self.datas转成HTML报表、用Edge打开该本地HTML文件并触发打印（Ctrl + P），实现打印预览 / 打印自动化。
    def printer(self):
        if self.datas is None or len(self.datas) == 0:
            return
        html_data = []
        img_src = "<img src = {} width=300px height=200px>"  # 定义了一个 HTML 图片标签的模板字符串，其中的 {} 是一个占位符，将在后续循环中被图片路径替换。
        for rowIndex, row in enumerate(self.datas):
            html_row = []
            for columnIndex, item in enumerate(row):
                if columnIndex == 0:                   #
                    item = '已上传' if item == 1 else '未上传'
                # 将原始数据（预期为图片路径）插入到预定义的 img_src HTML 模板中，使其成为一个完整的 HTML 图片标签。
                elif columnIndex == 1:                # 图片路径
                    item = img_src.format(item)
                elif columnIndex == 3:               # 扫描时间
                    item = str(item).split('.')[0]  # 将数据转换为字符串，并使用 .split('.')[0] 移除小数点及其后的部分通常用于清除时间戳中的毫秒
                elif columnIndex >= 8:                 # 数据筛选
                    continue
                html_row.append(str(item))
            html_row = tuple(html_row)
            html_data.append(html_row)
        html_data = tuple(html_data)
        print(html_data)
        header_data = (("上传状态", "图片", "编码", "扫描时间", "长", "宽", "二维码长", "二维码宽"),)
        title = '测试报告' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        html = HtmlTableApi(
            title=title,
            header_data=header_data,
            rows_data=html_data
        ) # 创建一个 HtmlTableApi 类的实例，传入报告标题、表头数据和格式化后的行数据
        html.setAllStyle()
        html.createHtml()
        # 这段代码使用自动化工具打开生成的HTML文件，并模拟键盘操作触发打印功能。
        edge_options = Options()
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        edge_options.add_experimental_option("detach", True)
        driver = webdriver.Edge(options=edge_options)
        driver.get(f'file://D:/石材检测/结果/{title}.html')
        time.sleep(1)
        pyautogui.keyDown('esc')
        pyautogui.keyUp('esc')
        pyautogui.keyDown('esc')
        pyautogui.keyUp('esc')
        pyautogui.hotkey('ctrl', 'p')       # 在大多数浏览器中触发打印对话框的标准操作

    # 这段 Python 代码定义了一个名为 button_switch 的方法，它根据传入的 flag 参数（通常由用户界面的按钮点击触发）来执行不同的操作，/
    # 主要是切换按钮状态（样式/选中状态）、更新内部变量，以及控制一个名为 watch_dog 的扫描任务的启动、停止和暂停。
    def button_switch(self, flag=None):
        # 量尺按钮
        if flag == 1:
            self.raw_measure = 2
            self.scanRulerBtn.setStyleSheet(
                '#scanRulerBtn{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.scanOriginalBtn.setStyleSheet(
                '#scanOriginalBtn{border-radius: 10px; border: 2px groove gray;border-style: outset}')
        # 原始图片
        elif flag == 2:
            self.raw_measure = 1
            self.scanOriginalBtn.setStyleSheet(
                '#scanOriginalBtn{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.scanRulerBtn.setStyleSheet(
                '#scanRulerBtn{border-radius: 10px; border: 2px groove gray;border-style: outset}')
        elif flag == "area":
            self.areaStatsTBtn.setChecked(True)
            self.countStatsTBtn.setChecked(False)
            self.init_data()    #  调用 init_data 方法，可能用于重置或重新加载数据以适应新的统计模式
        elif flag == "count":
            self.countStatsTBtn.setChecked(True)
            self.areaStatsTBtn.setChecked(False)
            self.init_data()
        # 扫描
        elif flag == 5:
            if self.scan is False:
                # if self.comboBox_3.currentIndex() == -1:
                #     self.tip_win = TipWin()
                #     self.tip_win.label.setText('没有选择石材类型！')
                #     self.tip_win.show()
                #     return
                if self.cad_path is None:
                    self.tip_win = TipWin()
                    self.tip_win.label.setText('没有选择CAD文件！')
                    self.tip_win.show()
                    return
                self.scan = True      # 设置扫描状态变量为 True（表示开始扫描）。
                # 传入检测类别
                # self.watch_dog.type = self.comboBox_3.currentIndex()
                self.watch_dog.type = 1   # 设置扫描任务对象 watch_dog 的类型为 1
                # 继续
                if self.start_n == 0:
                    self.watch_dog.start()   #  调用watch_dog对象的start方法（首次启动线程）。
                    self.start_n += 1
                else:
                    self.watch_dog.resume()
                self.scanStatusLabel.setText(
                    "<html><head/><body><p>当前状态：&nbsp; <span style=\" color:rgb(255, 0, 0);\">{}</span></p></body></html>".format(
                        '扫描中'))
                self.scanStartBtn.setText('停止扫描')
                self.write_logger('启动扫描')
                self.scanStartBtn.setStyleSheet(
                    '#scanStartBtn{background-color: rgb(255, 40, 40);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            else:
                self.scanStatusLabel.setText(
                    "<html><head/><body><p>当前状态：&nbsp; <span style=\" color:rgb(0, 0, 255);\">{}</span></p></body></html>".format(
                        '停止中'))
                self.scan = False
                # 暂停
                self.watch_dog.pause()
                self.scanStartBtn.setText('启动扫描')
                self.write_logger('停止扫描')
                self.scanStartBtn.setStyleSheet(
                    '#scanStartBtn{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')

    def show_raw_pic(self, row, col):
        if row >= len(self.datas):
            return

    def write_logger(self, msg):
        self.scanLogBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S-------->', time.localtime()) + msg + '\n')

    def closeEvent(self, event):
        # 不够暴力
        # sys.exit(0)
        # 暴力杀死进程
        os._exit(0)

    # 重置CAD  主要功能是删除与 CAD 文件同名的 BMP 图像文件（如果存在），并重新初始化和加载 CAD 图像到用户界面。
    def del_cad_bmp(self):
        cad_name = self.cad_path.split('/')[-1].split('\\')[-1].split('.')[0]
        p = './' + cad_name + '.bmp'
        # 存在即重置
        if os.path.exists(p):
            os.remove(p)
            init_canvas(self.cad_path)
            self.simulation_cad([1, cad_name])

    # 显示相机异常的提示
    def showError(self, cnt):
        # print(12345)
        content = '相机错误\n'
        for c in cnt:
            content += c
        content += '请检查后重启软件！'
        self.tip_win = TipWin()    # 显然是一个自定义的提示窗口类
        self.tip_win.label.setText(content)
        self.tip_win.show()

    # 选择CAD
    def select_cad(self):
        if self.scan is True:
            # 在停止扫描时可以选择
            self.tip_win = TipWin()
            self.tip_win.label.setText('请先停止扫描!')
            self.tip_win.show()
            return
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取CAD文件",
                                                            "C:/Users/Administrator/Desktop/1017/",
                                                            "CAD Files (*.dxf)")   # 第一个参数是父窗口，第二个是对话框的标题。  # 指定了文件对话框打开时的默认初始目录。 #指定了文件过滤器，用户只能选择扩展名为 .dxf 的 CAD 文件。
        if ok:
            print(get_filename_path)
            self.label_4.setText('当前CAD文件：' + get_filename_path)
            self.cad_path = get_filename_path
            # 传参给watch dog
            self.watch_dog.cad_path = self.cad_path
            cad_name = self.cad_path.split('/')[-1].split('.')[0]
            p = './' + cad_name + '.bmp'
            # 不存在的话要新建
            if os.path.exists(p) is False:
                print('新建画布')
                init_canvas(self.cad_path)
            self.simulation_cad([1, cad_name])

    # 自动查询cad
    def search_cad(self, pro):
        all_cad = glob.glob('Y:/**/*.dxf', recursive=True)
        all_img = glob.glob('Y:/**/*.jpg', recursive=True) + glob.glob('Y:/**/*.png', recursive=True)
        find_cad = 0
        for cad in all_cad:
            if pro in cad:
                print('find!')
                find_cad = 1
        if find_cad == 0:
            print('not found')

    # 显示扫描CAD
    def show_cad(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                            "选取图片",
                                                            "C:/Users/Administrator/Desktop/1017/",
                                                            "Image Files (*.png *.jpeg *.jpg *.bmp)")
        if ok:
            self.cad_img_path = get_filename_path
            # 加载、缩放图片并创建场景
            scene = QGraphicsScene()
            pix = QtGui.QPixmap(self.cad_img_path).scaled(self.graphicsView_3.size(),
                                                          aspectRatioMode=Qt.KeepAspectRatio)    # self.graphicsView_3在哪里定义？
            item = QGraphicsPixmapItem(pix)
            scene.addItem(item)
            self.graphicsView_3.setScene(scene)

    # 展示cad大图
    def open_cad_img(self):
        if self.cad_img_path is not None:
            os.startfile(self.cad_img_path)
        else:
            self.tip_win = TipWin()
            self.tip_win.label.setText('没有选择图片！')
            self.tip_win.show()

    # 展示绘制的cad
    def open_canvas(self):
        if self.cad_path is not None:
            try:
                cad_name = self.cad_path.split('/')[-1].split('\\')[-1].split('.')[0]
                p = 'D:/app_24/stone_detection/stone_detection/' + cad_name + '.bmp'
                os.startfile(p)
            except Exception as e:
                print(e)

    # 模拟cad更新
    # op 很可能是一个列表，其中 op[1] 存储了 CAD 文件的纯文件名（不带扩展名）。
    def  simulation_cad(self, op):
        # if op[0] == 0:
        #     # 二维码读取失败
        #     self.tip_win = TipWin()
        #     self.tip_win.label.setText('二维码读取失败')
        #     self.tip_win.show()
        scene = QGraphicsScene()   # 在 Qt 图形视图框架中，QGraphicsScene 是一个容器，管理所有图形项（如图像、文本、线条等）。
        # 显示模拟图需要传入cad名字
        # 构造要加载的 BMP 图像文件的完整路径 p。它使用传入的纯文件名 op[1]，并在前面加上 ./（当前目录），后面加上 .bmp 扩展名。
        p = './' + op[1] + '.bmp'

        pix = QtGui.QPixmap(p).scaled(self.graphicsView_4.size(), aspectRatioMode=Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)
        self.graphicsView_4.setScene(scene)    # 将场景设置到视图,从而在界面上显示图像。

    # 从watchdog更新的cad
    def update_cad(self, cad):
        self.cad_path = cad
        self.label_4.setText('当前CAD文件：' + self.cad_path)

    # 从watchdog更新img
    def update_img(self, img_path):
        if self.cad_img_path == img_path:
            return
        self.cad_img_path = img_path
        scene = QGraphicsScene()
        pix = QtGui.QPixmap(self.cad_img_path).scaled(self.graphicsView_3.size(), aspectRatioMode=Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)
        self.graphicsView_3.setScene(scene)

    # 显示设置  作用是将相机或视觉系统的配置文件的路径显示到用户界面的特定标签（Label）控件上。
    def show_setting(self):
        self.label_6.setText('vlcf文件：' + self.mono_vlcf)
        self.label_9.setText('vlcf文件：' + self.color_vlcf)
        self.label_7.setText('ini文件：' + self.mono_ini)
        self.label_10.setText('ini文件：' + self.color_ini)

    # 更改彩色相机使用
    def change_color_status(self):
        if self.use_color == 0:
            self.use_color = 1
            self.pushButton.setText('关闭')
        elif self.use_color == 1:
            self.use_color = 0
            self.pushButton.setText('打开')
        self.watch_dog.use_color_cam = self.use_color

    # 修改设置 根据操作码 op 引导用户选择不同的配置文件（.vlcf 或 .ini），更新 UI 标签和内部变量，并在用户选择保存时将这些配置写入本地 JSON 文件。
    def modify_setting(self, op):
        if op == 0 or op == 2:
            get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                                "选取vlcf文件",
                                                                "D:/",
                                                                "vlcf Files (*.vlcf)")
            if ok:
                print(get_filename_path)
                if op == 0:
                    self.label_6.setText('vlcf文件：' + get_filename_path)
                    self.mono_vlcf = get_filename_path
                elif op == 2:
                    self.label_9.setText('vlcf文件：' + get_filename_path)
                    self.color_vlcf = get_filename_path

        if op == 1 or op == 3:
            get_filename_path, ok = QFileDialog.getOpenFileName(self,
                                                                "选取ini文件",
                                                                "D:/",
                                                                "ini Files (*.ini)")
            if ok:
                print(get_filename_path)
                if op == 1:
                    self.label_7.setText('ini文件：' + get_filename_path)
                    self.mono_ini = get_filename_path
                elif op == 3:
                    self.label_10.setText('ini文件：' + get_filename_path)
                    self.color_ini = get_filename_path

        # 保存 将所有最新的配置路径和彩色相机使用状态 (self.use_color) 赋值给配置字典 self.cfg。
        if op == 4:
            self.cfg['mono_vlcf'] = self.mono_vlcf
            self.cfg['mono_ini'] = self.mono_ini
            self.cfg['color_vlcf'] = self.color_vlcf
            self.cfg['color_ini'] = self.color_ini
            self.cfg['color_cam'] = self.use_color
            with open('configs/cfg.json', 'w') as f:
                json.dump(self.cfg, f, indent=4)
                f.close()
            self.tip_win = TipWin()
            self.tip_win.label.setText('重启软件后生效！')
            self.tip_win.show()

    def init_hardware_integration(self):
        """初始化硬件控制集成"""
        try:
            # 创建硬件集成实例
            self.hardware_integration = MainHardwareIntegration(self)   # 将 self（即主应用程序或主窗口实例）作为参数传递给 MainHardwareIntegration 的构造函数。这通常是为了让硬件模块能够访问或回调主程序中的方法和属性。

            # 可选：设置定时器来定期检查设备状态
            self.status_check_timer = QTimer()
            self.status_check_timer.timeout.connect(self.periodic_status_check)
            self.status_check_timer.start(30000)  # 每30秒检查一次状态

            print("硬件控制模块集成成功")

        except Exception as e:
            print(f"硬件控制模块集成失败: {e}")
            # 可以选择是否继续运行程序或退出

    def init_business_logic(self):
        """初始化业务逻辑"""
        # 这里可以添加你的业务逻辑初始化代码
        # 比如：数据库连接、配置加载等
        pass

    def periodic_status_check(self):
        """定期状态检查"""
        try:
            status = self.hardware_integration.get_device_status()
            print(f"设备状态检查: {status}")

            # 可以根据状态做一些自动化操作
            # 比如：如果连接断开，自动尝试重连等

        except Exception as e:
            print(f"状态检查异常: {e}")

    # 居中表格中的数据
    def center_table_data(self, tableName: str):
        # 扫描数据表格
        for row in range(tableName.rowCount()):
            for col in range(tableName.columnCount()):
                item = tableName.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

    # ==================== 扫描数据页面业务代码 ================

    # 【扫描数据页面】查看大图
    def on_scan_view_large(self):
        cid = getattr(self, "current_scan_composite_identifier", None)   # 获取当前选中的数据行标识符 (cid)
        if not cid:
            QMessageBox.warning(self, "提示", "未选中行！")
            return

        urls = query_image_urls(cid)
        if not urls:
            QMessageBox.warning(self, "提示", "图片不存在！")
            return

        # 根据按钮选择要打开的图片
        file_path = None
        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                file_path = local_path
            else:
                QMessageBox.warning(self, "提示", "图片不存在！")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            # 量尺图片是网络图片，需要先下载到临时文件

            try:
                import requests
                from tempfile import NamedTemporaryFile
                response = requests.get(url)        # 发送 HTTP GET 请求下载图片内容。
                temp_file = NamedTemporaryFile(delete=False, dir=download_dir, suffix=".png")
                temp_file.write(response.content)
                temp_file.close()
                file_path = temp_file.name
            except Exception as e:
                print(f"下载量尺图片失败: {e}")
                return

        if file_path:
            # 调用系统默认图片查看器打开
            if platform.system() == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            elif platform.system() == "Windows":  # Windows
                os.startfile(file_path)
            else:  # Linux
                subprocess.call(["xdg-open", file_path])

    # 【扫描数据页面】根据按钮显示量尺、原始图片按钮
    def refresh_scan_image(self, type: str):
        # 设置按钮状态
        if type == "original":
            self.scanOriginalBtn.setChecked(True)
            self.scanRulerBtn.setChecked(False)
        elif type == "ruler":
            self.scanOriginalBtn.setChecked(False)
            self.scanRulerBtn.setChecked(True)

        # 直接读取 self.current_scan_composite_identifier
        cid = getattr(self, "current_scan_composite_identifier", None)
        if not cid:
            self.scanPicView.setScene(QGraphicsScene())
            return

        urls = query_image_urls(cid)  # 调用外部函数查询数据库，获取该 cid 对应的图片 URL/本地路径字典。
        if not urls:
            print(f"{cid} 未找到对应图片")
            self.scanPicView.setScene(QGraphicsScene())
            return

        pixmap = None
        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                pixmap = QPixmap(local_path)
            else:
                print(f"原始图片路径不存在: {local_path}")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            try:
                response = requests.get(url)
                img_data = BytesIO(response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(img_data.read())
            except Exception as e:
                print(f"加载量尺图片失败: {e}")

        # 显示到 QGraphicsView
        scene = QGraphicsScene()
        if pixmap:
            pixmap = pixmap.scaled(
                self.scanPicView.width(), self.scanPicView.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            scene.addPixmap(pixmap)
        self.scanPicView.setScene(scene)

    # 【扫描数据页面】根据表格选中行显示量尺、原始数据
    def on_scan_table_row_selected(self, row, column):
        # 获取 composite_identifier（和之前一样）
        production_order_number = self.scanDataTable.item(row, 1).text()
        number = self.scanDataTable.item(row, 2).text()
        composite_identifier = f"{production_order_number}{number}"
        self.current_scan_composite_identifier = composite_identifier  # ✅ 必须加上
        self.refresh_scan_image("original" if self.scanOriginalBtn.isChecked() else "ruler")

        urls = query_image_urls(composite_identifier)
        if not urls:
            print(f"{composite_identifier} 未找到对应图片")
            # 清空 QGraphicsView
            scene = QGraphicsScene()
            self.scanPicView.setScene(scene)
            return

        pixmap = None

        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                pixmap = QPixmap(local_path)
            else:
                print(f"原始图片路径不存在: {local_path}")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            try:
                response = requests.get(url)
                img_data = BytesIO(response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(img_data.read())   # 从内存数据中加载图片，而不是从文件路径加载。
            except Exception as e:
                print(f"加载量尺图片失败: {e}")

        # 显示到 QGraphicsView
        scene = QGraphicsScene()
        if pixmap:
            # 按比例缩放适应 QGraphicsView 尺寸
            view_width = self.scanPicView.width()
            view_height = self.scanPicView.height()
            pixmap = pixmap.scaled(view_width, view_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scene.addPixmap(pixmap)
        self.scanPicView.setScene(scene)

    # 【扫描数据页面】时间范围查询扫描数据并展示
    def load_table_data(self):
        """
        查询数据库并填充到 scanDataTable
        """
        # 获取时间范围
        start_time = self.scanStartDateEdit.date().toString("yyyy-MM-dd")  + " 00:00:00"
        end_time = self.scanEndDateEdit.date().toString("yyyy-MM-dd")  + " 23:59:59"

        # 查询数据库
        results = query_stone_measurements(start_time, end_time)

        # 设置表格行数
        self.scanDataTable.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            # -------- 1. 图片列 --------
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            # 检查数据库返回的数据中是否有原始图片 URL 并且该本地文件确实存在。
            if row["original_url"] and os.path.exists(row["original_url"]):
                pixmap = QPixmap(row["original_url"]).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                img_label.setPixmap(pixmap)
            else:
                img_label.setText("无图片")
            self.scanDataTable.setCellWidget(row_idx, 0, img_label)

            # -------- 2. 单号 --------
            self.scanDataTable.setItem(row_idx, 1, QTableWidgetItem(str(row["production_order_number"])))

            # -------- 3. ID（编号前缀 + 编号）--------
            id_value = (row["number_prefix"] or "") + str(row["number"])
            self.scanDataTable.setItem(row_idx, 2, QTableWidgetItem(id_value))

            # -------- 4. 长 --------
            self.scanDataTable.setItem(row_idx, 3, QTableWidgetItem(str(row["design_length"])))

            # -------- 5. 宽 --------
            self.scanDataTable.setItem(row_idx, 4, QTableWidgetItem(str(row["design_width"])))

            # -------- 6. 扫描长 --------
            self.scanDataTable.setItem(row_idx, 5, QTableWidgetItem(str(row["scan_length"])))

            # -------- 7. 扫描宽 --------
            self.scanDataTable.setItem(row_idx, 6, QTableWidgetItem(str(row["scan_width"])))

            # -------- 8. 扫描时间 --------
            self.scanDataTable.setItem(row_idx, 7, QTableWidgetItem(str(row["scan_time"])))

        # 自适应列宽
        self.scanDataTable.resizeColumnsToContents()
        self.scanDataTable.resizeRowsToContents()
        for col_idx in range(1, self.scanDataTable.columnCount()):
            self.scanDataTable.setColumnWidth(col_idx, 100)  # 从第二列开始固定宽度

        # 居中内容
        self.center_table_data(self.scanDataTable)

    # 【扫描数据】重置按钮
    def on_scan_start_date_changed(self):
        self.scanEndDateEdit.setMinimumDate(self.scanStartDateEdit.date())

    # ==================== 切割数据页面业务代码 =================
    # 【切割数据】cutStartDateEdit 改变时，动态更新 cutEndDateEdit 的最小值
    def on_cut_start_date_changed(self):
        self.cutEndDateEdit.setMinimumDate(self.cutStartDateEdit.date())

    # 【切割数据】查询日期重置
    def reset_date_range(self):
        """将日期重置：起始2025-09-01，结束今天"""
        self.cutStartDateEdit.setDate(QDate(2025, 9, 1))
        today = datetime.today()
        self.cutEndDateEdit.setDate(QDate(today.year, today.month, today.day))

    # 【切割数据】根据时间范围查询切割数据
    def query_cutting_data(self):
        """根据时间范围查询切割数据并填充表格"""
        start_date = self.cutStartDateEdit.date().toString("yyyy-MM-dd") + " 00:00:00"
        end_date = self.cutEndDateEdit.date().toString("yyyy-MM-dd") + " 23:59:59"

        # 调用查询函数
        records = get_cutting_records(start_date, end_date)

        # 设置表格行数
        self.cutDataTable.setRowCount(len(records))

        # 设置表格内容
        for row_idx, rec in enumerate(records):
            items = [
                rec.get("operator_fullname", ""),
                rec.get("project_name", ""),
                rec.get("length", 0),
                rec.get("width", 0),
                rec.get("thickness", 0),
                rec.get("cutting_meters", 0),
                rec.get("square_area", 0),
                rec.get("cutting_status", ""),
                str(rec.get("cutting_time", "")) if rec.get("cutting_time") else "",
                rec.get("drawing_number", ""),
                rec.get("box_number", "")
            ]
            for col_idx, value in enumerate(items):
                item = QTableWidgetItem(str(value))
                self.cutDataTable.setItem(row_idx, col_idx, item)
        # 居中表格数据
        self.center_table_data(self.cutDataTable)

    # ==================== 用户信息页面业务代码 =================

    # 日志记录

    # 【用户信息】加载/刷新用户数据
    def load_user_table(self):
        # 查询用户信息
        users = get_all_users()     # # 函数没写？

        # 清空表格
        self.userInfoTable.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            # 列顺序: 用户名、用户密码、用户权限、最后登录时间、创建时间、修改时间
            # 用户密码这里留空或显示为 '******'
            username_item = QTableWidgetItem(str(user.get("username", "")))
            fullname_item = QTableWidgetItem(str(user.get("fullname", "")))
            password_item = QTableWidgetItem("******")  # 因为没有查询密码
            role_item = QTableWidgetItem(str(user.get("role", "")))
            last_login_item = QTableWidgetItem(
                str(user.get("lastLogin_at", "")) if user.get("lastLogin_at") else ""
            )
            created_item = QTableWidgetItem(
                str(user.get("created_at", "")) if user.get("created_at") else ""
            )
            updated_item = QTableWidgetItem(
                str(user.get("updated_at", "")) if user.get("updated_at") else ""
            )

            # 设置每个单元格的字体（可选）
            font12 = self.userInfoTable.font()  # 或你之前定义的 font12
            for item in [
                username_item,
                fullname_item,
                password_item,
                role_item,
                last_login_item,
                created_item,
                updated_item,
            ]:
                item.setFont(font12)

            # 将每个 QTableWidgetItem 写入表格
            self.userInfoTable.setItem(row_idx, 0, username_item)
            self.userInfoTable.setItem(row_idx, 1, fullname_item)
            self.userInfoTable.setItem(row_idx, 2, password_item)
            self.userInfoTable.setItem(row_idx, 3, role_item)
            self.userInfoTable.setItem(row_idx, 4, last_login_item)
            self.userInfoTable.setItem(row_idx, 5, created_item)
            self.userInfoTable.setItem(row_idx, 6, updated_item)
        self.center_table_data(self.userInfoTable)

    # 【用户信息】删除用户数据
    def on_delete_user_clicked(self):
        selected_rows = self.userInfoTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选中要删除的用户")
            return

        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除选中的用户吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # 倒序遍历删除，从最后一行往前删，不会影响前面行的索引，这是处理列表/表格删除的标准做法。
        for index in sorted(selected_rows, key=lambda x: x.row  (), reverse=True):
            row = index.row()
            username_item = self.userInfoTable.item(row, 0)
            if username_item:
                username = username_item.text()
                success, msg = delete_user(username, self.current_user_role)
                QMessageBox.information(self, "删除结果", msg)

                # 写日志
                log_user_action(
                    username=self.current_user,  # 当前操作人
                    action_type="delete_user",
                    target_user=username,
                    result=msg
                )
                if success:
                    self.userInfoTable.removeRow(row)

    # 【用户信息】修改用户数据
    def on_update_user_clicked(self):
        selected_rows = self.userInfoTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选中要修改的用户")
            return

        index = selected_rows[0]
        row = index.row()
        username_item = self.userInfoTable.item(row, 0)
        fullname_item = self.userInfoTable.item(row, 1)
        password_item = self.userInfoTable.item(row, 2)
        role_item = self.userInfoTable.item(row, 3)

        target_username = username_item.text()
        new_fullname = fullname_item.text()
        new_role = role_item.text() if role_item else None
        password_text = password_item.text() if password_item else ""
        new_password_hash = None

        # 仅在密码被修改（不是 "******"）时才 hash
        if password_text != "******" and password_text.strip() != "":
            new_password_hash = hash_password(password_text)

        success, msg, log_msg = update_user(
            target_username=target_username,
            current_user_role=self.current_user_role,
            new_password_hash=new_password_hash,
            new_role=new_role,
            new_fullname=new_fullname

        )
        QMessageBox.information(self, "修改结果", msg)

        # 写日志
        log_user_action(
            username=self.current_user,  # 当前操作人
            action_type="update_user",
            target_user=target_username,
            result=log_msg
        )

        if success:
            if new_role:
                self.userInfoTable.item(row, 3).setText(new_role)
            if new_password_hash:
                self.userInfoTable.item(row, 2).setText("******")
            if new_fullname:
                self.userInfoTable.item(row, 1).setText(new_fullname)

    # ==================== 缺陷检测页面 ====================
    def populate_defect_page(self):
        # 查询数据库
        defect_list = get_latest_defect_info()
        if not defect_list:
            latest_defect = {}
            # 如果没有数据，可以清空显示
            self.defectTotalCountLabel.setText("0")
            self.defectChippedCornerLabel.setText("0")
            self.defectSurfaceStainLabel.setText("0")
            self.defectCrackLabel.setText("0")
            return

        # 假设只显示最新的一条数据
        latest_defect = defect_list[0]

        # 填充到对应的标签
        self.defectTotalCountLabel.setText(str(latest_defect.get("total_defects", 0)))
        self.defectChippedCornerLabel.setText(str(latest_defect.get("missing_corners", 0)))
        self.defectSurfaceStainLabel.setText(str(latest_defect.get("stains", 0)))
        self.defectCrackLabel.setText(str(latest_defect.get("cracks", 0)))

    def on_hardware_connected(self):
        # 启动所有监控（或其他初始化）
        try:
            self.hardware_integration.start_all_monitors()
        except Exception as e:
            print(f"启动监控失败: {e}")
            return
        # 延迟 1s 再下发工艺，确保 PLC 已经就绪
        QTimer.singleShot(1000, self.example_edge_grinder_params)

    # ==================== 便捷控制方法 ====================

    def quick_start_all_hardware(self):
        """一键启动所有硬件并在连接成功后下发工艺参数"""
        try:
            self.hardware_integration.connect_all_devices()

            # 2s 后检查并启动监控，再调用下发函数
            QTimer.singleShot(3000, self.on_hardware_connected)

        except Exception as e:
            print(f"一键启动硬件失败: {e}")

    def emergency_stop_all_hardware(self):
        """紧急停止所有硬件"""
        try:
            self.hardware_integration.stop_all_monitors()
            self.hardware_integration.disconnect_all_devices()
            print("紧急停止完成")

        except Exception as e:
            print(f"紧急停止异常: {e}")

    # ==================== 手动控制示例 ====================

    def example_manual_flipper_control(self):
        """翻板机手动控制示例"""
        # 假设根据某些条件决定是否翻板
        if self.should_flip_board():
            success = self.hardware_integration.manual_flipper_turn()
            if success:
                print("翻板指令发送成功")
        else:
            success = self.hardware_integration.manual_flipper_pass()
            if success:
                print("通过指令发送成功")

    def example_manual_sorter_control(self):
        """分拣机手动控制示例"""
        # 假设根据产品质量决定分拣工位
        station = self.determine_sorting_station()
        success = self.hardware_integration.manual_sorter_to_station(station)
        if success:
            print(f"分拣到{station}号工位指令发送成功")
    """
    在下面重新添加了手动下发指令的示例方法 example_edge_grinder_params，并且实现了将任务添加到队列的逻辑。
    """
    def example_edge_grinder_params(self):
        """侧磨机参数设置示例"""
        # 假设从订单或二维码获取工艺参数
        params = self.get_process_parameters()

        machine_name = "磨边机1号"
        success = self.hardware_integration.manual_send_edge_params(
            machine_name,
            params['process_type'],
            params['thickness'],
            params['angle']
        )
        print(f"调用 [测试案例]向{machine_name}发送工艺参数...")
        if success:
            print(f"向{machine_name}发送工艺参数成功")
    #
    # def example_edge_grinder_params(self):
    #     """侧磨机参数设置示例：手动下发加工任务到队列"""
    #     try:
    #         print("新测试函数------开始手动下发工艺参数...")
    #         # 1. 准备工艺数据（实际开发中可改为从 UI 输入框获取）
    #         machine_name = "磨边机1号"  # 必须与配置文件中的名称一致
    #         process_type = 2  # 工艺类型 (例如：1-直边)
    #         thickness = 18.0  # 材料厚度
    #         angle = 45.0  # 斜边角度
    #
    #         # 2. 检查硬件控制器是否可用
    #         if hasattr(self, 'hardware_integration'):
    #             # 获取底层控制器实例
    #             controller = self.hardware_integration.hardware_controller
    #
    #             # 3. 调用 HardwareController 的 add_edge_task 函数
    #             # 该函数会将任务放入对应的 self.edge_queues[machine_name] 队列中
    #             controller.add_edge_task(machine_name, process_type, thickness, angle)
    #
    #             # 4. 界面日志反馈
    #             print(f"手动下发任务成功: {machine_name} | 工艺:{process_type} | 厚度:{thickness}| 斜边角度:{angle}")
    #         else:
    #             QMessageBox.warning(self, "警告", "硬件集成模块未初始化")
    #
    #     except Exception as e:
    #         print(f"手动下发工艺异常: {e}")
    #         traceback.print_exc()

    # ==================== 业务逻辑方法（示例） ====================

    def should_flip_board(self) -> bool:
        """判断是否需要翻板的业务逻辑"""
        # 这里应该是你的实际业务判断逻辑
        # 比如：根据产品类型、工艺要求、质量检测结果等
        return False # 示例返回

    def determine_sorting_station(self) -> int:
        """确定分拣工位的业务逻辑"""
        # 这里应该是你的实际业务判断逻辑
        # 比如：根据产品规格、质量等级、客户要求等
        return 1  # 示例返回1号工位

    def get_process_parameters(self) -> dict:
        """获取工艺参数的业务逻辑"""
        # 这里应该从数据库、二维码内容或其他数据源获取
        return {
            'process_type': 2,  # 直边
            'thickness': 20.0,  # 20mm
            'angle': 45.0  # 45度
        }


    # ==================== 产线新增5个扫码枪看板UI注入 ====================
    def inject_scanner_ui(self):
        """
        动态缩小日志GroupBox的高度，并在其上方插入新增的5个扫码枪的实时监控看板
        """
        try:
            if not hasattr(self, 'groupBox_5'):
                return

            # 1. 强制缩小原有日志框 (groupBox_5) 的最大高度到原来的一半左右 (约300px)
            self.groupBox_5.setMaximumHeight(300)

            # 2. 动态创建 5个新增扫码枪的显示面板
            from PyQt5.QtWidgets import QGroupBox, QGridLayout
            self.new_scanner_group = QGroupBox("流水线5台扫码枪")
            self.new_scanner_group.setStyleSheet(
                "QGroupBox { font-weight: bold; border: 1px solid gray; margin-top: 5px; margin-bottom: 5px; } QGroupBox::title {font-size: 30px; subcontrol-origin: margin; left: 15px; padding: 0 3px; }")
            self.new_scanner_group.setStyleSheet("""
                QGroupBox { 
                    font-size: 30px; /* 同时也在这里设置一遍 */
                    font-weight: bold; 
                    border: 2px solid gray; /* 必须加 solid */
                    border-radius: 5px;
                    margin-top: 30px; /* 重要：字体大时，必须调大此边距，否则标题会重叠在边框上 */
                    margin-bottom: 5px; 
                } 
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 15px; 
                    padding: 0 10px;
                    font-size: 30px; /* 标题字体大小 */
                }
            """)
            scanner_layout = QGridLayout()
            self.scanner_labels = {}

            # 这5个名字必须和 hardware_config.txt 里 scanner1~5 的 name 保持绝对一致
            scanner_names = [
                "侧磨机1号扫码枪(上料前)——1", "侧磨机2号扫码枪——2", "侧磨机3号扫码枪——3",
                "侧磨机4号扫码枪——4", "分拣机扫码枪——5"
            ]

            for i, name in enumerate(scanner_names):
                lbl = QLabel(f"{name}:\n[等待扫码...]")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(
                    "color: blue; font-weight: bold; font-size: 25px; border: 1px dashed #ccc; padding: 5px;")
                row = i // 3  # 排列布局：每行放3个，自动换行
                col = i % 3
                scanner_layout.addWidget(lbl, row, col)
                self.scanner_labels[name] = lbl

            self.new_scanner_group.setLayout(scanner_layout)

            # 3. 巧妙地将其插入到日志框上方 (verticalLayout_21 负责存放所有硬件控制底部的结构)
            idx = self.verticalLayout_21.indexOf(self.groupBox_5)
            if idx != -1:
                self.verticalLayout_21.insertWidget(idx, self.new_scanner_group)
                # 我们将三者的权重都设为 1，这样日志就刚好占据总高度的 1/(1+1+1) = 1/3
                self.verticalLayout_21.setStretch(0, 1)  # PLC 控制区
                self.verticalLayout_21.setStretch(1, 1)  # 扫码枪看板
                self.verticalLayout_21.setStretch(2, 1)  # 日志部分 (groupBox_5)

        except Exception as e:
            print(f"动态重构扫码枪UI失败: {e}")

    def update_scanner_ui(self, device_name, data):
        """
        接收底层 TCP 传回的数据，更新看板 UI
        """
        if hasattr(self, 'scanner_labels') and device_name in self.scanner_labels:
            lbl = self.scanner_labels[device_name]
            lbl.setText(f"{device_name}:\n{data}")
            # 成功获取数据后，将边框和背景变为绿色粗体的高亮状态
            lbl.setStyleSheet(
                "color: green; font-weight: bold; font-size: 15px; background-color: #e6ffe6; border: 1px solid #ccc; padding: 10px;")


    # ==================== 事件处理 ====================

    def closeEvent(self, event):
        """程序关闭事件"""
        try:
            print("正在关闭程序...")

            # 安全关闭硬件连接
            self.hardware_integration.cleanup_on_close()

            # 其他清理工作
            if hasattr(self, 'status_check_timer'):
                self.status_check_timer.stop()

            print("程序关闭完成")
            event.accept()

        except Exception as e:
            print(f"关闭程序时发生异常: {e}")
            event.accept()  # 即使有异常也强制关闭



# 提示框
class TipWin(QWidget, Ui_Tip):
    def __init__(self):
        super(TipWin, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)


def main():
    app = QApplication(sys.argv)
    mywindow = Window()
    mywindow.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

