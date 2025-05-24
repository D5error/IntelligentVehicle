import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import patches
from collections import deque
from lib import util, vehicle
from lib.algorithm import config
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题
route = util.load_route()

# 一个可视化窗口
class Minimap:
    def __init__(self):
        self.config = util.load_config()

        plt.ion()
        self.init_legend()
        self.trajectory_x = deque(maxlen=config.trajectory_length)
        self.trajectory_y = deque(maxlen=config.trajectory_length)
        self.update_count = 0

        self.ax.set_xlim(-5, 165)   # x轴范围
        self.ax.set_ylim(-5, 165)   # y轴范围

        # 加载背景图片（路径根据你的实际情况修改）
        self.bg_image = mpimg.imread(self.config.map_path)
        plt.imshow(self.bg_image, extent=[0, 160, 0, 160], aspect='auto') 

        # 绘制参考路径
        self.plot_route()

        # 绘制转弯点
        self.plot_turning_points()

        self.fig.canvas.flush_events()

    # 绘制参考路径
    def plot_route(self):
        # 更新参考路径
        ref_x = [p[0] for p in route]
        ref_y = [p[1] for p in route]
        self.route_line.set_data(ref_x, ref_y)

    # 绘制转弯点
    def plot_turning_points(self):
        x, y = [], []
        for p in self.config.turning_points:
            x.append(p.x)
            y.append(p.y)
            circle = patches.Circle((p.x, p.y), self.config.braking_distance, color='k', fill=False)
            self.ax.add_patch(circle)

        self.turning_point.set_offsets(list(zip(x, y)))

    # 初始化图例
    def init_legend(self):
        self.fig, self.ax = plt.subplots()
        self.route_line, = self.ax.plot([], [], 'r--', label="路径")
        self.vehicle_point = self.ax.scatter([], [], c='b', label="小车位置")
        self.lookahead_point = self.ax.scatter([], [], c='y', label="预瞄点")
        self.traj_line, = self.ax.plot([], [], 'k-', label="小车轨迹")
        self.turning_point = self.ax.scatter([], [], c='k', label="转弯点")
        self.ax.scatter([], [], c='r', label="其他车辆")
        self.ax.legend()

    def update_plot(self, vehicle_data: vehicle.VehicleData, target_point, all_vehicles_data: dict[str, vehicle.VehicleData]):
        if not self.config.minimap_tracking:
            return

        # 更新自己车辆位置
        self.vehicle_point.set_offsets([[vehicle_data.x, vehicle_data.y]])

        # 更新其他车辆位置
        other_vehicle_x = []
        other_vehicle_y = []
        for v in all_vehicles_data.values():
            if v.name != vehicle_data.name:
                other_vehicle_x.append(v.x)
                other_vehicle_y.append(v.y)
        if hasattr(self, 'other_vehicle'):
            self.other_vehicle.remove()
        self.other_vehicle = self.ax.scatter([], [], c='r', label="其他车辆")
        self.other_vehicle.set_offsets(list(zip(other_vehicle_x, other_vehicle_y)))

        # 更新轨迹
        self.trajectory_x.append(vehicle_data.x)
        self.trajectory_y.append(vehicle_data.y)
        self.traj_line.set_data(self.trajectory_x, self.trajectory_y)

        # 更新预瞄点
        self.lookahead_point.set_offsets([target_point[0], target_point[1]])

        # 刷新图像
        self.update_count += 1
        if self.update_count % config.update_count == 0:  # 每 5 次更新一次图形
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            self.update_count = 0
