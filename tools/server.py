import socket
import json
import threading

# 测试用的服务器类，用于接收JSON数据 
class Server:
    def __init__(self, callback, host='0.0.0.0', port=6666):
        self.host = host
        self.port = port
        self.callback = callback

        # 创建一个UDP套接字
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 绑定套接字到地址和端口
        server_address = (host, port)
        self.sock.bind(server_address)


    def udp_json_server(self):
        print(f"UDP监听{self.host}:{self.port}")
        
        while True:
            data, address = self.sock.recvfrom(4096)  # 接收最多4096字节的数据
            
            # 解码
            data = data.decode()

            if data:
                # 解码接收到的JSON数据
                try:
                    json_data = json.loads(data)
                    self.callback(json_data['x'], json_data['y'])
                    
                except json.JSONDecodeError:
                    print(f"收到来自{address}的数据，但是无法解析为JSON")

    def start(self):
        threading.Thread(target=self.udp_json_server, daemon=True).start()
