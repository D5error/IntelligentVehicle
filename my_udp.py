import json
import logging
import socket
import threading
from lib.vehicle import VehicleData, AllVehicleData
from lib.util import load_config

class UDPClient:
    def __init__(self, ip, port, send_port, vehicle_name):
        self.send_port = send_port
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", port))
        self.vehicle_data = VehicleData()
        self.all_vehicle_data = AllVehicleData()
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
        threading.Thread(target=self.get_global_state, daemon=True).start()

    def receive(self):
        while True:
            data0, addr = self.sock.recvfrom(10240)
            data1 = data0.decode()

            data = json.loads(data1)
            try:
                for vehicle in data['vehicles']:
                    if vehicle['name'] == self.vehicle_name:
                        self.vehicle_data.name = vehicle['name']
                        self.vehicle_data.x = vehicle['x']
                        self.vehicle_data.y = vehicle['y']
                        self.vehicle_data.yaw = vehicle['yaw']
                        self.vehicle_data.speed = vehicle['speed']

            except Exception as e:
                self.logger.error(e)

    def send(self, message):
        self.sock.sendto(message.encode(), (self.ip, self.send_port))
        self.logger.info("send message: " + message)

    def get_vehicle_state(self):
        return self.vehicle_data

    def get_global_state(self):
        config = load_config("config.yaml")
        is_print_vehicles = config['print_vehicles']

        while True:
            data0, addr =self.sock.recvfrom(10240)
            data1 = data0.decode()
            data = json.loads(data1)

            # 解析数据
            try:
                for vehicle in data['vehicles']:
                    vehicle_data = VehicleData()
                    vehicle_data.name = vehicle['name']
                    vehicle_data.x = vehicle['x']
                    vehicle_data.y = vehicle['y']
                    vehicle_data.yaw = vehicle['yaw']
                    vehicle_data.speed = vehicle['speed']
                    self.all_vehicle_data.update_vehicle_data(vehicle_data)

                # 打印所有车辆状态
                if is_print_vehicles:
                    print(self.all_vehicle_data.get_all_vehicle_data())

            except Exception as e:
                self.logger.error(e)

    def send_control_command(self, v, w):
        message = '{"name":"' + self.vehicle_name + '","vx":%f,"vz":%f}' % (v, w)
        self.send(message)
