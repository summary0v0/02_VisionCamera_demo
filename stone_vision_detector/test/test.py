# -*- coding: utf-8 -*-
import time
from configs.IKapBoard import *  # 导入封装好的SDK

def grab_image_demo():
    """
    IKapBoard 图像采集Demo
    功能：枚举设备 -> 打开设备 -> 采集1帧图像 -> 保存为JPG -> 释放资源
    """
    h_dev = None  # 设备句柄
    try:
        # ====================== 步骤1：枚举硬件设备 ======================
        print("正在枚举硬件设备...")
        # 枚举所有类型设备(USB3.0/PCIe/CXP)
        ret, board_count = IKapGetBoardCount(IKBoardALL)
        if ret != IKStatus_Success or board_count <= 0:
            print("错误：未找到任何IKap硬件设备！")
            return
        print(f"找到 {board_count} 个设备")

        # ====================== 步骤2：打开第一个设备 ======================
        print("正在打开设备...")
        # 打开第一个设备(索引0)
        h_dev = IKapOpen(IKBoardALL, 1)
        if not h_dev:
            print("错误：打开设备失败！")
            return
        print("设备打开成功")

        # ====================== 步骤3：读取相机基础参数 ======================
        # 读取图像宽度
        ret, width = IKapGetInfo(h_dev, IKP_IMAGE_WIDTH)
        # 读取图像高度
        ret, height = IKapGetInfo(h_dev, IKP_IMAGE_HEIGHT)
        # 读取图像位深
        ret, bit_depth = IKapGetInfo(h_dev, IKP_DATA_FORMAT)
        print(f"图像参数：宽度={width}, 高度={height}, 位深={bit_depth}bit")

        # ====================== 步骤4：启动图像采集 ======================
        print("启动采集...")
        # 采集1帧图像
        ret = IKapStartGrab(h_dev, 1)
        if ret != IKStatus_Success:
            print("错误：启动采集失败！")
            return

        # 等待采集完成（阻塞等待）
        print("等待图像采集完成...")
        ret = IKapWaitGrab(h_dev)
        if ret != IKStatus_Success:
            print("错误：采集超时/失败！")
            IKapStopGrab(h_dev)
            return

        # ====================== 步骤5：保存图像到本地 ======================
        save_path = b"capture_image.jpg"  # 保存路径（bytes格式）
        # 保存第0帧缓冲区图像，JPEG高质量
        IKapSaveBuffer(h_dev, 0, save_path, IKP_JPEG_QUALITYGOOD)
        print(f"图像保存成功！路径：{save_path.decode()}")

        # ====================== 步骤6：停止采集 ======================
        IKapStopGrab(h_dev)
        print("采集已停止")

    except Exception as e:
        print(f"程序异常：{str(e)}")

    finally:
        # ====================== 步骤7：关闭设备，释放资源 ======================
        if h_dev:
            IKapClose(h_dev)
            print("设备已关闭，资源释放完成")

if __name__ == "__main__":
    grab_image_demo()