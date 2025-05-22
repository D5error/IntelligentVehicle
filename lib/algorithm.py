import numpy as np
import math
from lib.util import load_route, load_config


# 加载配置参数
config = load_config("config.yaml")
route = load_route(config["route_path"])
L = config["L"]
Ld = config["Ld"]
dynamic_Ld = config["dynamic_Ld"]
k = config["k"]
c = config["c"]
braking_distance = config["braking_distance"]
turning_speed = config["turning_speed"]
turning_points = config["turning_points"]
speed = config["speed"]


# 纯跟踪控制算法：https://blog.csdn.net/Ronnie_Hu/article/details/115817922
# https://blog.csdn.net/weixin_42301220/article/details/124882144
def pure_pursuit(curr_x, curr_y, curr_yaw, v_x):
    # 计算预瞄点
    target_point = get_target_point(curr_x, curr_y)

    # 计算alpha
    dx = target_point[0] - curr_x
    dy = target_point[1] - curr_y
    alpha = math.atan2(dy, dx) - curr_yaw
    
    # 动态调整预瞄距离
    if dynamic_Ld:
        Ld = k * v_x + c

    print(Ld)
    # 计算转向角
    delta = math.atan2(2.0 * L * np.sin(alpha), Ld)

    return delta, target_point

# 寻找预瞄点
def get_target_point(curr_x, curr_y):
    # 找到最近的路径点
    min_idx = np.argmin([np.hypot(x - curr_x, y - curr_y) for x, y in route])
    
    # 计算预瞄点
    for i in range(min_idx + 1, len(route)):
        distance = np.hypot(route[i][0] - curr_x, route[i][1] - curr_y)
        if distance > Ld:
            min_idx = i
            break

    target_point = route[min_idx]
    return target_point

# 动态控制车辆速度，车辆距离转弯点小于安全距离时，车辆减速
def dynamic_speed(curr_x, curr_y):
    new_speed = speed

    for turning_point in turning_points:
        x = turning_point['x']
        y = turning_point['y']
        distance_to_turning_point = np.hypot(curr_x - x, curr_y - y)
        if distance_to_turning_point < braking_distance:
            new_speed = turning_speed
            break

    return new_speed