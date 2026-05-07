
"""
石材流水线MES系统 - 硬件控制统一模块
整合翻板机、侧磨机、分拣机和二维码扫描功能
"""
import configparser
import logging
import os
import queue
import struct
import threading
import time
from typing import Optional, Dict, Any

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from pymodbus.client.tcp import ModbusTcpClient
from common import dbFunction
import utils

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./log/log_hardware.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class HardwareConfig:
    """硬件设备配置类（支持从 ./config/config.txt 读取）"""

    def __init__(self, config_path: str = "./configs/hardware_config.txt"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        self.parser = configparser.ConfigParser()
        self.parser.read(config_path, encoding="utf-8")

        # 磨边机寄存器默认配置（作为基础模板）
        self.EDGE_REGISTERS_TEMPLATE = {
            'task_request': {
                'type': 'word',
                'description': '任务请求标志位',
                'read_only': True
            },
            'scan_flag': {
                'type': 'word',
                'description': '扫码标志位',
                'read_only': True
            },
            'process_type': {
                'type': 'word',
                'description': '工艺类型',
                'read_only': False,
                'values': {1: '直边', 2: '大斜边', 3: '背切', 4: '开边槽', 5: '圆边'}
            },
            'material_thickness': {
                'type': 'real',
                'description': '材料厚度',
                'read_only': False,
                'unit': 'mm',
                'decimal_places': 1
            },
            'bevel_angle': {
                'type': 'real',
                'description': '斜边角度',
                'read_only': False,
                'unit': '度',
                'decimal_places': 1
            }
        }

        # 翻板机
        self.FLIPPER_CONFIG = self._load_device_config("flipper")

        # 分拣机
        self.SORTER_CONFIG = self._load_device_config("sorter")

        # 磨边机（多个）
        self.EDGE_GRINDERS = {}
        for section in self.parser.sections():
            if section.startswith("edge_grinders."):
                machine_name = section.split(".", 1)[1]
                self.EDGE_GRINDERS[machine_name] = self._load_device_config(section)

        # 扫描枪
        self.SCANNERS = {}
        for section in self.parser.sections():
            if section.startswith("scanner."):
                scanner_name = section.split(".", 1)[1]
                self.SCANNERS[scanner_name] = self._load_device_config(section)



    def _load_device_config(self, section: str):
        cfg = dict(self.parser.items(section))
        device = {
            "ip": cfg.get("ip", "127.0.0.1"),
            "port": int(cfg.get("port", 502)),
            "name": cfg.get("name", section)
        }

        # 加载寄存器
        registers = {}
        for key, value in cfg.items():
            if key.startswith("registers."):
                parts = key.split(".")
                if len(parts) >= 3:  # registers.register_name.attribute
                    reg_name = parts[1]
                    attr = parts[2]
                    if reg_name not in registers:
                        registers[reg_name] = {}
                    registers[reg_name][attr] = self._parse_value(value)

        # 对于磨边机，合并模板配置和具体配置
        if section.startswith("edge_grinders."):
            merged_registers = {}
            for reg_name, template_cfg in self.EDGE_REGISTERS_TEMPLATE.items():
                # 从模板复制基础配置
                merged_registers[reg_name] = dict(template_cfg)
                # 如果配置文件中有对应的寄存器配置，则覆盖/补充
                if reg_name in registers:
                    merged_registers[reg_name].update(registers[reg_name])
            registers = merged_registers

        if registers:
            device["registers"] = registers

        if "slave_id" in cfg:
            device["slave_id"] = int(cfg["slave_id"])

        return device

    def get_edge_register_info(self, machine_name: str, register_name: str):
        """获取特定磨边机的特定寄存器信息"""
        if machine_name not in self.EDGE_GRINDERS:
            return None

        machine_config = self.EDGE_GRINDERS[machine_name]
        if "registers" not in machine_config:
            return None

        return machine_config["registers"].get(register_name)

    @staticmethod
    def _parse_value(value: str):
        """自动转换数值/布尔"""
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return value


class HardwareController(QObject):
    """硬件控制器主类"""

    # 定义信号
    connection_status_changed = pyqtSignal(str, str, bool)  # 设备类型, 设备名称, 连接状态
    data_received = pyqtSignal(str, str, str, object)  # 设备类型, 设备名称, 寄存器名称, 数值
    error_occurred = pyqtSignal(str, str, str)  # 设备类型, 设备名称, 错误信息
    scan_flag_detected = pyqtSignal(str, str)  # 设备类型, 设备名称 - 检测到扫码标志
    task_request_detected = pyqtSignal(str, str)  # 设备类型, 设备名称 - 检测到任务请求
    scanner_data_received = pyqtSignal(str, str)  # 扫码枪数据接收信号：设备名称, 扫到的数据

    def __init__(self):
        super().__init__()
        self.config = HardwareConfig()

        # 各设备客户端
        self.flipper_client = None
        self.sorter_client = None
        self.edge_clients = {}
        self.qr_clients = {}  # 二维码扫描设备

        # 监控线程
        self.monitor_threads = {}
        self.sorter_queue = queue.Queue()  # 分拣机任务队列

        # 从配置文件加载磨边机
        self.edge_machines = self.config.EDGE_GRINDERS  # 动态读取所有磨边机配置
        self.edge_queues = {
            name: queue.Queue() for name in self.edge_machines.keys()
        }

        self.is_running = False

        # 维护连接状态
        self.edge_connected = {name: False for name in self.edge_machines.keys()}  # 磨边机连接状态
        self.flipper_connected = False  # 翻板机连接状态
        self.sorter_connected = False  # 分拣机连接状态

        # ==================== 翻板机任务队列 ====================
        self.flipper_task_queue = queue.Queue()
        self.flipper_poll_thread = None
        self.flipper_polling = False

        # ==================== 扫描枪 ====================
        self.scanner_controller = ScannerController(self, scanner_configs=self.config.SCANNERS)
        # 启动处理线程
        threading.Thread(target=self._process_before_processing_queue, daemon=True).start()
        threading.Thread(target=self._process_before_sorting_queue, daemon=True).start()

    # ==================== 扫描枪 ====================

    def _process_before_processing_queue(self):
        """处理加工前扫描枪队列"""
        while True:
            # 当队列有数据才往下操作，否则会阻塞线程
            # 从 URL 获取 composite_id、processing_type、thickness 等信息
            # url = self.scanner_controller.queue_before_processing.get()
            # composite_id, scale_url, processing_type, thickness = process_stone_item_from_url(url)

            # 测试用例
            time.sleep(5)
            print("处理加工前扫描枪队列。")
            # process_map 'values': {1: '直边', 2: '大斜边', 3: '背切', 4: '开边槽', 5: '圆边'}
            # process_map = {"0": None, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
            composite_id, scale_url, processing_type, thickness = "25-5-181A177", "https://lsmc-oss.oss-cn-shanghai.aliyuncs.com/middleware/lsmc/1927548980971450370/cropMap/cell/cbbc5501-cd02-488e-8bfc-125e5d7b514c.png", "5432", 16.0

            # 翻板机任务
            if self.flipper_connected:
                if processing_type != "0000":
                    self.flipper_task_queue.put(1)
                    print(f"[翻板机] 投递翻板任务: composite_id={composite_id}", flush=True)
                else:
                    self.flipper_task_queue.put(2)
                    print(f"[翻板机] 投递通过任务: composite_id={composite_id}", flush=True)
            else:
                print(f"[翻板机] 未连接，跳过投递: composite_id={composite_id}")

            # 四台侧磨机任务
            directions = ["磨边机1号", "磨边机2号", "磨边机3号", "磨边机4号"]
            # process_map 'values': {1: '直边', 2: '大斜边', 3: '背切', 4: '开边槽', 5: '圆边'}
            process_map = {"0": None, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
            for i, ch in enumerate(processing_type):
                if self.edge_connected.get(directions[i]) and process_map.get(ch):
                    # --- 滚动存放逻辑开始 ---
                    # 如果队列当前长度已经达到或超过 5，先弹出最旧的一条
                    if self.edge_queues[directions[i]].qsize() >= 5:
                        removed_task = self.edge_queues[directions[i]].get()
                        print(
                            f"{directions[i]} 队列已满5行，移除最旧任务: composite_id={composite_id}, 工艺={removed_task[0]}, 厚度={removed_task[1]}, 角度={removed_task[2]}",
                            flush=True)

                    self.edge_queues[directions[i]].put((process_map[ch], thickness, 0.0))
                    print(
                        f" {directions[i]} 执行磨边任务: composite_id={composite_id}, 工艺={process_map[ch]}, 厚度={thickness}, 当前队列长度={self.edge_queues[directions[i]].qsize()}",
                        flush=True)
                elif not self.edge_connected.get(directions[i]):
                    print(f"{directions[i]} 未连接，跳过任务")

    def _process_before_sorting_queue(self):
        """处理分拣前扫描枪队列"""
        import time
        while True:
            # 当队列有数据才往下操作，否则会阻塞线程
            # url = self.scanner_controller.queue_before_sorting.get()
            # composite_id = utils.get_scale_and_id_by_url(url)['composite_id']
            # 获取 box_number
            # box_number = get_box_number_by_composite(composite_id)

            # 测试用例
            time.sleep(5)
            print("处理分拣前扫描枪队列。")
            composite_id = "25-5-181A177"
            box_number = "2#"

            if box_number:
                # 去掉 '#'
                box_number_clean = ''.join(filter(str.isdigit, str(box_number)))
                box_number_clean = int(box_number_clean)
                if self.sorter_connected:
                    self.sorter_queue.put(box_number_clean)
                    print(f"[分拣机] 投递 box_number={box_number_clean}")
                    # 更新数据库状态
                    # update_cutting_status(composite_id)
                    print("石材切割状态更新完成", flush=True)
                else:
                    print(f"[分拣机] 未连接，跳过投递")

            time.sleep(1)

    # ==================== 翻板机控制 ====================

    def connect_flipper(self):
        """连接翻板机"""
        try:
            config = self.config.FLIPPER_CONFIG
            client = ModbusTcpClient(
                host=config['ip'],
                port=config['port'],
                timeout=10
            )

            if client.connect():
                self.flipper_client = {
                    'client': client,
                    'config': config
                }
                self.connection_status_changed.emit('flipper', config['name'], True)
                self.flipper_connected = True
                logging.info(f"成功连接到翻板机 ({config['ip']}:{config['port']})")
                return True
            else:
                self.connection_status_changed.emit('flipper', config['name'], False)
                self.flipper_connected = False
                logging.error(f"无法连接到翻板机")
                return False

        except Exception as e:
            self.flipper_connected = False
            logging.error(f"连接翻板机时发生错误: {str(e)}")
            self.error_occurred.emit('flipper', 'connection', str(e))
            return False

    def disconnect_flipper(self):
        """断开翻板机连接"""
        if self.flipper_client:
            try:
                self.flipper_client['client'].close()
                config_name = self.flipper_client['config']['name']
                self.connection_status_changed.emit('flipper', config_name, False)
                self.flipper_client = None
                self.flipper_connected = False
                logging.info("已断开翻板机连接")
            except Exception as e:
                logging.error(f"断开翻板机连接时出错: {str(e)}")

    def flipper_turn_command(self):
        """翻板机执行翻板"""
        return self._write_flipper_register('task_command', 1)

    def flipper_pass_command(self):
        """翻板机直接通过"""
        return self._write_flipper_register('task_command', 2)

    # ==================== 翻板机新增控制指令 ====================

    def flipper_start_command(self) -> bool:
        """
        发送翻板机启动脉冲指令 (写入 1 -> 延时 1 秒 -> 写入 0)
        对应寄存器: flipper_start (地址: 303)
        """
        if not self.flipper_client:
            logging.error("翻板机未连接，无法发送脉冲指令")
            return False

        def send_pulse_logic():
            """子线程执行的脉冲逻辑"""
            try:
                # 1. 写入启动信号 1
                logging.info("下发翻板机启动脉冲：正在置 1 (地址 303)")
                success = self._write_flipper_register('flipper_start', 1)

                if success:
                    # 2. 延时 1 秒
                    # 这里的 time.sleep 在子线程中运行，不会卡顿主程序
                    time.sleep(1)

                    # 3. 写入复位信号 0
                    logging.info("下发翻板机启动脉冲：延时结束，正在复位为 0")
                    self._write_flipper_register('flipper_start', 0)
                else:
                    logging.error("翻板机启动脉冲发送失败 (写入 1 时失败)")

            except Exception as e:
                logging.error(f"脉冲控制逻辑执行异常: {str(e)}")

        # 开启守护线程执行脉冲逻辑，避免阻塞 UI 线程
        threading.Thread(target=send_pulse_logic, daemon=True).start()
        return True

    def flipper_stop_command(self) -> bool:
        """
        发送翻板机停止脉冲指令 (写入 1 -> 延时 1 秒 -> 写入 0)
        对应寄存器: flipper_stop (地址: 304)
        """
        if not self.flipper_client:
            logging.error("翻板机未连接，无法发送停止脉冲指令")
            return False

        def send_stop_pulse_logic():
            """子线程执行的停止脉冲逻辑"""
            try:
                # 1. 写入停止信号 1 (寄存器地址 304)
                logging.info("下发翻板机停止脉冲：正在置 1 (地址 304)")
                success = self._write_flipper_register('flipper_stop', 1)

                if success:
                    # 2. 延时 1 秒
                    # 使用 time.sleep 在守护线程中等待，不会阻塞 UI 或监控
                    time.sleep(1)

                    # 3. 写入复位信号 0，完成脉冲动作
                    logging.info("下发翻板机停止脉冲：延时结束，正在复位为 0")
                    self._write_flipper_register('flipper_stop', 0)
                else:
                    logging.error("翻板机停止脉冲发送失败 (写入 1 时失败)")

            except Exception as e:
                logging.error(f"停止脉冲控制逻辑执行异常: {str(e)}")

        # 开启守护线程执行脉冲逻辑
        threading.Thread(target=send_stop_pulse_logic, daemon=True).start()
        return True

    def read_flipper_status(self):
        """主动读取翻板机状态 (寄存器 2)"""
        return self._read_flipper_register('flipper_status')

    def _read_flipper_register(self, register_name: str) -> Optional[int]:
        """读取翻板机寄存器"""
        if not self.flipper_client:
            logging.error("翻板机未连接")
            return None

        config = self.flipper_client['config']
        client = self.flipper_client['client']

        if register_name not in config['registers']:
            logging.error(f"寄存器 {register_name} 未定义")
            return None

        register_info = config['registers'][register_name]
        address = register_info['address']

        try:
            result = client.read_holding_registers(address=address, count=1, slave=1)

            if not result.isError():
                value = result.registers[0]
                self.data_received.emit('flipper', config['name'], register_name, value)
                logging.info(f"读取翻板机.{register_name}: {value}")
                return value
            else:
                logging.error(f"读取翻板机.{register_name} 失败: {result}")
                self.error_occurred.emit('flipper', config['name'], f"读取寄存器失败: {result}")
                return None

        except Exception as e:
            logging.error(f"读取异常 - 翻板机.{register_name}: {str(e)}")
            self.error_occurred.emit('flipper', config['name'], f"读取异常: {str(e)}")
            return None

    def _write_flipper_register(self, register_name: str, value: int) -> bool:
        """写入翻板机寄存器"""
        if not self.flipper_client:
            logging.error("翻板机未连接")
            return False

        config = self.flipper_client['config']
        client = self.flipper_client['client']

        if register_name not in config['registers']:
            logging.error(f"寄存器 {register_name} 未定义")
            return False

        register_info = config['registers'][register_name]
        address = register_info['address']

        try:
            result = client.write_register(address=address, value=value, slave=1)

            if not result.isError():
                logging.info(f"写入翻板机.{register_name}: {value}")
                return True
            else:
                logging.error(f"写入翻板机.{register_name} 失败: {result}")
                self.error_occurred.emit('flipper', config['name'], f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - 翻板机.{register_name}: {str(e)}")
            self.error_occurred.emit('flipper', config['name'], f"写入异常: {str(e)}")
            return False

    def flipper_send_task(self, task: int) -> bool:
        """向翻板机发送任务"""
        if task not in [1, 2, 3]:
            logging.error(f"无效翻板机任务: {task}")
            return False

        return self._write_flipper_register('task_command', task)

    # ==================== 翻板机任务队列操作 ====================
    def add_flipper_task(self, task: int):
        """添加任务到翻板机队列，task=1 翻板, task=2 通过"""
        if task not in (1, 2):
            logging.warning(f"非法翻板任务: {task}")
            return
        self.flipper_task_queue.put(task)
        logging.info(f"添加翻板任务: {task}")

    def start_flipper_polling(self):
        """启动轮询翻板机请求寄存器线程"""
        if not self.flipper_client:
            logging.error("翻板机未连接，无法启动轮询")
            return

        if self.flipper_poll_thread and self.flipper_poll_thread.is_alive():
            logging.warning("翻板机轮询线程已在运行")
            return

        self.flipper_polling = True
        self.flipper_poll_thread = threading.Thread(target=self._flipper_poll_loop, daemon=True)
        self.flipper_poll_thread.start()
        logging.info("翻板机轮询线程已启动")

    def stop_flipper_polling(self):
        """停止轮询翻板机请求寄存器"""
        self.flipper_polling = False
        if self.flipper_poll_thread:
            self.flipper_poll_thread.join(timeout=2)
            logging.info("翻板机轮询线程已停止")

    def _flipper_poll_loop(self):
        """轮询翻板机请求寄存器，并根据队列发送任务"""
        while self.flipper_polling:
            value = self._read_flipper_register('task_request')
            if value is None:
                # 读取失败，稍等再试
                time.sleep(1)
                continue

            if value == 1:
                if not self.flipper_task_queue.empty():
                    task = self.flipper_task_queue.get()
                    success = self._write_flipper_register('task_command', task)
                    if success:
                        logging.info(f"发送翻板机任务: {task}，暂停轮询 10 秒")
                        # 暂停 10 秒
                        for _ in range(10):
                            if not self.flipper_polling:
                                break
                            time.sleep(1)
                    else:
                        logging.error("发送翻板机任务失败")
                else:
                    logging.warning("翻板机请求任务，但队列为空")
            # 每秒轮询一次
            time.sleep(1)

    def _write_flipper_task_request(self, value: int) -> bool:
        """向翻板机的task_request寄存器写入信号

        Args:
            value: 要写入的值

        Returns:
            bool: 写入是否成功
        """
        if not self.flipper_client:
            logging.error("翻板机未连接")
            return False

        config = self.flipper_client['config']
        client = self.flipper_client['client']

        if 'task_request' not in config['registers']:
            logging.error(f"寄存器 task_request 未定义")
            return False

        register_info = config['registers']['task_request']
        address = register_info['address']

        try:
            result = client.write_register(address=address, value=value, slave=1)

            if not result.isError():
                logging.info(f"写入翻板机.task_request: {value}")
                return True
            else:
                logging.error(f"写入翻板机.task_request 失败: {result}")
                self.error_occurred.emit('flipper', config['name'], f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - 翻板机.task_request: {str(e)}")
            self.error_occurred.emit('flipper', config['name'], f"写入异常: {str(e)}")
            return False

    # ==================== 分拣机控制 ====================

    def connect_sorter(self):
        """连接分拣机"""
        try:
            config = self.config.SORTER_CONFIG
            client = ModbusTcpClient(
                host=config['ip'],
                port=config['port'],
                timeout=10
            )

            if client.connect():
                self.sorter_client = {
                    'client': client,
                    'config': config
                }
                self.connection_status_changed.emit('sorter', config['name'], True)
                self.sorter_connected = True
                logging.info(f"成功连接到分拣机 ({config['ip']}:{config['port']})")
                return True
            else:
                self.connection_status_changed.emit('sorter', config['name'], False)
                self.sorter_connected = False
                logging.error(f"无法连接到分拣机")
                return False

        except Exception as e:
            self.sorter_connected = False
            logging.error(f"连接分拣机时发生错误: {str(e)}")
            self.error_occurred.emit('sorter', 'connection', str(e))
            return False

    def disconnect_sorter(self):
        """断开分拣机连接"""
        if self.sorter_client:
            try:
                self.sorter_client['client'].close()
                config_name = self.sorter_client['config']['name']
                self.connection_status_changed.emit('sorter', config_name, False)
                self.sorter_client = None
                self.sorter_connected = False
                logging.info("已断开分拣机连接")
            except Exception as e:
                self.sorter_connected = False
                logging.error(f"断开分拣机连接时出错: {str(e)}")

    def sorter_send_to_station(self, station: int):
        """分拣机发送到指定工位"""
        if station not in [1, 2, 3]:
            logging.error(f"无效的工位号: {station}")
            return False

        return self._write_sorter_register('station_command', station)

    def _read_sorter_register(self, register_name: str) -> Optional[int]:
        """读取分拣机寄存器"""
        if not self.sorter_client:
            logging.error("分拣机未连接")
            return None

        config = self.sorter_client['config']
        client = self.sorter_client['client']

        if register_name not in config['registers']:
            logging.error(f"寄存器 {register_name} 未定义")
            return None

        register_info = config['registers'][register_name]
        address = register_info['address']

        try:
            result = client.read_holding_registers(address=address, count=1, slave=1)

            if not result.isError():
                value = result.registers[0]
                self.data_received.emit('sorter', config['name'], register_name, value)
                logging.info(f"读取分拣机.{register_name}: {value}")
                return value
            else:
                logging.error(f"读取分拣机.{register_name} 失败: {result}")
                self.error_occurred.emit('sorter', config['name'], f"读取寄存器失败: {result}")
                return None

        except Exception as e:
            logging.error(f"读取异常 - 分拣机.{register_name}: {str(e)}")
            self.error_occurred.emit('sorter', config['name'], f"读取异常: {str(e)}")
            return None

    def _write_sorter_register(self, register_name: str, value: int) -> bool:
        """写入分拣机寄存器"""
        if not self.sorter_client:
            logging.error("分拣机未连接")
            return False

        config = self.sorter_client['config']
        client = self.sorter_client['client']

        if register_name not in config['registers']:
            logging.error(f"寄存器 {register_name} 未定义")
            return False

        register_info = config['registers'][register_name]
        address = register_info['address']

        try:
            result = client.write_register(address=address, value=value, slave=1)

            if not result.isError():
                logging.info(f"写入分拣机.{register_name}: {value}")
                return True
            else:
                logging.error(f"写入分拣机.{register_name} 失败: {result}")
                self.error_occurred.emit('sorter', config['name'], f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - 分拣机.{register_name}: {str(e)}")
            self.error_occurred.emit('sorter', config['name'], f"写入异常: {str(e)}")
            return False

    def add_sorter_task(self, station: int):
        """向分拣机任务队列添加任务"""
        if station in [1, 2, 3]:
            self.sorter_queue.put(station)
            logging.info(f"添加分拣任务: {station}")
        else:
            logging.error(f"无效的分拣机任务: {station}")

    def _write_sorter_task_request(self, value: int) -> bool:
        """向分拣机的task_request寄存器写入信号

        Args:
            value: 要写入的值

        Returns:
            bool: 写入是否成功
        """
        if not self.sorter_client:
            logging.error("分拣机未连接")
            return False

        config = self.sorter_client['config']
        client = self.sorter_client['client']

        if 'task_request' not in config['registers']:
            logging.error(f"寄存器 task_request 未定义")
            return False

        register_info = config['registers']['task_request']
        address = register_info['address']

        try:
            result = client.write_register(address=address, value=value, slave=1)

            if not result.isError():
                logging.info(f"写入分拣机.task_request: {value}")
                return True
            else:
                logging.error(f"写入分拣机.task_request 失败: {result}")
                self.error_occurred.emit('sorter', config['name'], f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - 分拣机.task_request: {str(e)}")
            self.error_occurred.emit('sorter', config['name'], f"写入异常: {str(e)}")
            return False



    # ==================== 侧磨机控制 ====================

    def _read_edge_raw_registers(self, machine_name: str, address: int, count: int = 2):
        """读取侧磨机原始 holding registers（不做任何解析）"""
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return None

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        slave_id = client_info['config']['slave_id']

        result = client.read_holding_registers(
            address=address,
            count=count,
            slave=slave_id
        )

        if result.isError():
            logging.error(f"读取原始寄存器失败: {result}")
            return None

        return result.registers

    def connect_edge_grinders(self):
        """连接所有侧磨机"""
        success_count = 0
        for machine_name, machine_config in self.config.EDGE_GRINDERS.items():
            if self._connect_single_edge_grinder(machine_name, machine_config):
                success_count += 1

        logging.info(f"侧磨机连接完成，成功连接 {success_count}/{len(self.config.EDGE_GRINDERS)} 台")
        return success_count > 0

    def _connect_single_edge_grinder(self, machine_name: str, machine_config: dict):
        """连接单台侧磨机"""
        try:
            client = ModbusTcpClient(
                host=machine_config['ip'],
                port=machine_config['port'],
                timeout=10
            )

            if client.connect():
                self.edge_clients[machine_name] = {
                    'client': client,
                    'config': machine_config
                }
                self.connection_status_changed.emit('edge_grinder', machine_name, True)
                self.edge_connected[machine_name] = True
                logging.info(f"成功连接到 {machine_name} ({machine_config['ip']}:{machine_config['port']})")
                return True
            else:
                self.connection_status_changed.emit('edge_grinder', machine_name, False)
                self.edge_connected[machine_name] = False
                logging.error(f"无法连接到 {machine_name}")
                return False

        except Exception as e:
            self.edge_connected[machine_name] = False
            logging.error(f"连接 {machine_name} 时发生错误: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, str(e))
            return False

    def disconnect_edge_grinders(self):
        """断开所有侧磨机连接"""
        for machine_name, client_info in self.edge_clients.items():
            try:
                client_info['client'].close()
                self.connection_status_changed.emit('edge_grinder', machine_name, False)
                self.edge_connected[machine_name] = False
                logging.info(f"已断开 {machine_name} 连接")
            except Exception as e:
                self.edge_connected[machine_name] = False
                logging.error(f"断开 {machine_name} 连接时出错: {str(e)}")

        self.edge_clients.clear()

    def send_edge_grinder_params(self, machine_name: str, process_type: int, thickness: float, angle: float):
        """发送侧磨机工艺参数"""
        success_count = 0

        # 发送工艺类型
        if self._write_edge_word_register(machine_name, 'process_type', process_type):
            success_count += 1

        # 发送材料厚度
        if self._write_edge_real_register(machine_name, 'material_thickness', thickness):
            success_count += 1

        # 发送斜边角度
        if self._write_edge_real_register(machine_name, 'bevel_angle', angle):
            success_count += 1

        logging.info(f"向 {machine_name} 发送参数完成，成功 {success_count}/3 个参数")
        return success_count == 3

    def _read_edge_word_register(self, machine_name: str, register_name: str) -> Optional[int]:
        """读取侧磨机Word类型寄存器"""
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return None

        # 从具体机器配置中获取寄存器信息
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config or register_name not in machine_config['registers']:
            logging.error(f"寄存器 {register_name} 在 {machine_name} 中未定义")
            return None

        register_info = machine_config['registers'][register_name]
        if register_info.get('type') != 'word':
            logging.error(f"寄存器 {register_name} 不是Word类型")
            return None

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        address = register_info['address']
        slave_id = client_info['config']['slave_id']

        try:
            result = client.read_holding_registers(address=address, count=1, slave=slave_id)

            if not result.isError():
                value = result.registers[0]
                self.data_received.emit('edge_grinder', machine_name, register_name, value)
                logging.info(f"读取 {machine_name}.{register_name}: {value}")
                return value
            else:
                logging.error(f"读取 {machine_name}.{register_name} 失败: {result}")
                self.error_occurred.emit('edge_grinder', machine_name, f"读取寄存器失败: {result}")
                return None

        except Exception as e:
            logging.error(f"读取异常 - {machine_name}.{register_name}: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, f"读取异常: {str(e)}")
            return None

    def _read_edge_real_register(self, machine_name: str, register_name: str) -> Optional[float]:
        """读取侧磨机Real类型寄存器（浮点数，占用2个寄存器）"""
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return None

        # 从具体机器配置中获取寄存器信息
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config or register_name not in machine_config['registers']:
            logging.error(f"寄存器 {register_name} 在 {machine_name} 中未定义")
            return None

        register_info = machine_config['registers'][register_name]
        if register_info.get('type') != 'real':
            logging.error(f"寄存器 {register_name} 不是Real类型")
            return None

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        address = register_info['address']
        slave_id = client_info['config']['slave_id']

        try:
            # Real类型占用2个寄存器
            result = client.read_holding_registers(address=address, count=2, slave=slave_id)

            if not result.isError():
                # 将两个16位寄存器合并为32位浮点数
                # raw_bytes = struct.pack('>HH', result.registers[0], result.registers[1])
                raw_bytes = struct.pack('>HH', result.registers[1], result.registers[0])
                value = struct.unpack('>f', raw_bytes)[0]

                # 根据配置保留小数位数
                decimal_places = register_info.get('decimal_places', 1)
                value = round(value, decimal_places)

                self.data_received.emit('edge_grinder', machine_name, register_name, value)
                logging.info(f"读取 {machine_name}.{register_name}: {value}")
                return value
            else:
                logging.error(f"读取 {machine_name}.{register_name} 失败: {result}")
                self.error_occurred.emit('edge_grinder', machine_name, f"读取寄存器失败: {result}")
                return None

        except Exception as e:
            logging.error(f"读取异常 - {machine_name}.{register_name}: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, f"读取异常: {str(e)}")
            return None

    def _write_edge_task_request(self, machine_name: str, value: int) -> bool:
        """向侧磨机的task_request寄存器写入信号

        Args:
            machine_name: 侧磨机名称，如 '磨边机1号'
            value: 要写入的值

        Returns:
            bool: 写入是否成功

        Note:
            尽管task_request在配置中标记为read_only=true，
            但此方法允许在特殊情况下向其写入（例如复位请求标志）
        """
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return False

        # 从具体机器配置中获取寄存器信息
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config or 'task_request' not in machine_config['registers']:
            logging.error(f"寄存器 task_request 在 {machine_name} 中未定义")
            return False

        register_info = machine_config['registers']['task_request']

        # 检查寄存器类型
        if register_info.get('type') != 'word':
            logging.error(f"寄存器 task_request 不是Word类型")
            return False

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        address = register_info['address']
        slave_id = client_info['config']['slave_id']

        try:
            result = client.write_register(address=address, value=value, slave=slave_id)

            if not result.isError():
                logging.info(f"写入 {machine_name}.task_request: {value}")
                return True
            else:
                logging.error(f"写入 {machine_name}.task_request 失败: {result}")
                self.error_occurred.emit('edge_grinder', machine_name, f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - {machine_name}.task_request: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, f"写入异常: {str(e)}")
            return False

    def _write_edge_word_register(self, machine_name: str, register_name: str, value: int) -> bool:
        """写入侧磨机Word类型寄存器"""
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return False

        # 从具体机器配置中获取寄存器信息
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config or register_name not in machine_config['registers']:
            logging.error(f"寄存器 {register_name} 在 {machine_name} 中未定义")
            return False

        register_info = machine_config['registers'][register_name]
        if register_info.get('type') != 'word':
            logging.error(f"寄存器 {register_name} 不是Word类型")
            return False

        if register_info.get('read_only', False):
            logging.error(f"寄存器 {register_name} 为只读")
            return False

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        address = register_info['address']
        slave_id = client_info['config']['slave_id']

        try:
            result = client.write_register(address=address, value=value, slave=slave_id)

            if not result.isError():
                logging.info(f"写入 {machine_name}.{register_name}: {value}")
                return True
            else:
                logging.error(f"写入 {machine_name}.{register_name} 失败: {result}")
                self.error_occurred.emit('edge_grinder', machine_name, f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - {machine_name}.{register_name}: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, f"写入异常: {str(e)}")
            return False

    def _write_edge_real_register(self, machine_name: str, register_name: str, value: float) -> bool:
        """写入侧磨机Real类型寄存器"""
        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return False

        # 从具体机器配置中获取寄存器信息
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config or register_name not in machine_config['registers']:
            logging.error(f"寄存器 {register_name} 在 {machine_name} 中未定义")
            return False

        register_info = machine_config['registers'][register_name]
        if register_info.get('type') != 'real':
            logging.error(f"寄存器 {register_name} 不是Real类型")
            return False

        if register_info.get('read_only', False):
            logging.error(f"寄存器 {register_name} 为只读")
            return False

        client_info = self.edge_clients[machine_name]
        client = client_info['client']
        address = register_info['address']
        slave_id = client_info['config']['slave_id']

        try:
            # 将浮点数转换为两个16位寄存器
            raw_bytes = struct.pack('>f', value)
            reg1, reg2 = struct.unpack('>HH', raw_bytes)

            # 写入两个寄存器
            result = client.write_registers(address=address, values=[reg2, reg1], slave=slave_id)

            if not result.isError():
                logging.info(f"写入 {machine_name}.{register_name}: {value}")
                # regs = self._read_edge_raw_registers(machine_name, 33, 2)
                # logging.info(f"[RAW] 33-34 = {regs}")
                return True
            else:
                logging.error(f"写入 {machine_name}.{register_name} 失败: {result}")
                self.error_occurred.emit('edge_grinder', machine_name, f"写入寄存器失败: {result}")
                return False

        except Exception as e:
            logging.error(f"写入异常 - {machine_name}.{register_name}: {str(e)}")
            self.error_occurred.emit('edge_grinder', machine_name, f"写入异常: {str(e)}")
            return False

    def read_edge_grinder_data(self, machine_name: str) -> Dict[str, Any]:
        """读取指定侧磨机的所有数据"""
        results = {}

        if machine_name not in self.edge_clients:
            logging.error(f"侧磨机 {machine_name} 未连接")
            return results

        # 从具体机器配置中获取寄存器列表
        machine_config = self.edge_clients[machine_name]['config']
        if 'registers' not in machine_config:
            logging.error(f"{machine_name} 没有寄存器配置")
            return results

        for register_name, register_info in machine_config['registers'].items():
            if register_info['type'] == 'word':
                value = self._read_edge_word_register(machine_name, register_name)
            elif register_info['type'] == 'real':
                value = self._read_edge_real_register(machine_name, register_name)
            else:
                continue

            if value is not None:
                results[register_name] = value

        return results

    def add_edge_task(self, machine_name: str, process_type: int, thickness: float, bevel_angle: float):
        print("edge_clients:", self.edge_clients.keys())
        print("edge_queues:", self.edge_queues.keys())

        """添加侧磨机任务到队列"""
        if machine_name not in self.edge_clients:
            logging.error(f"{machine_name} 未连接")
            return

        # 一个任务包含所有参数
        self.edge_queues[machine_name].put((process_type, thickness, bevel_angle))
        logging.info(f"添加侧磨机任务: {machine_name}, 工艺={process_type}, 厚度={thickness}, 角度={bevel_angle}")

    # ==================== 监控线程管理 ====================

    def start_flipper_monitor(self):
        """启动翻板机监控"""
        if 'flipper' not in self.monitor_threads or not self.monitor_threads['flipper'].isRunning():
            self.monitor_threads['flipper'] = FlipperMonitorThread(self)
            self.monitor_threads['flipper'].start()
            logging.info("启动翻板机监控")
            return True
        return False

    def stop_flipper_monitor(self):
        """停止翻板机监控"""
        if 'flipper' in self.monitor_threads and self.monitor_threads['flipper'].isRunning():
            self.monitor_threads['flipper'].stop()
            logging.info("停止翻板机监控")
            return True
        return False

    def start_sorter_monitor(self):
        """启动分拣机监控"""
        if 'sorter' not in self.monitor_threads or not self.monitor_threads['sorter'].isRunning():
            self.monitor_threads['sorter'] = SorterMonitorThread(self)
            self.monitor_threads['sorter'].start()
            logging.info("启动分拣机监控")
            return True
        return False

    def stop_sorter_monitor(self):
        """停止分拣机监控"""
        if 'sorter' in self.monitor_threads and self.monitor_threads['sorter'].isRunning():
            self.monitor_threads['sorter'].stop()
            logging.info("停止分拣机监控")
            return True
        return False

    def start_edge_monitor(self):
        """启动侧磨机监控"""
        for machine_name in self.edge_machines.keys():
            if machine_name not in self.monitor_threads or not self.monitor_threads[machine_name].isRunning():
                self.monitor_threads[machine_name] = EdgeGrinderMonitorThread(self, machine_name)
                self.monitor_threads[machine_name].start()
                logging.info(f"启动侧磨机监控: {machine_name}")
        return True

    def stop_edge_monitor(self):
        """停止侧磨机监控"""
        for machine_name, thread in self.monitor_threads.items():
            if thread.isRunning():
                thread.stop()
                logging.info(f"停止侧磨机监控: {machine_name}")
        return True

    def stop_all_monitors(self):
        """停止所有监控线程"""
        stopped_count = 0
        for monitor_type, thread in self.monitor_threads.items():
            if thread.isRunning():
                thread.stop()
                stopped_count += 1

        logging.info(f"已停止 {stopped_count} 个监控线程")
        return stopped_count

    def disconnect_all(self):
        """断开所有设备连接"""
        self.stop_all_monitors()
        self.disconnect_flipper()
        self.disconnect_sorter()
        self.disconnect_edge_grinders()
        logging.info("已断开所有设备连接")


# ==================== 扫描枪类 ====================

class ScannerController:
    def __init__(self, controller_ref=None, scanner_configs: Dict[str, Dict] = None):
        import socket, threading
        from queue import Queue


        # 如果没有提供配置,使用默认配置
        if scanner_configs is None:
            scanner_configs = {
                'before_processing': {'ip': '0.0.0.0', 'port': 9004, 'name': '加工前扫描枪', 'enabled': True},
                'before_sorting': {'ip': '0.0.0.0', 'port': 9005, 'name': '分拣前扫描枪', 'enabled': True}
            }

        self.controller_ref = controller_ref
        self.scanner_configs = scanner_configs
        self.queue_before_processing = Queue()
        self.queue_before_sorting = Queue()
        self.sockets = {}  # 存储多个socket
        self.threads = []  # 存储所有服务器线程

        # 为每个启用的扫描枪创建TCP服务器
        for scanner_type, config in scanner_configs.items():
            if config.get('enabled', True):
                self.queues[scanner_type] = Queue()  # 为每个枪建立一个队列
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((config['ip'], config['port']))
                    sock.listen(5)
                    self.sockets[scanner_type] = sock

                    # 启动该扫描枪的TCP server线程
                    thread = threading.Thread(
                        target=self._start_server,
                        args=(scanner_type, sock),
                        daemon=True
                    )
                    thread.start()
                    self.threads.append(thread)

                    logging.info(f"扫描枪 [{config['name']}] TCP服务启动: {config['ip']}:{config['port']}")
                except Exception as e:
                    logging.error(f"扫描枪 [{config['name']}] 启动失败: {str(e)}")

    def _handle_client(self, conn, addr, scanner_type: str):
        config = self.scanner_configs[scanner_type]
        device_name = config['name']
        print(f"{device_name} 连接来自: {addr}")

        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print(f"{device_name}({addr}) 已断开")
                        break

                    text = data.decode("utf-8", errors="ignore").strip()

                    # 【新增核心逻辑】如果存在信号，向上层 UI 发射接收到的数据
                    if self.controller_ref and hasattr(self.controller_ref, 'scanner_data_received'):
                        self.controller_ref.scanner_data_received.emit(device_name, text)

                    # 根据扫描枪类型将数据放入对应队列
                    if scanner_type == "before_processing":
                        self.queue_before_processing.put(text)
                    elif scanner_type == "before_sorting":
                        self.queue_before_sorting.put(text)
                    elif scanner_type.startswith("scanner"):
                        # 对于新增的5个扫码枪，我们在上面已经发了信号，这里仅做终端打印
                        pass
                    else:
                        logging.warning(f"未知扫描枪类型: {scanner_type}")

                    print(f"[{device_name}] 扫描到: {text}")
                    conn.sendall(b"OK\n")

                except Exception as e:
                    logging.error(f"处理 {device_name}({addr}) 出现异常: {e}")
                    break

    def _start_server(self, scanner_type: str, sock):
        config = self.scanner_configs[scanner_type]
        print(f"TCP server [{config['name']}] listening on {config['ip']}:{config['port']}", flush=True)
        while True:
            try:
                conn, addr = sock.accept()
                import threading
                threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr, scanner_type),
                    daemon=True
                ).start()
            except Exception as e:
                logging.error(f"扫描枪 [{config['name']}] 接受连接失败: {str(e)}")
                break


# ==================== 监控线程类 ====================

class FlipperMonitorThread(QThread):
    """翻板机监控线程"""

    def __init__(self, controller: HardwareController):
        super().__init__()
        self.controller = controller
        self.is_running = False

    def flipper_start_action(self):
        """执行翻板机启动"""
        if self.controller.flipper_start_command():
            self.log_message("✅ 翻板机启动指令发送成功")
        else:
            self.log_message("❌ 翻板机启动指令发送失败")

    def flipper_stop_action(self):
        """执行翻板机停止"""
        if self.controller.flipper_stop_command():
            self.log_message("🛑 翻板机停止指令发送成功")
        else:
            self.log_message("❌ 翻板机停止指令发送失败")

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                task_request = self.controller._read_flipper_register('task_request')
                """
                加入了翻板机启停控制功能flipper_start_action()和flipper_stop_action()函数
                """
                # 2. 读取翻板机实时状态 (寄存器 2) - 用于 UI 显示
                flipper_status = self.controller._read_flipper_register('flipper_status')
                print(f"翻板机状态flipper_status: {flipper_status}")
                if flipper_status == 2:
                    self.flipper_start_action()
                    time.sleep(5)
                    self.flipper_stop_action()
                    time.sleep(3)

                # 如果task_request为1，则代表数据已经被取走，可以将二次加工信息进行投递，否则不进行投递
                if task_request == 1:
                    logging.info("检测到翻板机任务请求")

                    # 从队列发送任务
                    if not self.controller.flipper_task_queue.empty():
                        task = self.controller.flipper_task_queue.get()
                        task = 2

                        # 发送任务到翻板机
                        success = self.controller.flipper_send_task(task)
                        logging.info(f"发送到翻板机任务 {task}: {'成功' if success else '失败'}")

                        # 参数发送成功后,将task_request寄存器设置为1,通知PLC数据已就绪
                        if success:
                            # 等待一小段时间确保参数写入完成
                            self.msleep(100)

                            # 调用_write_flipper_task_request方法将寄存器设置为1
                            write_success = self.controller._write_flipper_task_request(1)

                            if write_success:
                                logging.info("翻板机已通知PLC数据就绪(task_request=1)")
                            else:
                                logging.error("翻板机通知PLC失败,task_request写入失败")
                        else:
                            logging.error("翻板机任务发送失败,不设置task_request")
                    else:
                        logging.warning("翻板机请求任务，但队列为空")

                    # 暂停10秒再继续轮询
                    for _ in range(10):
                        if not self.is_running:
                            break
                        self.msleep(1000)
                else:
                    self.msleep(500)

            except Exception as e:
                logging.error(f"翻板机监控线程异常: {str(e)}")
                self.msleep(1000)

    def stop(self):
        """停止监控"""
        self.is_running = False
        self.wait()

    def log_message(self, param):
        pass


class SorterMonitorThread(QThread):
    """分拣机监控线程"""

    def __init__(self, controller: HardwareController):
        super().__init__()
        self.controller = controller
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                task_request = self.controller._read_sorter_register('task_request')
                # 如果task_request为0，则代表数据已经被取走，可以将二次加工信息进行投递，否则不进行投递
                if task_request == 1:
                    logging.info("检测到分拣机任务请求")

                    if not self.controller.sorter_queue.empty():
                        station = self.controller.sorter_queue.get()

                        # 发送工位号到分拣机
                        success = self.controller.sorter_send_to_station(station)
                        logging.info(f"发送到分拣机工位 {station}: {'成功' if success else '失败'}")

                        # 参数发送成功后,将task_request寄存器设置为1,通知PLC数据已就绪
                        if success:
                            # 等待一小段时间确保参数写入完成
                            self.msleep(100)

                            # 调用_write_sorter_task_request方法将寄存器设置为1
                            write_success = self.controller._write_sorter_task_request(1)

                            if write_success:
                                logging.info("分拣机已通知PLC数据就绪(task_request=1)")
                            else:
                                logging.error("分拣机通知PLC失败,task_request写入失败")
                        else:
                            logging.error("分拣机工位号发送失败,不设置task_request")

                    # 暂停10秒再继续轮询
                    for _ in range(10):
                        if not self.is_running:
                            break
                        self.msleep(1000)
                else:
                    self.msleep(1000)  # 每秒轮询一次

            except Exception as e:
                logging.error(f"分拣机监控线程异常: {str(e)}")
                self.msleep(1000)

    def stop(self):
        """停止监控"""
        self.is_running = False
        self.wait()


class EdgeGrinderMonitorThread(QThread):
    """侧磨机监控线程"""

    def __init__(self, controller: HardwareController, machine_name: str):
        super().__init__()
        self.controller = controller
        self.machine_name = machine_name
        self.is_running = False

    def run(self):
        """监控主循环"""
        self.is_running = True
        while self.is_running:
            try:
                # 读取任务请求寄存器
                task_request = self.controller._read_edge_word_register(
                    self.machine_name, 'task_request'
                )

                # 如果task_request为0，则代表数据已经被取走，可以将二次加工信息进行投递，否则不进行投递
                if task_request == 0:
                    logging.info(f"{self.machine_name} 检测到任务请求")

                    edge_queue = self.controller.edge_queues[self.machine_name]
                    if not edge_queue.empty():
                        process_type, thickness, angle = edge_queue.get()
                        success = self.controller.send_edge_grinder_params(
                            self.machine_name, process_type, thickness, angle
                        )
                        logging.info(
                            f"{self.machine_name} 发送参数 {process_type}, {thickness}, {angle}: {'成功' if success else '失败'}"
                        )

                        # 二次加工参数发送成功后,将task_request寄存器设置为1,通知PLC数据已就绪
                        if success:
                            # 等待一小段时间确保参数写入完成
                            self.msleep(100)

                            # 调用_write_edge_task_request方法将寄存器设置为1
                            write_success = self.controller._write_edge_task_request(
                                self.machine_name, 1
                            )

                            if write_success:
                                logging.info(f"{self.machine_name} 已通知PLC数据就绪(task_request=1)")
                            else:
                                logging.error(f"{self.machine_name} 通知PLC失败,task_request写入失败")
                        else:
                            logging.error(f"{self.machine_name} 参数发送失败,不设置task_request")


                    else:
                        logging.warning(f"{self.machine_name} 请求任务，但队列为空")

                    # 暂停 10 秒再继续轮询
                    for _ in range(10):
                        if not self.is_running:
                            break
                        self.msleep(1000)
                else:
                    self.msleep(1000)  # 每秒轮询一次

            except Exception as e:
                logging.error(f"{self.machine_name} 监控线程异常: {str(e)}")
                self.msleep(1000)

    def stop(self):
        """停止监控"""
        self.is_running = False
        self.wait()


# ==================== UI绑定类 ====================

class HardwareControllerUI:
    """硬件控制器UI绑定类"""

    def __init__(self, main_window, hardware_controller: HardwareController):
        self.main_window = main_window
        self.controller = hardware_controller

        # 状态标签映射
        self.status_labels = {
            'flipper': 'flipperStateLabel',
            'sorter': 'sorterStateLabel',
            'qr_before_edge': 'qrBeforeEdgeStateLabel',
            'qr_before_sorter': 'qrBeforeSorterStateLabel',
            'edge_grinder': {
                '磨边机1号': 'edgeGrinderStateLabel1',
                '磨边机2号': 'edgeGrinderStateLabel2',
                '磨边机3号': 'edgeGrinderStateLabel3',
                '磨边机4号': 'edgeGrinderStateLabel4',
            }

        }

        self.setup_connections()
        self.setup_signals()

    def setup_connections(self):
        """设置按钮连接"""
        try:
            # 分拣机控制按钮
            self.main_window.connect_sorter_btn.clicked.connect(self.connect_sorter)
            self.main_window.disconnect_sorter_btn.clicked.connect(self.disconnect_sorter)
            self.main_window.start_sorter_monitor_btn.clicked.connect(self.start_sorter_monitor)
            self.main_window.stop_sorter_monitor_btn.clicked.connect(self.stop_sorter_monitor)

            # 翻板机控制按钮
            self.main_window.connect_flipper_btn.clicked.connect(self.connect_flipper)
            self.main_window.disconnect_flipper_btn.clicked.connect(self.disconnect_flipper)
            self.main_window.start_flipper_monitor_btn.clicked.connect(self.start_flipper_monitor)
            self.main_window.stop_flipper_monitor_btn.clicked.connect(self.stop_flipper_monitor)
            # 新增：翻板机启停按钮 (假设 UI 中按钮名称如下)
            if hasattr(self.main_window, 'flipper_start_btn'):
                self.main_window.flipper_start_btn.clicked.connect(self.flipper_start_action)
            if hasattr(self.main_window, 'flipper_stop_btn'):
                self.main_window.flipper_stop_btn.clicked.connect(self.flipper_stop_action)

            # 侧磨机控制按钮
            self.main_window.connect_edge_btn.clicked.connect(self.connect_edge_grinders)
            self.main_window.disconnect_edge_btn.clicked.connect(self.disconnect_edge_grinders)
            self.main_window.start_edge_monitor_btn.clicked.connect(self.start_edge_monitor)
            self.main_window.stop_edge_monitor_btn.clicked.connect(self.stop_edge_monitor)

            # 全部PLC控制按钮（预留）
            self.main_window.connect_all_btn.clicked.connect(self.connect_qr_scanners)
            self.main_window.disconnect_all_btn.clicked.connect(self.disconnect_qr_scanners)
            self.main_window.start_all_monitor_btn.clicked.connect(self.start_qr_monitor)
            self.main_window.stop_all_monitor.clicked.connect(self.stop_qr_monitor)

        except AttributeError as e:
            logging.warning(f"某些按钮未找到: {e}")

    def setup_signals(self):
        """设置硬件控制器信号连接"""
        self.controller.connection_status_changed.connect(self.on_connection_status_changed)
        self.controller.data_received.connect(self.on_data_received)
        self.controller.error_occurred.connect(self.on_error_occurred)
        self.controller.scan_flag_detected.connect(self.on_scan_flag_detected)
        self.controller.task_request_detected.connect(self.on_task_request_detected)
        # 【新增】对接扫码枪信号
        self.controller.scanner_data_received.connect(self.on_scanner_data_received)

    # ==================== 按钮事件处理 ====================

    def connect_sorter(self):
        """连接分拣机"""
        self.log_message("正在连接分拣机...")
        success = self.controller.connect_sorter()
        if success:
            self.log_message("分拣机连接成功")
        else:
            self.log_message("分拣机连接失败")

    def disconnect_sorter(self):
        """断开分拣机"""
        self.controller.disconnect_sorter()
        self.log_message("已断开分拣机连接")

    def start_sorter_monitor(self):
        """启动分拣机监控"""
        if self.controller.start_sorter_monitor():
            self.log_message("分拣机监控已启动")
        else:
            self.log_message("分拣机监控启动失败")

    def stop_sorter_monitor(self):
        """停止分拣机监控"""
        if self.controller.stop_sorter_monitor():
            self.log_message("分拣机监控已停止")

    def connect_flipper(self):
        """连接翻板机"""
        self.log_message("正在连接翻板机...")
        success = self.controller.connect_flipper()
        if success:
            self.log_message("翻板机连接成功")
        else:
            self.log_message("翻板机连接失败")

    def disconnect_flipper(self):
        """断开翻板机"""
        self.controller.disconnect_flipper()
        self.log_message("已断开翻板机连接")

    def start_flipper_monitor(self):
        """启动翻板机监控"""
        if self.controller.start_flipper_monitor():
            self.log_message("翻板机监控已启动")
        else:
            self.log_message("翻板机监控启动失败")

    def stop_flipper_monitor(self):
        """停止翻板机监控"""
        if self.controller.stop_flipper_monitor():
            self.log_message("翻板机监控已停止")

    # ==================== 新增动作处理 ====================
    def flipper_start_action(self):
        """执行翻板机启动"""
        if self.controller.flipper_start_command():
            self.log_message("✅ 翻板机启动指令发送成功")
        else:
            self.log_message("❌ 翻板机启动指令发送失败")

    def flipper_stop_action(self):
        """执行翻板机停止"""
        if self.controller.flipper_stop_command():
            self.log_message("🛑 翻板机停止指令发送成功")
        else:
            self.log_message("❌ 翻板机停止指令发送失败")

    def connect_edge_grinders(self):
        """连接侧磨机"""
        self.log_message("正在连接所有侧磨机...")
        success = self.controller.connect_edge_grinders()
        if success:
            self.log_message("侧磨机连接完成")
        else:
            self.log_message("侧磨机连接失败")

    def disconnect_edge_grinders(self):
        """断开侧磨机"""
        self.controller.disconnect_edge_grinders()
        self.log_message("已断开所有侧磨机连接")

    def start_edge_monitor(self):
        """启动侧磨机监控"""
        if self.controller.start_edge_monitor():
            self.log_message("侧磨机监控已启动")
        else:
            self.log_message("侧磨机监控启动失败")

    def stop_edge_monitor(self):
        """停止侧磨机监控"""
        if self.controller.stop_edge_monitor():
            self.log_message("侧磨机监控已停止")

    def connect_qr_scanners(self):
        """连接二维码扫描器（预留）"""
        self.log_message("二维码扫描器功能待实现...")

    def disconnect_qr_scanners(self):
        """断开二维码扫描器（预留）"""
        self.log_message("二维码扫描器功能待实现...")

    def start_qr_monitor(self):
        """启动二维码监控（预留）"""
        self.log_message("二维码监控功能待实现...")

    def stop_qr_monitor(self):
        """停止二维码监控（预留）"""
        self.log_message("二维码监控功能待实现...")

    # ==================== 信号处理 ====================

    def on_connection_status_changed(self, device_type: str, device_name: str, connected: bool):
        """处理连接状态变化"""
        status_text = "已连接" if connected else "未连接"
        color = "green" if connected else "red"

        # 更新对应的状态标签
        if device_type == 'flipper':
            self.update_status_label('flipper', f"翻板机: {status_text}", color)
        elif device_type == 'sorter':
            self.update_status_label('sorter', f"分拣机: {status_text}", color)
        elif device_type == 'edge_grinder':
            # 处理多台侧磨机
            label_map = self.status_labels.get('edge_grinder', {})
            label_name = label_map.get(device_name)
            if label_name:
                self.update_status_label(f"edge_grinder", f"{device_name}: {status_text}", color,
                                         device_name=device_name)
            else:
                logging.warning(f"未找到 {device_name} 的标签")

        self.log_message(f"{device_name} 连接状态: {status_text}")

    # def on_data_received(self, device_type: str, device_name: str, register_name: str, value):
    #     """处理接收到的数据"""
    #     # 如果寄存器是 task_request 且值为 0，则不记录
    #     if register_name == "task_request" and value == 0:
    #         return
    #
    #     self.log_message(f"数据接收: {device_name}.{register_name} = {value}")

    # ==================== 新增：扫码枪数据接收 ====================
    def on_scanner_data_received(self, device_name: str, data: str):
        """处理新扫码枪传回的数据"""
        # 1. 写入底部日志框
        self.log_message(f"[扫码枪] {device_name} 扫码成功: {data}")

        # 2. 调用主窗口的 UI 更新方法更新看板
        if hasattr(self.main_window, 'update_scanner_ui'):
            self.main_window.update_scanner_ui(device_name, data)

    def on_data_received(self, device_type: str, device_name: str, register_name: str, value):
        """处理接收到的数据并更新 UI"""
        # 排除掉轮询时的 0 值干扰日志
        if register_name in ["task_request", "flipper_status"] and value == 0:
            return

        # 处理翻板机状态显示 (寄存器名称对应 config 中的 flipper_status)
        if device_type == 'flipper' and register_name == 'flipper_status':
            status_map = {1: "运行中", 2: "待机", 3: "故障", 0: "离线"}
            status_desc = status_map.get(value, f"未知({value})")

            # 更新状态标签 (假设 UI 中有 flipperRealStatusLabel)
            if hasattr(self.main_window, 'flipperRealStatusLabel'):
                label = self.main_window.flipperRealStatusLabel
                label.setText(f"翻板机状态: {status_desc}")
                # 根据状态改变颜色
                color = "green" if value == 1 else "orange" if value == 2 else "red"
                label.setStyleSheet(f"color: {color}; font-weight: bold;")

        # 只有重要数据才记录到日志框
        if register_name not in ["flipper_status", "task_request"]:
            self.log_message(f"数据接收: {device_name}.{register_name} = {value}")

    def on_error_occurred(self, device_type: str, device_name: str, error_msg: str):
        """处理错误信息"""
        self.log_message(f"错误 [{device_name}]: {error_msg}")

    def on_scan_flag_detected(self, device_type: str, device_name: str):
        """处理扫码标志检测"""
        self.log_message(f"🔍 {device_name} 检测到扫码标志！")
        # 这里可以添加后续业务逻辑

    def on_task_request_detected(self, device_type: str, device_name: str):
        """处理任务请求检测"""
        self.log_message(f"📋 {device_name} 检测到任务请求！")
        # 这里可以添加后续业务逻辑

    def update_status_label(self, label_type: str, text: str, color: str, device_name: str = None):
        """更新状态标签，支持单台设备和多台设备"""
        try:
            label_name = None

            if device_name is None:
                # 单台设备或非字典情况
                label_name = self.status_labels.get(label_type)
            else:
                # 多台设备情况，label_type 对应的是字典
                labels_dict = self.status_labels.get(label_type)
                if isinstance(labels_dict, dict):
                    label_name = labels_dict.get(device_name)

            if label_name and hasattr(self.main_window, label_name):
                label = getattr(self.main_window, label_name)
                label.setText(text)
                label.setStyleSheet(f"color: {color}; font-weight: bold;")

        except Exception as e:
            logging.warning(f"更新状态标签失败: {e}")

    def log_message(self, message: str):
        """添加日志消息"""
        try:
            if hasattr(self.main_window, 'logPlainTextEdit'):
                current_time = time.strftime("%H:%M:%S")
                log_entry = f"[{current_time}] {message}"
                self.main_window.logPlainTextEdit.appendPlainText(log_entry)

                # 自动滚动到底部
                cursor = self.main_window.logPlainTextEdit.textCursor()
                cursor.movePosition(cursor.End)
                self.main_window.logPlainTextEdit.setTextCursor(cursor)
            else:
                # 如果没有日志控件，输出到控制台
                print(f"LOG: {message}")

        except Exception as e:
            logging.warning(f"添加日志消息失败: {e}")

    # ==================== 业务方法 ====================

    def flipper_turn_action(self):
        """翻板机执行翻板动作"""
        success = self.controller.flipper_turn_command()
        if success:
            self.log_message("翻板机执行翻板指令成功")
        else:
            self.log_message("翻板机执行翻板指令失败")
        return success

    def flipper_pass_action(self):
        """翻板机直接通过动作"""
        success = self.controller.flipper_pass_command()
        if success:
            self.log_message("翻板机执行通过指令成功")
        else:
            self.log_message("翻板机执行通过指令失败")
        return success

    def sorter_send_to_station(self, station: int):
        """分拣机发送到指定工位"""
        success = self.controller.sorter_send_to_station(station)
        if success:
            self.log_message(f"分拣机发送到{station}号工位指令成功")
        else:
            self.log_message(f"分拣机发送到{station}号工位指令失败")
        return success

    def send_edge_grinder_params(self, machine_name: str, process_type: int, thickness: float, angle: float):
        """发送侧磨机工艺参数"""
        success = self.controller.send_edge_grinder_params(machine_name, process_type, thickness, angle)
        if success:
            self.log_message(f"向{machine_name}发送工艺参数成功")
        else:
            self.log_message(f"向{machine_name}发送工艺参数失败")
        return success

    def get_edge_grinder_data(self, machine_name: str):
        """获取侧磨机数据"""
        data = self.controller.read_edge_grinder_data(machine_name)
        if data:
            self.log_message(f"成功读取{machine_name}数据: {data}")
        else:
            self.log_message(f"读取{machine_name}数据失败")
        return data


# ==================== 使用示例 ====================

if __name__ == "__main__":
    """
    使用示例：

    # 在你的主程序中这样使用：

    from HardwareController import HardwareController, HardwareControllerUI

    # 创建硬件控制器
    hardware_controller = HardwareController()

    # 创建UI绑定（假设main_window是你的主窗口）
    hardware_ui = HardwareControllerUI(main_window, hardware_controller)

    # 现在所有按钮都已经自动绑定到相应的功能
    """

    print("硬件控制模块加载完成")
    print("请在主程序中导入并使用 HardwareController 和 HardwareControllerUI 类")

    # ====================== 测试动态加载配置文件 ======================

    cfg = HardwareConfig()
    print(cfg.FLIPPER_CONFIG)
    print(cfg.SORTER_CONFIG)
    print(cfg.EDGE_GRINDERS)

    # ========================== 测试翻板机 ===========================

    # controller = HardwareController()
    # controller.connect_flipper()

    # 【添加任务】
    # controller.add_flipper_task(1)  # 翻板
    # controller.add_flipper_task(2)  # 通过
    #
    # # 【启动轮询】
    # controller.start_flipper_polling()
    #
    # # 【需要停止时】
    # time.sleep(150)
    # controller.stop_flipper_polling()

    # ========================== 测试侧磨机 ===========================
    #
    # controller = HardwareController()
    # controller.connect_edge_grinders()
    #
    # # 【添加任务到磨边机1号队列】
    # controller.edge_queues['磨边机1号'].put((1, 12.5, 30.0))  # 工艺: 直边, 厚度 12.5, 角度 30
    # controller.edge_queues['磨边机2号'].put((2, 15.0, 45.0))
    # controller.edge_queues['磨边机3号'].put((3, 25.0, 45.0))
    # controller.edge_queues['磨边机4号'].put((4, 35.0, 45.0))
    #
    # # 【启动所有侧磨机监控】
    # controller.start_edge_monitor()
    # time.sleep(20)
    # controller.edge_queues['磨边机1号'].put((1, 22.5, 80.0))  # 工艺: 直边, 厚度 12.5, 角度 30
    # # 运行一段时间后停止
    # time.sleep(150)
    # controller.stop_edge_monitor()

    # ========================== 测试扫描枪 ===========================

    # 【测试连接和接收数据】
    # hc = HardwareController()
    # print("HardwareController 启动完毕，TCP 扫描枪服务已启动")
    # # 主线程保持运行
    # import time
    # while True:
    #     time.sleep(1)


    # 【测试分拣前和加工前的扫描枪扫到数据后做的操作】：DB中的processing_type的值对翻板机和侧磨机的任务队列分别进行投递，
    """
        - 队列存在：初始化 HardwareController 时就创建了
        - 客户端连接失败：任务无法投递，队列保持为空
        以上两点保证了侧磨机不会执行历史加工操作！
    """
    # 创建硬件控制器
    hc = HardwareController()
    hc.connect_flipper()
    hc.connect_sorter()
    hc.connect_edge_grinders()
    time.sleep(5)
    # 模拟加工前扫描
    hc.scanner_controller.queue_before_processing.put(
        "before_processing http://stone/25-5-181A177"
    )

    # 模拟分拣前扫描
    hc.scanner_controller.queue_before_sorting.put(
        "before_sorting http://stone/25-5-181A177"
    )

    # 给处理线程一点时间
    time.sleep(1)

    # 查看翻板机队列
    flipper_tasks = []
    while not hc.flipper_task_queue.empty():
        flipper_tasks.append(hc.flipper_task_queue.get())
    print("【测试代码】翻板机队列:", flipper_tasks)

    # 查看四台侧磨机队列
    for name, q in hc.edge_queues.items():
        tasks = []
        while not q.empty():
            tasks.append(q.get())
        print(f"【测试代码】{name} 队列:", tasks)

    # 查看分拣机队列
    sorter_tasks = []
    while not hc.sorter_queue.empty():
        sorter_tasks.append(hc.sorter_queue.get())
    print("【测试代码】分拣机队列:", sorter_tasks)

    time.sleep(100)
