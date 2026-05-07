import socket
import threading
import time

HOST = "127.0.0.1"  # 服务器 IP
PORT = 9004         # 服务器端口

def simulate_scanner(device_name, messages):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for msg in messages:
            full_msg = f"{device_name}: {msg}"
            s.sendall(full_msg.encode("utf-8"))
            data = s.recv(1024)
            print(f"[{device_name}] 收到服务器应答: {data.decode().strip()}")
            time.sleep(1)

# 两台模拟扫描枪
scanner_before_processing_msgs = ["ID1001", "ID1002", "ID1003"]
scanner_before_sorting_msgs = ["ID2001", "ID2002", "ID2003"]

# 用线程模拟同时扫码
threading.Thread(target=simulate_scanner, args=("before_processing", scanner_before_processing_msgs)).start()
threading.Thread(target=simulate_scanner, args=("before_sorting", scanner_before_sorting_msgs)).start()
