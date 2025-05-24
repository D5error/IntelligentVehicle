import json
import logging
import socket
import threading
from lib import util, vehicle

class UDPClient:
    def __init__(self, ip, port, send_port, vehicle_name):
        self.config = util.load_config()
        self.send_port = send_port
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", port))
        self.vehicle_data = vehicle.VehicleData()
        self.all_vehicle_data = vehicle.AllVehicleData()
        self.vehicle_name = vehicle_name

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)  

    def start(self):
        threading.Thread(target=self.receive, daemon=True).start()

    # 接收车辆数据
    def receive(self):
        is_print_vehicles = self.config.print_vehicles

        while True:
            data0, addr = self.sock.recvfrom(10240)
            data1 = data0.decode()

            data = json.loads(data1)
            try:
                for car in data['vehicles']:
                    if car['name'] == self.vehicle_name:
                        self.vehicle_data.name = car['name']
                        self.vehicle_data.x = car['x']
                        self.vehicle_data.y = car['y']
                        self.vehicle_data.yaw = car['yaw']
                        self.vehicle_data.speed = car['speed']
                    
                    # 保存所有车辆状态，包括自己
                    vehicle_data = vehicle.VehicleData()
                    vehicle_data.name = car['name']
                    vehicle_data.x = car['x']
                    vehicle_data.y = car['y']
                    vehicle_data.yaw = car['yaw']
                    vehicle_data.speed = car['speed']
                    self.all_vehicle_data.update_vehicle_data(vehicle_data)

                # 打印所有车辆状态
                if is_print_vehicles:
                    print(self.all_vehicle_data.get_all_vehicle_data())

            except Exception as e:
                self.logger.error("my_udp.py:receive():", e)

    def send(self, message):
        self.sock.sendto(message.encode(), (self.ip, self.send_port))
        # self.logger.info("send message: " + message)

    def get_vehicle_state(self):
        return self.vehicle_data

    def get_all_vehicle_state(self) -> vehicle.AllVehicleData:
        return self.all_vehicle_data

    def send_control_command(self, v, w):
        message = '{"name":"' + self.vehicle_name + '","vx":%f,"vz":%f}' % (v, w)
        self.send(message)
