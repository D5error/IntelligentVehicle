import math
import time
from my_udp import UDPClient
from lib.util import *
from lib.algorithm import pure_pursuit
from lib.minimap import Minimap



class Control:
    def __init__(self):
        self.config = load_config("config.yaml")
        
        net = self.config["net"]
        self.udp_client = UDPClient(*split_net(net))

        self.m_v = 0
        self.m_x = 0
        self.m_y = 0
        self.m_yaw = 0

        self.control_rate = 10  # hz
        
    def control_node(self):
        start_time = time.time()
        L = self.config["L"]
        Ld = self.config["Ld"]
        speed = self.config["speed"]
        route_path = self.config["route_path"]

        # 加载路径
        route = load_route(route_path)

        # 加载小地图
        minimap = Minimap(self.config["minimap"])

        while True:
            vehicle_data = self.udp_client.get_vehicle_state()
            self.m_x = vehicle_data.x
            self.m_y = vehicle_data.y
            self.m_yaw = vehicle_data.yaw / 180 * math.pi

            delta, target_point = pure_pursuit(self.m_x, self.m_y, self.m_yaw, route, Ld, L)
            # print(f"当前坐标: ({self.m_x: .3f} -> {target_point[0]}, {self.m_y: .3f} -> {target_point[1]}), yaw: {self.m_yaw}")


            v = speed
            w = delta

            self.udp_client.send_control_command(v, w)

            # 更新小地图
            minimap.update_plot(vehicle_data, route, target_point)

            elapsed_time = time.time() - start_time
            sleep_time = max((1.0 / self.control_rate) - elapsed_time, 0.0)
            time.sleep(sleep_time)
            start_time = time.time()


if __name__ == '__main__':
    control = Control()
    control.udp_client.start()
    control.control_node()
