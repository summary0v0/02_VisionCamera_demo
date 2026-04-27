"""摄像头采集模块。

负责实时取流、单帧抓拍，以及后续接入工业相机 SDK 的适配。
"""


class CameraCapture:
    """封装摄像头初始化与图像采集逻辑。"""

    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def open(self):
        """打开摄像头或初始化采集设备。"""
        raise NotImplementedError("待实现摄像头打开逻辑")

    def read(self):
        """读取一帧图像。"""
        raise NotImplementedError("待实现图像读取逻辑")

    def release(self):
        """释放摄像头或采集资源。"""
        raise NotImplementedError("待实现资源释放逻辑")
