# _*_ coding: utf-8 -*_
import common.IKapBoard as IKapBoard
import ctypes
import threading
import queue

# 定义每轮采集的帧数
DEFINE_FRAME_COUNT = 3


class SaveThread(threading.Thread):
    """专门负责将队列中的 RAW 数据写入硬盘的线程"""

    def __init__(self, data_queue):
        super().__init__()
        self.queue = data_queue
        self.running = True
        self.daemon = True

    def run(self):
        while self.running or not self.queue.empty():
            try:
                # 阻塞式获取任务，超时时间1秒
                task = self.queue.get(timeout=1)
                data, save_path = task

                # 执行写入操作
                with open(save_path, 'wb') as f:
                    f.write(data)

                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"写入文件失败: {e}")


class IKapBoardGrabLineTrigger:
    def __init__(self, save_path):
        # 设备句柄
        self.m_hDev = ctypes.c_void_p(None)
        self.m_nCurFrameIndex = ctypes.c_uint(0)
        self.save_path = save_path

        # 实例化数据队列和保存线程
        self.data_queue = queue.Queue(maxsize=100)
        self.save_worker = SaveThread(self.data_queue)
        self.save_worker.start()

        # 核心修复：必须在实例属性中持有回调函数对象的引用，防止被垃圾回收
        self.c_start_cb = None
        self.c_stop_cb = None
        self.c_ready_cb = None
        self.c_timeout_cb = None
        self.c_lost_cb = None

    @staticmethod
    def GetBoardCount():
        """获取系统识别到的板卡数量 """
        res, nBoardCount = IKapBoard.IKapGetBoardCount(IKapBoard.IKBoardPCIE)
        for nIndex in range(0, nBoardCount):
            res, strBoardName = IKapBoard.IKapGetBoardName(IKapBoard.IKBoardPCIE, nIndex)
            if res == IKapBoard.IK_RTN_OK:
                print(f"Board {nIndex}: {strBoardName}")
        return nBoardCount

    def OpenDevice(self, nIndex):
        """打开指定索引的板卡设备 """
        self.m_hDev = IKapBoard.IKapOpen(IKapBoard.IKBoardPCIE, nIndex)
        return self.m_hDev is not None and self.m_hDev != -1

    def IsOpenDevice(self):
        return self.m_hDev is not None and self.m_hDev != -1

    def CloseDevice(self):
        if self.IsOpenDevice():
            self.save_worker.running = False
            IKapBoard.IKapClose(self.m_hDev)

    def LoadConfigurationFile(self, strFileName):
        """加载配置文件 (.vlcf) """
        # 注意：此处传入的应是经过 ctypes 转换的字节流或字符串
        res = IKapBoard.IKapLoadConfigurationFromFile(self.m_hDev, strFileName)
        return res == IKapBoard.IK_RTN_OK

    def SetLineTrigger(self):
        """设置线触发模式相关参数 """
        # 设置 CC1 信号源 [cite: 12, 13]
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_CC1_SOURCE,
                                    IKapBoard.IKP_CC_SOURCE_VAL_INTEGRATION_SIGNAL1)
        if res != IKapBoard.IK_RTN_OK: return False

        # 设置触发源为编码器1 [cite: 12, 13]
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE,
                                    IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE_VAL_SHAFT_ENCODER1)
        return res == IKapBoard.IK_RTN_OK

    def StartGrab(self, nFrameCount=0):
        """配置并启动采集"""
        # 1. 还原为最基础、最安全的采集设置
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT, DEFINE_FRAME_COUNT)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_TIME_OUT, -1)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_GRAB_MODE, IKapBoard.IKP_GRAB_NON_BLOCK)

        # 2. 注册回调函数 (确保引用在函数运行期间不被释放)
        CMPFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_void_p)
        self.c_start_cb = CMPFUNC(self.onGrabStartProc)
        self.c_stop_cb = CMPFUNC(self.onGrabStopProc)
        print(f'开始执行onFrameReadyProc函数')
        self.c_ready_cb = CMPFUNC(self.onFrameReadyProc)

        # 3. 注册
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStart, self.c_start_cb, ctypes.c_void_p(0))
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStop, self.c_stop_cb, ctypes.c_void_p(0))
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady, self.c_ready_cb, ctypes.c_void_p(0))

        # 4. 执行正式启动
        print(f"正在启动底层采集流...")
        res = IKapBoard.IKapStartGrab(self.m_hDev, nFrameCount)
        return res == IKapBoard.IK_RTN_OK

    def onFrameReadyProc(self, pParam):
        """安全排雷模式：剔除所有容易引发堆栈溢出的 C++ 结构体查询"""
        IKapBoard.IKapReleaseBuffer(self.m_hDev, self.m_nCurFrameIndex.value)
        print(f'无法执行onFrameReadyProc函数')
        try:
            print(f"✅ 成功收到一帧！(队列: {self.save_path}, 索引: {self.m_nCurFrameIndex.value})")

            # 【核心修复】：直接告诉采集卡底层“这块内存可以回收继续拍下一张了”
            # 完全不调用带有危险结构体的 SDK 查询函数
            IKapBoard.IKapReleaseBuffer(self.m_hDev, self.m_nCurFrameIndex.value)

        except Exception as e:
            # 如果有 Python 报错，确保它被打印出来而不是直接闪退
            print(f"❌ 回调函数内发生异常: {e}")

        finally:
            # 安全轮转索引，等待下一帧到来
            self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT

    # def StartGrab(self, nFrameCount=0):
    #     """配置并启动采集"""
    #     # 1. 增强稳定性设置：设置内核块大小为 16M (针对大分辨率图像)
    #     IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_PCIE_KERNAL_BLOCK_SIZE,
    #                           IKapBoard.IKP_PCIE_KERNAL_BLOCK_SIZE_VAL_16M)
    #
    #     # 2. 基础采集设置
    #     IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT, DEFINE_FRAME_COUNT)
    #     IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_TIME_OUT, -1)
    #     IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_GRAB_MODE, IKapBoard.IKP_GRAB_NON_BLOCK)
    #
    #     # 3. 关键修改：图像传输模式改为异步平衡模式 (减少堆栈压力)
    #     IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_TRANSFER_MODE,
    #                           IKapBoard.IKP_FRAME_TRANSFER_ASYNCHRONOUS)
    #
    #     # 4. 注册回调函数 (确保引用在函数运行期间不被释放)
    #     # 必须使用 WINFUNCTYPE 来匹配 Windows C++ SDK 的 __stdcall 调用约定！
    #     CMPFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_void_p)
    #     self.c_start_cb = CMPFUNC(self.onGrabStartProc)
    #     self.c_stop_cb = CMPFUNC(self.onGrabStopProc)
    #     self.c_ready_cb = CMPFUNC(self.onFrameReadyProc)
    #
    #     # 注册
    #     # 修复4：将 None 替换为 ctypes.c_void_p(0)，防止 ctypes 传递 Python 对象的内存地址给 C++
    #     IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStart, self.c_start_cb, ctypes.c_void_p(0))
    #     IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStop, self.c_stop_cb, ctypes.c_void_p(0))
    #     IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady, self.c_ready_cb, ctypes.c_void_p(0))
    #
    #     # 5. 最后执行正式启动
    #     print(f"正在启动底层采集流...")
    #     res = IKapBoard.IKapStartGrab(self.m_hDev, nFrameCount)
    #     return res == IKapBoard.IK_RTN_OK
    #
    # def onFrameReadyProc(self, pParam):
    #     """安全排雷模式：仅验证底层是否稳定，不进行大内存拷贝"""
    #     try:
    #         # 1. 尝试获取状态
    #         res, bufferStatus = IKapBoard.IKapGetBufferStatus(self.m_hDev, self.m_nCurFrameIndex.value)
    #
    #         if res == IKapBoard.IK_RTN_OK:
    #             print(f"✅ 成功收到一帧！(队列: {self.save_path}, 索引: {self.m_nCurFrameIndex.value})")
    #
    #             # 安全起见，我们这次先不去调用 ctypes.string_at 复制内存
    #             # 只告诉采集卡：“这帧我看过了，你把内存回收吧”
    #             IKapBoard.IKapReleaseBuffer(self.m_hDev, self.m_nCurFrameIndex.value)
    #         else:
    #             print(f"⚠️ 收到空帧或异常帧，状态码: {res}")
    #
    #     except Exception as e:
    #         # 确保回调里的错误不会直接闪退，而是打印出来
    #         print(f"❌ 回调函数内发生严重异常: {e}")
    #
    #     finally:
    #         # 轮转索引
    #         self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT

    # def onFrameReadyProc(self, pParam):
    #     """图像就绪回调：严禁在此函数内做耗时操作 """
    #     pUserBuffer = ctypes.c_void_p(0)  # 初始化为0
    #
    #     # 修复1：明确使用 .value 取出整数值
    #     res, bufferStatus = IKapBoard.IKapGetBufferStatus(self.m_hDev, self.m_nCurFrameIndex.value)
    #
    #     if res == IKapBoard.IK_RTN_OK and bufferStatus.uFull == 1:
    #         # 获取当前帧的内存地址和大小
    #         res, nFrameSize = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_SIZE)
    #
    #         # 修复2：去掉 ctypes.byref，因为 IKapBoard.py 中已经封装了 byref
    #         IKapBoard.IKapGetBufferAddress(self.m_hDev, self.m_nCurFrameIndex.value, pUserBuffer)
    #
    #         # 修复3：加上安全判断，确保内存地址有效后再拷贝
    #         if pUserBuffer.value:
    #             # 快速拷贝内存数据到 Python 字节对象
    #             raw_data = ctypes.string_at(pUserBuffer.value, nFrameSize)
    #
    #             # 生成文件名并送入后端队列处理
    #             timestamp = time.strftime('%H-%M-%S', time.localtime())
    #             save_name = f"{self.save_path}/{timestamp}_index{self.m_nCurFrameIndex.value}.raw"
    #
    #             try:
    #                 self.data_queue.put_nowait((raw_data, save_name))
    #             except queue.Full:
    #                 print("警告：保存队列已满，丢弃当前帧")
    #
    #         # 必须释放缓冲区给硬件重新使用
    #         IKapBoard.IKapReleaseBuffer(self.m_hDev, self.m_nCurFrameIndex.value)
    #
    #     # 轮转索引
    #     self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT

    # 其他回调仅打印日志
    def onGrabStartProc(self, pParam):
        print("SDK: Grab Started")

    def onGrabStopProc(self, pParam):
        print("SDK: Grab Stopped")

    def onTimeoutProc(self, pParam):
        print("SDK: Grab Timeout")

    def onFrameLostProc(self, pParam):
        print("SDK: Frame Lost")

    def StopGrab(self):
        """停止采集并注销回调 """
        if self.IsOpenDevice():
            for event in [IKapBoard.IKEvent_GrabStart, IKapBoard.IKEvent_GrabStop,
                          IKapBoard.IKEvent_FrameReady, IKapBoard.IKEvent_TimeOut,
                          IKapBoard.IKEvent_FrameLost]:
                IKapBoard.IKapUnRegisterCallback(self.m_hDev, event)
            IKapBoard.IKapStopGrab(self.m_hDev)
        return True

    def SetResolution(self, width, height):
        """
        强制设置采集卡缓冲区的物理宽高，防止大图引发堆栈溢出
        """
        if self.IsOpenDevice():
            # IKP_IMAGE_WIDTH 和 IKP_IMAGE_HEIGHT 是 IKap SDK 设置图像宽高的标准常量
            # 如果你的 common.IKapBoard 中常量名略有不同，请以你的文件为准
            IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_WIDTH, width)
            IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_HEIGHT, height)
            print(f"已手动重置采集卡缓冲区分辨率: {width} x {height}")
            return True
        return False
