"""
主程序硬件控制集成文件
用于将硬件控制模块集成到主程序中
"""

import sys
import logging
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox

# 导入硬件控制模块
from common.HardwareController import HardwareController, HardwareControllerUI


class MainHardwareIntegration:
    """主程序硬件集成类"""

    def __init__(self, main_window):
        """
        初始化硬件集成

        Args:
            main_window: 主程序窗口对象，必须包含以下控件：
                - connect_sorter_btn: 连接分拣机按钮
                - disconnect_sorter_btn: 断开分拣机按钮
                - start_sorter_monitor_btn: 启动分拣机监控按钮
                - stop_sorter_monitor_btn: 停止分拣机监控按钮
                - connect_flipper_btn: 连接翻板机按钮
                - disconnect_flipper_btn: 断开翻板机按钮
                - start_flipper_monitor_btn: 启动翻板机监控按钮
                - stop_flipper_monitor_btn: 停止翻板机监控按钮
                - connect_edge_btn: 连接侧磨机按钮
                - disconnect_edge_btn: 断开侧磨机按钮
                - start_edge_monitor_btn: 启动侧磨机监控按钮
                - stop_edge_monitor_btn: 停止侧磨机监控按钮
                - connect_all_btn: 连接所有PLC按钮
                - disconnect_all_btn: 断开所有PLC按钮
                - start_all_monitor_btn: 启动所有PLC监控按钮
                - stop_all_monitor: 停止所有PLC监控按钮
                - flipperStateLabel: 翻板机状态标签
                - sorterStateLabel: 分拣机状态标签
                - qrBeforeEdgeStateLabel: 侧磨机前二维码状态标签
                - qrBeforeSorterStateLabel: 分拣机前二维码状态标签
                - logPlainTextEdit: 日志显示控件
        """
        self.main_window = main_window

        # 初始化硬件控制器
        self.hardware_controller = HardwareController()

        # 初始化UI绑定
        self.hardware_ui = HardwareControllerUI(main_window, self.hardware_controller)

        # 设置业务逻辑信号连接
        self.setup_business_logic()

        # 初始化状态
        self.init_status_display()

        logging.info("硬件控制模块集成完成")

    def setup_business_logic(self):
        """设置业务逻辑信号连接"""
        # 连接扫码标志检测到业务处理
        self.hardware_controller.scan_flag_detected.connect(self.handle_scan_flag)

        # 连接任务请求检测到业务处理
        self.hardware_controller.task_request_detected.connect(self.handle_task_request)

        # 连接错误处理
        self.hardware_controller.error_occurred.connect(self.handle_hardware_error)

    def init_status_display(self):
        """初始化状态显示"""
        try:
            # 设置初始状态
            if hasattr(self.main_window, 'flipperStateLabel'):
                self.main_window.flipperStateLabel.setText("翻板机: 未连接")
                self.main_window.flipperStateLabel.setStyleSheet("color: red; font-weight: bold;")

            if hasattr(self.main_window, 'sorterStateLabel'):
                self.main_window.sorterStateLabel.setText("分拣机: 未连接")
                self.main_window.sorterStateLabel.setStyleSheet("color: red; font-weight: bold;")

            if hasattr(self.main_window, 'qrBeforeEdgeStateLabel'):
                self.main_window.qrBeforeEdgeStateLabel.setText("侧磨机前二维码: 未连接")
                self.main_window.qrBeforeEdgeStateLabel.setStyleSheet("color: red; font-weight: bold;")

            if hasattr(self.main_window, 'qrBeforeSorterStateLabel'):
                self.main_window.qrBeforeSorterStateLabel.setText("分拣机前二维码: 未连接")
                self.main_window.qrBeforeSorterStateLabel.setStyleSheet("color: red; font-weight: bold;")

            for i in range(1, 5):  # 侧磨机1~4
                label_name = f'edgeGrinderStateLabel{i}'
                if hasattr(self.main_window, label_name):
                    label = getattr(self.main_window, label_name)
                    label.setText(f"侧磨机{i}: 未连接")
                    label.setStyleSheet("color: red; font-weight: bold;")


        except Exception as e:
            logging.warning(f"初始化状态显示失败: {e}")

    # ==================== 业务逻辑处理方法 ====================

    def handle_scan_flag(self, device_type: str, device_name: str):
        # ================== 仅手动测试需要使用 ======================


        """
        处理扫码标志检测

        Args:
            device_type: 设备类型 ('edge_grinder' 等)
            device_name: 设备名称
        """
        # self.hardware_ui.log_message(f"🔍 检测到 {device_name} 扫码标志")
        #
        # if device_type == 'edge_grinder':
        #     # 处理侧磨机扫码 - 可能需要读取二维码数据并处理工艺参数
        #     self.process_edge_grinder_scan(device_name)

        # 可以添加其他设备类型的扫码处理

    def handle_task_request(self, device_type: str, device_name: str):
        # ============== 仅手动测试需要使用 ================


        """
        处理任务请求检测

        Args:
            device_type: 设备类型 ('flipper', 'sorter' 等)
            device_name: 设备名称
        """
        # self.hardware_ui.log_message(f"📋 检测到 {device_name} 任务请求")
        #
        # if device_type == 'flipper':
        #     # 处理翻板机任务请求 - 根据业务逻辑决定翻板还是通过
        #     self.process_flipper_task(device_name)
        # elif device_type == 'sorter':
        #     # 处理分拣机任务请求 - 根据业务逻辑决定分拣到哪个工位
        #     self.process_sorter_task(device_name)

    def handle_hardware_error(self, device_type: str, device_name: str, error_msg: str):
        """处理硬件错误"""
        error_text = f"硬件错误 - {device_name}: {error_msg}"
        self.hardware_ui.log_message(f"❌ {error_text}")

        # 可以选择是否弹出错误对话框
        # QMessageBox.warning(self.main_window, "硬件错误", error_text)

    def process_edge_grinder_scan(self, machine_name: str):
        """
        处理侧磨机扫码事件

        这里应该根据你的业务逻辑来处理：
        1. 从数据库或其他来源获取工艺参数
        2. 发送工艺参数到侧磨机
        """
        try:
            # 示例：发送默认工艺参数
            # 实际使用时应该从二维码内容或数据库获取
            process_type = 1 # 直边
            thickness = 20.0  # 20mm
            angle = 45.0  # 45度

            success = self.hardware_controller.send_edge_grinder_params(
                machine_name, process_type, thickness, angle
            )

            if success:
                self.hardware_ui.log_message(f"✅ 成功向 {machine_name} 发送工艺参数")
            else:
                self.hardware_ui.log_message(f"❌ 向 {machine_name} 发送工艺参数失败")

        except Exception as e:
            logging.error(f"处理侧磨机扫码事件异常: {e}")
            self.hardware_ui.log_message(f"❌ 处理 {machine_name} 扫码事件异常: {e}")

    def process_flipper_task(self, device_name: str):
        """
        处理翻板机任务请求

        这里应该根据你的业务逻辑来决定：
        1. 是否需要翻板
        2. 还是直接通过
        """
        try:
            # 示例：简单的业务逻辑 - 这里可以根据产品信息、工艺要求等决定
            # 实际使用时应该根据具体业务需求来判断

            need_flip = True  # 这里应该是你的业务判断逻辑

            if need_flip:
                success = self.hardware_controller.flipper_turn_command()
                if success:
                    self.hardware_ui.log_message(f"✅ {device_name} 执行翻板指令成功")
                else:
                    self.hardware_ui.log_message(f"❌ {device_name} 执行翻板指令失败")
            else:
                success = self.hardware_controller.flipper_pass_command()
                if success:
                    self.hardware_ui.log_message(f"✅ {device_name} 执行通过指令成功")
                else:
                    self.hardware_ui.log_message(f"❌ {device_name} 执行通过指令失败")

        except Exception as e:
            logging.error(f"处理翻板机任务请求异常: {e}")
            self.hardware_ui.log_message(f"❌ 处理 {device_name} 任务请求异常: {e}")

    def process_sorter_task(self, device_name: str):
        """
        处理分拣机任务请求

        这里应该根据你的业务逻辑来决定：
        1. 分拣到哪个工位
        2. 根据产品规格、质量检测结果等
        """
        try:
            # 示例：简单的分拣逻辑 - 这里可以根据产品信息、质量检测结果等决定
            # 实际使用时应该根据具体业务需求来判断

            target_station = 1  # 这里应该是你的业务判断逻辑，返回1、2或3

            success = self.hardware_controller.sorter_send_to_station(target_station)
            if success:
                self.hardware_ui.log_message(f"✅ {device_name} 发送到{target_station}号工位成功")
            else:
                self.hardware_ui.log_message(f"❌ {device_name} 发送到{target_station}号工位失败")

        except Exception as e:
            logging.error(f"处理分拣机任务请求异常: {e}")
            self.hardware_ui.log_message(f"❌ 处理 {device_name} 任务请求异常: {e}")

    # ==================== 公共接口方法 ====================

    def connect_all_devices(self):
        """连接所有设备"""
        self.hardware_ui.log_message("开始连接所有设备...")

        # 连接翻板机
        self.hardware_ui.connect_flipper()

        # 连接分拣机
        self.hardware_ui.connect_sorter()

        # 连接侧磨机
        self.hardware_ui.connect_edge_grinders()

        self.hardware_ui.log_message("设备连接流程完成")

    def disconnect_all_devices(self):
        """断开所有设备"""
        self.hardware_ui.log_message("开始断开所有设备...")
        self.hardware_controller.disconnect_all()
        self.hardware_ui.log_message("所有设备已断开")

    def start_all_monitors(self):
        """启动所有监控"""
        self.hardware_ui.log_message("开始启动所有监控...")

        self.hardware_ui.start_flipper_monitor()
        self.hardware_ui.start_sorter_monitor()
        self.hardware_ui.start_edge_monitor()

        self.hardware_ui.log_message("所有监控启动完成")

    def stop_all_monitors(self):
        """停止所有监控"""
        self.hardware_ui.log_message("开始停止所有监控...")
        self.hardware_controller.stop_all_monitors()
        self.hardware_ui.log_message("所有监控已停止")

    def get_device_status(self) -> dict:
        """
        获取所有设备连接状态

        Returns:
            dict: 设备状态字典
        """
        return {
            'flipper_connected': self.hardware_controller.flipper_client is not None,
            'sorter_connected': self.hardware_controller.sorter_client is not None,
            'edge_grinders_count': len(self.hardware_controller.edge_clients),
            'monitor_threads_running': len(
                [t for t in self.hardware_controller.monitor_threads.values() if t.isRunning()])
        }

    # ==================== 手动控制方法 ====================

    def manual_flipper_turn(self):
        """手动翻板机翻板"""
        return self.hardware_ui.flipper_turn_action()

    def manual_flipper_pass(self):
        """手动翻板机通过"""
        return self.hardware_ui.flipper_pass_action()

    def manual_sorter_to_station(self, station: int):
        """手动分拣机到指定工位"""
        return self.hardware_ui.sorter_send_to_station(station)

    def manual_send_edge_params(self, machine_name: str, process_type: int, thickness: float, angle: float):
        """手动发送侧磨机参数"""
        return self.hardware_ui.send_edge_grinder_params(machine_name, process_type, thickness, angle)

    def get_edge_grinder_data(self, machine_name: str):
        """获取侧磨机数据"""
        return self.hardware_ui.get_edge_grinder_data(machine_name)

    # ==================== 程序关闭处理 ====================

    def cleanup_on_close(self):
        """程序关闭时的清理工作"""
        try:
            self.hardware_ui.log_message("正在关闭硬件控制模块...")

            # 停止所有监控
            self.stop_all_monitors()

            # 断开所有连接
            self.disconnect_all_devices()

            self.hardware_ui.log_message("硬件控制模块已安全关闭")

        except Exception as e:
            logging.error(f"关闭硬件控制模块时发生异常: {e}")


