# _*_ coding: utf-8 -*_
import common.IKapBoard as IKapBoard
import ctypes
import time
import threading
import queue

# 硬件分块后单次内存极小（约16MB），放大环形队列让 PCIe 传输更加丝滑
DEFINE_FRAME_COUNT = 8

# =====================================================================
# 【终极防御 1】：全局静态回调气囊
# 坚决防止 C++ 底层硬件中断引发的野指针崩溃 (0xC0000409)
# =====================================================================
CMPFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_void_p)


def _global_dummy(p):
    pass


GLOBAL_DUMMY_CB = CMPFUNC(_global_dummy)


class SaveThread(threading.Thread):
    """专门负责将队列中的 RAW 分块数据异步追加/拼接成大图"""

    def __init__(self, data_queue):
        super().__init__()
        self.queue = data_queue
        self.running = True
        self.daemon = True

    def run(self):
        while self.running or not self.queue.empty():
            try:
                task = self.queue.get(timeout=1)
                data, save_path, write_mode = task

                # write_mode 为 'wb' 时创建新文件，为 'ab' 时追加拼接数据
                with open(save_path, write_mode) as f:
                    f.write(data)

                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"写入文件失败: {e}")


class IKapBoardGrabLineTrigger:
    def __init__(self, save_path):
        self.m_hDev = ctypes.c_void_p(None)
        self.m_nCurFrameIndex = ctypes.c_uint(0)
        self.save_path = save_path

        self.data_queue = queue.Queue(maxsize=100)
        self.save_worker = SaveThread(self.data_queue)
        self.save_worker.start()

        self.polling_thread = None
        self.is_polling = False

        # ==== 大图拼接控制变量 ====
        self.target_height = 24000  # 默认最终需要的大图总高度
        self.hw_height = 1000  # 硬件底层安全的 DMA 分块高度

    @staticmethod
    def GetBoardCount():
        res, nBoardCount = IKapBoard.IKapGetBoardCount(IKapBoard.IKBoardPCIE)
        for nIndex in range(0, nBoardCount):
            res, strBoardName = IKapBoard.IKapGetBoardName(IKapBoard.IKBoardPCIE, nIndex)
            if res == IKapBoard.IK_RTN_OK:
                print(f"Board {nIndex}: {strBoardName}")
        return nBoardCount

    def OpenDevice(self, nIndex):
        self.m_hDev = IKapBoard.IKapOpen(IKapBoard.IKBoardPCIE, nIndex)
        return self.m_hDev is not None and self.m_hDev != -1

    def IsOpenDevice(self):
        return self.m_hDev is not None and self.m_hDev != -1

    def CloseDevice(self):
        if self.IsOpenDevice():
            self.is_polling = False
            if self.polling_thread:
                self.polling_thread.join(timeout=1.0)
            self.save_worker.running = False
            IKapBoard.IKapClose(self.m_hDev)

    def LoadConfigurationFile(self, strFileName):
        # 兼容外部传入的 bytes 或 str，确保文件路径不越界
        if isinstance(strFileName, str):
            strFileName = strFileName.encode('gbk', errors='ignore')
        res = IKapBoard.IKapLoadConfigurationFromFile(self.m_hDev, strFileName)
        return res == IKapBoard.IK_RTN_OK

    def SetLineTrigger(self):
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_CC1_SOURCE,
                                    IKapBoard.IKP_CC_SOURCE_VAL_INTEGRATION_SIGNAL1)
        if res != IKapBoard.IK_RTN_OK: return False
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE,
                                    IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE_VAL_SHAFT_ENCODER1)
        return res == IKapBoard.IK_RTN_OK

    def SetResolution(self, width, height):
        """
        【终极防御 2】：恢复 Width 设置，并强行拦截庞大的 Height。
        将几百兆的巨大内存块切分为硬件驱动能安全消化的 1000 行小块。
        """
        if self.IsOpenDevice():
            self.target_height = height
            self.hw_height = 1000

            # 必须设置宽度，否则硬件内存错位秒退！
            IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_WIDTH, width)
            IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_HEIGHT, self.hw_height)

            print(f"已重置安全采集块: 物理宽 {width}, 硬件单块高 {self.hw_height} (将无缝拼成 {height} 行)")
            return True
        return False

    def StartGrab(self, nFrameCount=0):
        if not self.IsOpenDevice():
            return False

        # 【终极防御 3】：恢复 PCIe 大内存块与异步传输配置
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_PCIE_KERNAL_BLOCK_SIZE,
                              IKapBoard.IKP_PCIE_KERNAL_BLOCK_SIZE_VAL_16M)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_TRANSFER_MODE, IKapBoard.IKP_FRAME_TRANSFER_ASYNCHRONOUS)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT, DEFINE_FRAME_COUNT)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_TIME_OUT, -1)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_GRAB_MODE, IKapBoard.IKP_GRAB_NON_BLOCK)

        # 挂载全局安全回调
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStart, GLOBAL_DUMMY_CB, ctypes.c_void_p(0))
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStop, GLOBAL_DUMMY_CB, ctypes.c_void_p(0))
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady, GLOBAL_DUMMY_CB, ctypes.c_void_p(0))

        print(f"正在启动底层采集流...")
        res = IKapBoard.IKapStartGrab(self.m_hDev, nFrameCount)

        if res == IKapBoard.IK_RTN_OK:
            self.is_polling = True
            self.polling_thread = threading.Thread(target=self.poll_buffer_loop, daemon=True)
            self.polling_thread.start()
            return True
        return False

    def poll_buffer_loop(self):
        """后台高频安全拼接车间"""
        print("SDK: Polling Thread Started")

        lines_collected = 0
        current_save_path = ""

        while self.is_polling and self.IsOpenDevice():
            try:
                # =====================================================================
                # 【终极防御 4】：128字节宽裕安全气囊
                # 防止 SDK 版本更新导致的 IKAPBUFFERSTATUS 结构体变大，直接写穿内存
                # =====================================================================
                bufferStatus_raw = ctypes.create_string_buffer(128)
                res = IKapBoard.libIKapBoard.IKapGetBufferStatus(self.m_hDev, self.m_nCurFrameIndex.value,
                                                                 ctypes.byref(bufferStatus_raw))

                if res == IKapBoard.IK_RTN_OK:
                    # 强转并只读取最核心的第一个标志位 uFull
                    uFull = ctypes.cast(bufferStatus_raw, ctypes.POINTER(ctypes.c_uint)).contents.value

                    if uFull == 1:
                        res_info, nFrameSize = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_SIZE)
                        pUserBuffer = ctypes.c_void_p(0)
                        IKapBoard.IKapGetBufferAddress(self.m_hDev, self.m_nCurFrameIndex.value, pUserBuffer)

                        if pUserBuffer.value:
                            # 将安全的小块数据抓取出来
                            raw_data = ctypes.string_at(pUserBuffer.value, nFrameSize)

                            # ---- 精密无缝拼接逻辑 ----
                            bytes_per_line = nFrameSize // self.hw_height if self.hw_height > 0 else 0
                            lines_needed = self.target_height - lines_collected
                            lines_to_write = min(self.hw_height, lines_needed)

                            valid_bytes = lines_to_write * bytes_per_line
                            data_to_write = raw_data[:valid_bytes]

                            # 判断是创建新文件(wb)还是追加拼图(ab)
                            if lines_collected == 0:
                                timestamp = time.strftime('%H-%M-%S', time.localtime())
                                current_save_path = f"{self.save_path}/{timestamp}_full.raw"
                                write_mode = 'wb'
                            else:
                                write_mode = 'ab'

                            try:
                                self.data_queue.put_nowait((data_to_write, current_save_path, write_mode))
                            except queue.Full:
                                pass

                            lines_collected += lines_to_write

                            # 行数积攒达标，输出完美的超大 RAW 图像
                            if lines_collected >= self.target_height:
                                print(f"✅ 成功无缝拼接完成一张 {self.target_height} 行的大图: {current_save_path}")
                                lines_collected = 0

                        # 立刻把缓冲区释放还给硬件继续扫描
                        IKapBoard.IKapReleaseBuffer(self.m_hDev, self.m_nCurFrameIndex.value)
                        self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT
                    else:
                        time.sleep(0.002)
                else:
                    time.sleep(0.002)
            except Exception as e:
                print(f"❌ 轮询线程内异常: {e}")
                time.sleep(0.1)

    def StopGrab(self):
        """停止采集"""
        self.is_polling = False
        if self.polling_thread:
            self.polling_thread.join(timeout=1.0)
        if self.IsOpenDevice():
            IKapBoard.IKapStopGrab(self.m_hDev)
        return True