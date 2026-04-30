# _*_ coding: utf-8 -*_
import IKapBoard
import ctypes
import os
import time
import numpy as np
import cv2

# 定义缓冲帧数
DEFINE_FRAME_COUNT = 1


class SingleCameraLineTrigger:
    def __init__(self, save_path="./output_images"):
        self.m_hDev = ctypes.c_void_p(None)
        self.m_nCurFrameIndex = ctypes.c_uint(0)
        self.m_bufferData = ctypes.c_void_p(None)

        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # 回调函数占位
        self.grabStartProc = ctypes.c_void_p(None)
        self.grabStopProc = ctypes.c_void_p(None)
        self.frameReadyProc = ctypes.c_void_p(None)

    def OpenDevice(self, nIndex=0):
        """打开指定索引的采集卡"""
        self.m_hDev = IKapBoard.IKapOpen(IKapBoard.IKBoardPCIE, nIndex)
        if self.m_hDev == None or self.m_hDev == -1:
            print("打开采集卡失败，请检查硬件连接！")
            return False
        print(f"成功打开采集卡 (Index: {nIndex})")
        return True

    def LoadConfigurationFile(self, strFileName):
        """加载配置文件，增加防崩溃的安全加载"""
        abs_path = os.path.normpath(os.path.abspath(strFileName))
        if not os.path.exists(abs_path):
            print(f"找不到配置文件: {abs_path}")
            return False

        # 尝试编码以防中文路径导致的 DLL 崩溃
        for enc in ['gbk', 'utf-8']:
            try:
                path_bytes = abs_path.encode(enc)
                char_array = ctypes.create_string_buffer(path_bytes)
                if IKapBoard.IKapLoadConfigurationFromFile(self.m_hDev, char_array.value):
                    print(f"配置文件加载成功: {abs_path}")
                    return True
            except Exception as e:
                continue
        print("配置文件加载失败！")
        return False

    def SetLineTrigger(self):
        """核心：将触发源设置为编码器线触发"""
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_CC1_SOURCE,
                                    IKapBoard.IKP_CC_SOURCE_VAL_INTEGRATION_SIGNAL1)
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE,
                                    IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE_VAL_SHAFT_ENCODER1)
        if res != IKapBoard.IK_RTN_OK:
            print("设置编码器线触发失败！")
            return False
        print("已成功配置编码器线触发模式。")
        return True

    def StartGrab(self):
        """配置并启动采集"""
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT, DEFINE_FRAME_COUNT)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_TIME_OUT, -1)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_GRAB_MODE, IKapBoard.IKP_GRAB_NON_BLOCK)
        IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_TRANSFER_MODE,
                              IKapBoard.IKP_FRAME_TRANSFER_SYNCHRONOUS_NEXT_EMPTY_WITH_PROTECT)

        # 注册回调函数
        self.frameReadyProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onFrameReadyProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady, self.frameReadyProc,
                                       ctypes.c_void_p(None))

        res = IKapBoard.IKapStartGrab(self.m_hDev, 0)
        if res != IKapBoard.IK_RTN_OK:
            print("启动采集失败！")
            return False
        print("采集已启动，等待编码器信号触发...")
        return True

    def StopGrab(self):
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady)
        IKapBoard.IKapStopGrab(self.m_hDev)
        IKapBoard.IKapClose(self.m_hDev)
        print("采集已停止，设备已关闭。")

    def onFrameReadyProc(self, pParam):
        """当编码器触发足够行数拼成一帧时，进入此回调"""
        print("\n--> 收到完整一帧图像数据！")
        pUserBuffer = ctypes.c_void_p(None)
        res, bufferStatus = IKapBoard.IKapGetBufferStatus(self.m_hDev, self.m_nCurFrameIndex)

        if bufferStatus.uFull == 1:
            res, nFrameSize = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_SIZE)
            IKapBoard.IKapGetBufferAddress(self.m_hDev, self.m_nCurFrameIndex, pUserBuffer)

            # 获取宽高和通道信息，用于还原图像
            _, nWidth = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_WIDTH)
            _, nHeight = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_HEIGHT)
            _, nImageType = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_TYPE)

            # 将底层内存数据拷贝出
            bufferData = (nFrameSize * ctypes.c_ubyte).from_address(pUserBuffer.value)

            # 使用 Numpy 转为图像矩阵
            try:
                img_array = np.frombuffer(bufferData, dtype=np.uint8)

                if nImageType == IKapBoard.IKP_IMAGE_TYPE_VAL_MONOCHROME:
                    # 黑白相机
                    img_array = img_array.reshape((nHeight, nWidth))
                else:
                    # 彩色相机 (RGB 或 BGR)
                    img_array = img_array.reshape((nHeight, nWidth, 3))

                # 去除全0行（防黑边逻辑，沿用你原始代码的习惯）
                # 注意：如果图像太大，这一步会稍微耗时
                # img_array = img_array[[not np.all(img_array[i] == 0) for i in range(img_array.shape[0])], ...]

                # 保存图像
                filename = f"{self.save_path}/Grab_{time.strftime('%Y%m%d_%H%M%S')}.bmp"
                cv2.imwrite(filename, img_array)
                print(f"--> 图像成功输出至: {filename}")

            except Exception as e:
                print(f"图像转换/保存失败: {e}")

        # 循环复位帧索引
        self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT


if __name__ == "__main__":
    # 检查是否有板卡
    res, count = IKapBoard.IKapGetBoardCount(IKapBoard.IKBoardPCIE)
    if count == 0:
        print("未检测到 IKap 采集卡！")
        os._exit(0)

    demo = SingleCameraLineTrigger(save_path="./demo_output")

    # 1. 打开卡 0
    if not demo.OpenDevice(0):
        os._exit(0)

    # 2. 替换为你本地真实的 vlcf 配置文件路径
    config_path = r"C:/Users/Administrator/Desktop/Setting/test_color.vlcf"
    if not demo.LoadConfigurationFile(config_path):
        demo.StopGrab()
        os._exit(0)

    # 3. 设置线触发为轴编码器
    if not demo.SetLineTrigger():
        demo.StopGrab()
        os._exit(0)

    # 4. 启动采图
    if demo.StartGrab():
        print("\n系统正在运行。请转动流水线编码器以提供触发脉冲。")
        print("按回车键 (Enter) 退出程序...\n")
        input()  # 阻塞主线程，等待回调函数在后台线程中执行

    # 5. 退出清理
    demo.StopGrab()