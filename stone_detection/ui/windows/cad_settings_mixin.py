from .dependencies import *


class CadSettingsMixin:
    def del_cad_bmp(self):
        cad_name = self.cad_path.split('/')[-1].split('\\')[-1].split('.')[0]
        p = './' + cad_name + '.bmp'
        # 存在即重置
        if os.path.exists(p):
            os.remove(p)
            init_canvas(self.cad_path)
            self.simulation_cad([1, cad_name])

    def showError(self, cnt):
        # print(12345)
        content = '相机错误\n'
        for c in cnt:
            content += c
        content += '请检查后重启软件！'
        self.tip_win = TipWin()    # 显然是一个自定义的提示窗口类
        self.tip_win.label.setText(content)
        self.tip_win.show()

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

    def open_cad_img(self):
        if self.cad_img_path is not None:
            os.startfile(self.cad_img_path)
        else:
            self.tip_win = TipWin()
            self.tip_win.label.setText('没有选择图片！')
            self.tip_win.show()

    def open_canvas(self):
        if self.cad_path is not None:
            try:
                cad_name = self.cad_path.split('/')[-1].split('\\')[-1].split('.')[0]
                p = 'D:/app_24/stone_detection/stone_detection/' + cad_name + '.bmp'
                os.startfile(p)
            except Exception as e:
                print(e)

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

    def update_cad(self, cad):
        self.cad_path = cad
        self.label_4.setText('当前CAD文件：' + self.cad_path)

    def update_img(self, img_path):
        if self.cad_img_path == img_path:
            return
        self.cad_img_path = img_path
        scene = QGraphicsScene()
        pix = QtGui.QPixmap(self.cad_img_path).scaled(self.graphicsView_3.size(), aspectRatioMode=Qt.KeepAspectRatio)
        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)
        self.graphicsView_3.setScene(scene)

    def show_setting(self):
        self.label_6.setText('vlcf文件：' + self.mono_vlcf)
        self.label_9.setText('vlcf文件：' + self.color_vlcf)
        self.label_7.setText('ini文件：' + self.mono_ini)
        self.label_10.setText('ini文件：' + self.color_ini)

    def change_color_status(self):
        if self.use_color == 0:
            self.use_color = 1
            self.pushButton.setText('关闭')
        elif self.use_color == 1:
            self.use_color = 0
            self.pushButton.setText('打开')
        self.watch_dog.use_color_cam = self.use_color

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
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.cfg, f, indent=4)
                f.close()
            self.tip_win = TipWin()
            self.tip_win.label.setText('重启软件后生效！')
            self.tip_win.show()
