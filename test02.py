# -*- coding: utf-8 -*-
import time
import signal
from ctypes import *
from configs.IKapBoard import *

# 全局变量
g_h_dev = None
g_trigger_count = 0
g_running = True

# Ctrl+C 退出
def signal_handler(signum, frame):
    global g_running
    print("\n退出程序...")
    g_running = False

signal.signal(signal.SIGINT, signal_handler)

# 【正确】回调函数定义（3参数，匹配SDK原生格式）
EVENT_CALLBACK = CFUNCTYPE(None, IKAP_HANDLE, c_uint32, c_void_p)
def trigger_callback(h_dev, event_type, ctx):
    global g_trigger_count
    g_trigger_count += 1
    t = "上升沿" if event_type == IKEVENT_INPUT_RISING_EDGE else "下降沿"
    print(f"📶 触发成功！次数：{g_trigger_count} | {t}")

# 主程序
def main():
    global g_h_dev
    try:
        print("="*50)
        print("IKap IO触发检测【终极版】")
        print("="*50)

        # 1. 枚举设备
        ret, cnt = IKapGetBoardCount(IKBoardALL)
        if not cnt:
            print("未找到设备")
            return

        # 2. 打开设备
        g_h_dev = IKapOpen(IKBoardALL, 0)
        if not g_h_dev:
            print("打开设备失败")
            return
        print("✅ 设备打开成功")

        # ====================== 【关键】IO触发全套配置 ======================
        print("\n配置通用输入1(GPI1)边沿触发...")
        IKapSetInfo(g_h_dev, IKP_DISABLE_IO_EVENT, 0)                  # 开启IO事件
        IKapSetInfo(g_h_dev, IKP_GENERAL_INPUT1_POLARITY, 0)          # 高电平有效
        IKapSetInfo(g_h_dev, IKP_GENERAL_INPUT1_PROTECT_MODE, 0)      # 关闭防抖
        IKapSetInfo(g_h_dev, IKP_GENERAL_INPUT1_MIN_WIDTH, 0)         # 关闭最小宽度限制
        IKapSetInfo(g_h_dev, IKP_GENERAL_INPUT1_TRIGGER_MODE, 0)       # 边沿触发模式
        IKapSetInfo(g_h_dev, IKP_GENERAL_INPUT1_SAMPLE_MODE, 2)        # 仅监听上升沿（测试最稳定）

        # 3. 注册回调
        cb = EVENT_CALLBACK(trigger_callback)
        IKapRegisterCallback(g_h_dev, IKEVENT_INPUT_RISING_EDGE, cb, None)
        print("✅ 回调注册成功")

        # ====================== 【最重要】必须启动采集！ ======================
        # 启动空采集（不保存图像，仅激活硬件IO事件）
        IKapStartGrab(g_h_dev, 0)
        print("✅ 采集已启动，等待触发信号...")
        print("\n🔥 实时检测中，按 Ctrl+C 退出")

        # 循环等待
        while g_running:
            time.sleep(0.1)

    except Exception as e:
        print(f"异常：{e}")
    finally:
        if g_h_dev:
            IKapStopGrab(g_h_dev)
            IKapUnRegisterCallback(g_h_dev, 0xFFFFFFFF)
            IKapClose(g_h_dev)
            print(f"\n✅ 设备关闭 | 总触发次数：{g_trigger_count}")

if __name__ == "__main__":
    main()