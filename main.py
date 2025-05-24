import math
import time
from my_udp import UDPClient
from lib import util, algorithm, minimap, vehicle


class Control:
    def __init__(self):
        net = util.load_config().net
        self.udp_client = UDPClient(*util.split_net(net))

        self.m_v = 0
        self.m_x = 0
        self.m_y = 0
        self.m_yaw = 0

        self.control_rate = 10  # hz
        
    def control_node(self):
        start_time = time.time()

        # 加载小地图
        map = minimap.Minimap()

        while True:
            # 获取当前车辆的状态
            vehicle_data = self.udp_client.get_vehicle_state()
            self.m_x = vehicle_data.x
            self.m_y = vehicle_data.y
            self.m_yaw = vehicle_data.yaw / 180 * math.pi

            # 获取全局车辆
            all_vehicles = self.udp_client.get_all_vehicle_state()

            # 纯跟踪算法
            delta, target_point = algorithm.pure_pursuit(self.m_x, self.m_y, self.m_yaw, vehicle_data.speed)

            # 冲突检测
            fake_car = vehicle.VehicleData() # 测试用
            fake_car.set_vehicle_stake(100, 153, "D5") # 测试用
            all_vehicles.update_vehicle_data(fake_car) # 测试用
            is_conflict = algorithm.conflict_detection(vehicle_data, all_vehicles.get_data())

            # 更新速度和转向角
            if is_conflict:
                v = 0
                w = 0
                print("刹车")

            else:
                v = algorithm.dynamic_speed(self.m_x, self.m_y)
                w = delta

            # 更新小地图
            map.update_plot(vehicle_data, target_point, all_vehicles.get_data())

            # 发送控制命令
            self.udp_client.send_control_command(v, w)

            # 控制频率
            elapsed_time = time.time() - start_time
            sleep_time = max((1.0 / self.control_rate) - elapsed_time, 0.0)
            time.sleep(sleep_time)
            start_time = time.time()


if __name__ == '__main__':
    control = Control()
    control.udp_client.start()
    control.control_node()
