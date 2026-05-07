from .dependencies import *
from ..generated.interface import Ui_MainWindow
from .cad_settings_mixin import CadSettingsMixin
from .cutting_data_mixin import CuttingDataMixin
from .hardware_control_mixin import HardwareControlMixin
from .scan_data_mixin import ScanDataMixin
from .user_management_mixin import UserManagementMixin


class Window(
    ScanDataMixin,
    CuttingDataMixin,
    UserManagementMixin,
    CadSettingsMixin,
    HardwareControlMixin,
    QMainWindow,
    Ui_MainWindow,
):
    def __init__(self, current_user=None, current_user_role=None):
        super().__init__()
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
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
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

    def beautification(self):
        self.scanDataTable.verticalHeader().setDefaultSectionSize(200)
        self.scanDataTable.setColumnWidth(2, 300)
        self.scanDataTable.setColumnWidth(3, 150)
        self.scanDataTable.setColumnWidth(4, 150)

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

    def center_table_data(self, tableName: str):
        # 扫描数据表格
        for row in range(tableName.rowCount()):
            for col in range(tableName.columnCount()):
                item = tableName.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)


__all__ = ["Window", "log_user_action"]
