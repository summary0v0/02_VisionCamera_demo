import os.path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QHeaderView, QAbstractItemView, QTableWidgetItem, \
    QLabel, QGraphicsScene, QGraphicsPixmapItem, QCheckBox, QWidget, QFileDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDate
import sys
from interface import Ui_MainWindow
import cv2
import time
from my_thread import *
from common.dbFunction import *
from PIL import Image
from common.my_html import *
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import pyautogui
from common.cloud_sever import upload
from tip import Ui_Tip
import src_rc
import traceback
from PIL import ImageFile
import json
import glob
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)   # 加载 Qt Designer 生成的 UI 到当前窗口
        # cad 图片路径，未选择时为 None
        self.cad_img_path = None
        # 面积统计/片数统计，默认前者
        self.area_num = 1
        # 原始图片/量尺图片，默认前者
        self.raw_measure = 1
        # 可选日期初始化
        self.scanStartDateEdit.setDate(QDate.currentDate())
        self.scanEndDateEdit.setDate(QDate.currentDate())
        # sql数据
        self.datas = []
        # 首页
        self.stackedWidget.setCurrentIndex(1)
        # 下拉框
        # self.comboBox_3.setCurrentIndex(1)
        self.beautification()
        self.init_data(0)
        # 是否启动了扫描
        self.scan = False
        # 当前选中的行
        self.row_selected = None

        # # 看门狗
        # self.watch_dog = WatchDogThread(ID=len(self.datas))
        # # self.watch_dog.start()
        # self.start_n = 0
        # # 用于记录有没有start过
        #
        # # 初始化
        # self.ini_cam = InitThread()
        #
        # # qr1
        # try:
        #     self.qr1 = QRThread1()
        #     self.qr1.start()
        #     self.qr2 = QRThread2()
        #     self.qr2.start()
        #     self.qr3 = QRThread3()
        #     self.qr3.start()
        #     self.qr4 = QRThread4()
        #     self.qr4.start()
        #     self.qr5 = QRThread5()
        #     self.qr5.start()
        # except Exception as e:
        #     print('qr: ', e)
        #
        # # cad
        # # self.cad_t = CadThread()
        # # self.cad_t.start()

        # 状态
        self.scanStatusLabel.setText("<html><head/><body><p>当前状态：&nbsp; <span style=\" color:rgb(0, 0, 255);\">{}</span></p></body></html>".format('停止中'))
        self.scanRulerBtn.setStyleSheet(
            '#toolButton_27{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
        self.areaStatsTBtn.setStyleSheet(
            '#toolButton_20{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')

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
        # if not os.path.exists(self.cad_path):
        #     print('default cad error!')
        #     self.cad_path = None
        # self.watch_dog.cad_path = self.cad_path


    def signal_connect(self):
        self.toolButton_22.clicked.connect(self.showTableData_date)
        self.toolButton_3.clicked.connect(self.reset_date)
        # 点击事件获取所选内容、行列
        self.scanDataTable.cellPressed.connect(self.show_pic)
        self.toolButton_4.clicked.connect(self.open_raw_img)
        # 删除
        self.toolButton_5.clicked.connect(self.select2del)
        self.scanRulerBtn.clicked.connect(lambda: self.button_switch(1))
        self.scanOriginalBtn.clicked.connect(lambda: self.button_switch(2))
        self.areaStatsTBtn.clicked.connect(lambda: self.button_switch(3))
        self.countStatsTBtn.clicked.connect(lambda: self.button_switch(4))
        # 打印
        self.toolButton_23.clicked.connect(self.printer)
        # 开始扫描
        self.scanStartBtn.clicked.connect(lambda: self.button_switch(5))
        # 切换页面
        self.toolButton_28.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.homeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.toolButton_29.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.toolButton_30.clicked.connect(self.close)
        # 图像处理完成信号
        # 刷新table
        # self.watch_dog.sizeSignal.connect(lambda: self.init_data(self.area_num - 1))
        # # 初始化相机
        # self.ini_cam.initSignal.connect(self.write_logger)
        # # 相机采集到图片
        # self.watch_dog.getSignal.connect(self.write_logger)
        # # 报警
        # self.ini_cam.errorSignal.connect(self.showError)
        # self.watch_dog.errorSignal.connect(self.showError)
        # # 上传
        # self.toolButton_24.clicked.connect(self.select2upload)
        # # 更改图片
        # self.toolButton_7.clicked.connect(self.show_cad)
        # # 更改cad
        # self.toolButton_10.clicked.connect(self.select_cad)
        # # cad大图
        # self.toolButton_6.clicked.connect(self.open_cad_img)
        #
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
        # 读到的项目
        # self.watch_dog.proSignal.connect(self.search_cad)
        # # 更新cad
        # self.watch_dog.updateSignal.connect(self.update_cad)
        # # 更新img
        # self.watch_dog.updateSignal_2.connect(self.update_img)
        # 扫码器
        # self.qr1.qrSignal.connect(self.write_logger)
        # self.qr2.qrSignal.connect(self.write_logger)
        # self.qr3.qrSignal.connect(self.write_logger)
        # self.qr4.qrSignal.connect(self.write_logger)
        # self.qr5.qrSignal.connect(self.write_logger)



    def init_data(self, flag):
         #TODO: 后面可能要自动更新当日数据
         self.showTableData_date()
         # 当天扫描的石材面积
         todayScannedArea = dbSumTodayArea(flag)
         # 已上传的石材面积
         uploadedArea = dbSumUploadArea(flag)
         # 还未上传的石材面积
         notUploadedArea = dbSumNotUploadedArea(flag)
         if flag == 1:
             self.todayScannedBtn.setText('今日扫描\n' + todayScannedArea + '片')
             self.uploadedBtn.setText('累计已上传\n' + uploadedArea + '片')
             self.notUploadedBtn.setText('累计未上传\n' + notUploadedArea + '片')
         else:
             todayScannedArea = '%.2f' % float(todayScannedArea)
             uploadedArea = '%.2f' % float(uploadedArea)
             notUploadedArea = '%.2f' % float(notUploadedArea)
             self.todayScannedBtn.setText('今日扫描\n' + todayScannedArea + '┫')
             self.uploadedBtn.setText('累计已上传\n' + uploadedArea + '┫')
             self.notUploadedBtn.setText('累计未上传\n' + notUploadedArea + '┫')

    # 美化
    def beautification(self):
        self.scanDataTable.verticalHeader().setDefaultSectionSize(200)
        self.scanDataTable.setColumnWidth(2, 300)
        self.scanDataTable.setColumnWidth(3, 150)
        self.scanDataTable.setColumnWidth(4, 150)

    # 日期区间内
    def showTableData_date(self):
        dateStart = self.scanStartDateEdit.dateTime()
        dateEnd = self.scanEndDateEdit.dateTime().addDays(1)
        self.datas = dbFindWithDateRange(dateStart, dateEnd)

        self.scanDataTable.setRowCount(len(self.datas))
        # 查询总面积
        areaSumAll = dbSumArea(dateStart, dateEnd, self.area_num - 1)
        if self.area_num == 1:
            areaSumAll = '%.2f' % float(areaSumAll)
            self.totalScannedBtn.setText('总共扫描\n' + areaSumAll + '┫')
        else:
            self.totalScannedBtn.setText('总共扫描\n' + areaSumAll + '片')
        if len(self.datas) == 0:
            self.scanDataTable.setRowCount(5)
            return
        # 将查询到的数据填充到表格内
        self.datas = self.datas[::-1]
        # print(self.datas)
        for rowIndex, row in enumerate(self.datas):
            for columnIndex, item in enumerate(row):
                if columnIndex == 0:
                    # 插入上传和未上传
                    if item == 1:
                        self.scanDataTable.setItem(rowIndex, columnIndex + 1, QTableWidgetItem('已上传'))
                    else:
                        self.scanDataTable.setItem(rowIndex, columnIndex + 1, QTableWidgetItem('未上传'))
                        # 未上传的尝试上传
                        self.write_logger(str(self.datas[rowIndex][2]) + '正在上传')
                        res = upload(self.datas[rowIndex])
                        if res == 1:
                            self.write_logger(str(self.datas[rowIndex][2]) + '上传成功')
                            dbUpdate(ID=self.datas[rowIndex][2])
                            self.scanDataTable.setItem(rowIndex, 1, QTableWidgetItem('已上传'))

                    # 插入复选框
                    checkbox = QCheckBox()
                    checkbox.setStyleSheet("QCheckBox::indicator"
                               "{"
                               "width :100px;"
                               "height : 100px;"
                               "}")
                    self.scanDataTable.setCellWidget(rowIndex, 0, checkbox)

                elif columnIndex == 1:
                    # 插入图片
                    imageLabel = QLabel("")
                    imageLabel.setScaledContents(True)
                    imageLabel.setAlignment(Qt.AlignCenter)
                    # print('图片item:', item)
                    if item[-3: ] == 'bmp':
                        new_item = item.replace('bmp', 'jpg')
                        if os.path.exists(new_item):
                            # print(new_item)
                            image = QtGui.QPixmap(new_item)
                        else:
                            image = QtGui.QPixmap(item)
                    if item[-3:] == 'jpg':
                        image = QtGui.QPixmap(item)
                    imageLabel.setPixmap(image)
                    self.scanDataTable.setCellWidget(rowIndex, columnIndex + 1, imageLabel)
                # 时间去掉小数点后的
                elif columnIndex == 3:
                    self.scanDataTable.setItem(rowIndex, columnIndex + 1,
                                               QTableWidgetItem(str(self.datas[rowIndex][columnIndex])[:-7]))
                elif columnIndex <= 7:
                    self.scanDataTable.setItem(rowIndex, columnIndex + 1,
                                               QTableWidgetItem(str(self.datas[rowIndex][columnIndex])))
                # 不可编辑
                if columnIndex not in [0, 2] and columnIndex < 9:
                    self.scanDataTable.item(rowIndex, columnIndex).setFlags(QtCore.Qt.ItemIsEnabled)

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

    def open_raw_img(self):
        try:
            print(self.datas[self.row_selected][1])
            os.startfile(self.datas[self.row_selected][1])
        except:
            self.tip_win = TipWin()
            self.tip_win.label.setText('选择的对象不存在！')
            self.tip_win.show()

    # 打印
    def printer(self):
        if self.datas is None or len(self.datas) == 0:
            return
        html_data = []
        img_src = "<img src = {} width=300px height=200px>"
        for rowIndex, row in enumerate(self.datas):
            html_row = []
            for columnIndex, item in enumerate(row):
                if columnIndex == 0:
                    item = '已上传' if item == 1 else '未上传'
                elif columnIndex == 1:
                    item = img_src.format(item)
                elif columnIndex == 3:
                    item = str(item).split('.')[0]
                elif columnIndex >= 8:
                    continue
                html_row.append(str(item))
            html_row = tuple(html_row)
            html_data.append(html_row)
        html_data = tuple(html_data)
        print(html_data)
        header_data = (("上传状态", "图片", "编码", "扫描时间", "长", "宽", "二维码长" ,"二维码宽"),)
        title = '测试报告' + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        html = HtmlTableApi(
            title=title,
            header_data=header_data,
            rows_data=html_data
        )
        html.setAllStyle()
        html.createHtml()
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
        pyautogui.hotkey('ctrl', 'p')

    def button_switch(self, flag=None):
        # 量尺按钮
        if flag == 1:
            self.raw_measure = 2
            self.scanRulerBtn.setStyleSheet('#toolButton_27{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.scanOriginalBtn.setStyleSheet('#toolButton_26{border-radius: 10px; border: 2px groove gray;border-style: outset}')
        # 原始图片
        elif flag == 2:
            self.raw_measure = 1
            self.scanOriginalBtn.setStyleSheet(
                '#toolButton_26{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.scanRulerBtn.setStyleSheet(
                '#toolButton_27{border-radius: 10px; border: 2px groove gray;border-style: outset}')
        # 面积统计
        elif flag == 3:
            self.area_num = 1
            self.init_data(flag=0)
            self.areaStatsTBtn.setStyleSheet(
                '#toolButton_20{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.countStatsTBtn.setStyleSheet(
                '#toolButton_21{border-radius: 10px; border: 2px groove gray;border-style: outset}')
        # 片数统计
        elif flag == 4:
            self.area_num = 2
            self.init_data(flag=1)
            self.countStatsTBtn.setStyleSheet(
                '#toolButton_21{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
            self.areaStatsTBtn.setStyleSheet(
                '#toolButton_20{border-radius: 10px; border: 2px groove gray;border-style: outset}')
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
                self.scan = True
                # 传入检测类别
                # self.watch_dog.type = self.comboBox_3.currentIndex()
                self.watch_dog.type = 1
                # 继续
                if self.start_n == 0:
                    self.watch_dog.start()
                    self.start_n += 1
                else:
                    self.watch_dog.resume()
                self.scanStatusLabel.setText(
                    "<html><head/><body><p>当前状态：&nbsp; <span style=\" color:rgb(255, 0, 0);\">{}</span></p></body></html>".format(
                        '扫描中'))
                self.scanStartBtn.setText('停止扫描')
                self.write_logger('启动扫描')
                self.scanStartBtn.setStyleSheet(
                    '#toolButton_25{background-color: rgb(255, 40, 40);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')
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
                    '#toolButton_25{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}')

    def reset_date(self):
        self.scanStartDateEdit.setDate(QDate.currentDate())
        self.scanEndDateEdit.setDate(QDate.currentDate())
        self.showTableData_date()

    def show_raw_pic(self, row, col):
        if row >= len(self.datas):
            return

    def write_logger(self, msg):
        self.scanLogBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S-------->', time.localtime()) + msg + '\n')

    # 选中后上传
    def select2upload(self):
        if len(self.datas) == 0:
            self.tip_win = TipWin()
            self.tip_win.label.setText('没有数据！')
            self.tip_win.show()
            return

        rows =  len(self.datas)
        # 记录要上传的id
        ids = []
        for i in range(rows):
            if self.scanDataTable.cellWidget(i, 0).isChecked():
                res = upload('data')
                # 数据库更新
                if res == 1:
                    self.write_logger(str(self.datas[i][2]) + '上传成功')
                    dbUpdate(ID=self.datas[i][2])
                    self.scanDataTable.setItem(i, 1, QTableWidgetItem('已上传'))
                    self.scanDataTable.cellWidget(i, 0).setChecked(False)

    def closeEvent(self, event):
        sys.exit(0)

    # 选中后删除
    def select2del(self):
        if len(self.datas) == 0:
            self.tip_win = TipWin()
            self.tip_win.label.setText('没有数据！')
            self.tip_win.show()
            return

        rows =  len(self.datas)
        for i in range(rows):
            if self.scanDataTable.cellWidget(i, 0).isChecked():
                print(self.datas[i][2])
                # 删除
                deletedata(ID=self.datas[i][2])
                self.scanDataTable.cellWidget(i, 0).setChecked(False)
        self.showTableData_date()

    # 重置CAD
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
        self.tip_win = TipWin()
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
                                                            "CAD Files (*.dxf)")
        if ok:
            print(get_filename_path)
            self.label_4.setText('当前CAD文件：'+ get_filename_path)
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
            scene = QGraphicsScene()
            pix = QtGui.QPixmap(self.cad_img_path).scaled(self.graphicsView_3.size(), aspectRatioMode=Qt.KeepAspectRatio)
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
    def simulation_cad(self, op):
        # if op[0] == 0:
        #     # 二维码读取失败
        #     self.tip_win = TipWin()
        #     self.tip_win.label.setText('二维码读取失败')
        #     self.tip_win.show()
        scene = QGraphicsScene()
        # 显示模拟图需要传入cad名字
        p = './' + op[1] + '.bmp'

        pix = QtGui.QPixmap(p).scaled(self.graphicsView_4.size(), aspectRatioMode=Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)
        self.graphicsView_4.setScene(scene)

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


    # 显示设置
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

    # 修改设置
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

        # 保存
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
    main()