# ==================== 使用指南 ====================

"""
使用指南：

1. 在你的主程序中导入这个模块：
   from MainIntegration import MainHardwareIntegration

2. 在主窗口初始化后创建硬件集成实例：
   self.hardware_integration = MainHardwareIntegration(self)

3. 可选：添加一些便捷的控制方法到主窗口：

   def connect_all_hardware(self):
       self.hardware_integration.connect_all_devices()

   def start_all_hardware_monitors(self):
       self.hardware_integration.start_all_monitors()

   def cleanup_hardware(self):
       self.hardware_integration.cleanup_on_close()

4. 在主窗口的closeEvent中调用清理方法：

   def closeEvent(self, event):
       self.hardware_integration.cleanup_on_close()
       event.accept()

5. 如果需要手动控制设备，可以调用：

   # 手动翻板
   self.hardware_integration.manual_flipper_turn()

   # 手动分拣到1号工位
   self.hardware_integration.manual_sorter_to_station(1)

   # 手动发送侧磨机参数
   self.hardware_integration.manual_send_edge_params('磨边机1号', 1, 20.0, 45.0)

6. 业务逻辑定制：
   - 修改 process_edge_grinder_scan() 方法来处理扫码后的工艺参数逻辑
   - 修改 process_flipper_task() 方法来处理翻板机的业务判断逻辑
   - 修改 process_sorter_task() 方法来处理分拣机的业务判断逻辑

注意事项：
- 确保你的主窗口包含所有必需的控件（按钮和标签）
- 所有的IP地址配置在 HardwareController.py 的 HardwareConfig 类中
- 寄存器地址配置也在 HardwareConfig 类中
- 日志会同时输出到文件和界面，可以根据需要调整
"""


