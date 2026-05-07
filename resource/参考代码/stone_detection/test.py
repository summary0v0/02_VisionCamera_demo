import cv2
import matplotlib.pyplot as plt
import numpy as np

rows = 8000
cols = 8320
channels = 3
img = np.fromfile(r'D:\tmp_dir2\2023-09-27_14-23-25.raw', dtype='uint8')
img = img.reshape(rows, cols, channels)
plt.imshow(img[..., ::-1])
plt.show()

import serial
import serial.tools.list_ports
import time

# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])


ser = serial.Serial("COM20", 9600)  # 打开 COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():  # 判断串口是否成功打开
    print("打开串口成功。")
else:
    print("打开串口失败。")


write_len = ser.write("dmod=1#300\r".encode('utf-8'))
print("串口发出{}个字节。".format(write_len))
# 读取串口输入信息并输出。
# while True:
time.sleep(5)
com_input = ser.read_all()
if com_input:   # 如果读取结果非空，则输出
    print(com_input)

ser.close()
if ser.isOpen():  # 判断串口是否关闭
    print("串口未关闭。")
else:
    print("串口已关闭。")