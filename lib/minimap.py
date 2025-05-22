import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from lib.vehicle import VehicleData
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 一个可视化窗口
class Minimap:
    def __init__(self, use_minimap=False):
        self.use_minimap = use_minimap
        if not self.use_minimap:
            return
            
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.route_line, = self.ax.plot([], [], 'r--', label="路径")
        self.vehicle_point = self.ax.scatter([], [], c='b', label="小车位置")
        self.lookahead_point = self.ax.scatter([], [], c='y', label="预瞄点")
        self.traj_line, = self.ax.plot([], [], 'k-', label="小车轨迹")
        self.ax.legend()
        self.trajectory_x = []
        self.trajectory_y = []

        self.ax.set_xlim(-5, 165)   # x轴范围
        self.ax.set_ylim(-5, 165)   # y轴范围

        # 加载背景图片（路径根据你的实际情况修改）
        self.bg_image = mpimg.imread('./map_small.png')
        # 查看图片
        plt.imshow(self.bg_image, extent=[0, 160, 0, 160], aspect='auto') 
        self.ax.imshow(self.bg_image, extent=[0, 160, 0, 160], aspect='auto', alpha=0.5)

    def update_plot(self, vehicle_data: VehicleData, route, target_point):
        if not self.use_minimap:
            return

        # 更新参考路径
        ref_x = [p[0] for p in route]
        ref_y = [p[1] for p in route]
        self.route_line.set_data(ref_x, ref_y)

        # 获取小车坐标
        x = vehicle_data.x
        y = vehicle_data.y

        # 更新车辆位置（scatter 需要重新设置数据）
        if len(self.trajectory_x) == 0:
            self.vehicle_point = self.ax.scatter([x], [y], c='b')
        else:
            self.vehicle_point.set_offsets([[x, y]])

        # 更新轨迹
        self.trajectory_x.append(x)
        self.trajectory_y.append(y)
        self.traj_line.set_data(self.trajectory_x, self.trajectory_y)

        # 更新预瞄点
        self.lookahead_point.set_offsets([target_point[0], target_point[1]])

        # 自动缩放
        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