class QuickStartExample:
    """快速开始示例类"""

    @staticmethod
    def show_integration_example():
        """显示集成示例代码"""
        example_code = """
# 在你的主程序中添加以下代码：

class YourMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 你的UI初始化

        # 初始化硬件集成模块
        self.hardware_integration = MainHardwareIntegration(self)

        # 可选：添加菜单栏或工具栏的快捷操作
        self.setup_hardware_shortcuts()

    def setup_hardware_shortcuts(self):
        \"\"\"设置硬件控制快捷操作\"\"\"
        # 可以添加菜单项或工具栏按钮来快速控制所有硬件
        pass

    def closeEvent(self, event):
        \"\"\"程序关闭事件\"\"\"
        # 安全关闭硬件连接
        self.hardware_integration.cleanup_on_close()
        event.accept()

    # 可选：添加一些便捷方法
    def emergency_stop_all(self):
        \"\"\"紧急停止所有设备\"\"\"
        self.hardware_integration.stop_all_monitors()
        self.hardware_integration.disconnect_all_devices()

    def status_check(self):
        \"\"\"检查所有设备状态\"\"\"
        status = self.hardware_integration.get_device_status()
        print(f"设备状态: {status}")
        """

        print(example_code)


if __name__ == "__main__":
    QuickStartExample.show_integration_example()