from .dependencies import *


class HardwareControlMixin:
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
