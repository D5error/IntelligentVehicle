import numpy as np
import math
from lib import util, vehicle


# 加载配置参数
config = util.load_config()
route = util.load_route()


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
    Ld = config.k * v_x + config.c if config.dynamic_Ld else config.Ld

    # 计算转向角
    delta = math.atan2(2.0 * config.L * np.sin(alpha), Ld)

    return delta, target_point

# 寻找预瞄点
def get_target_point(curr_x, curr_y):
    # 找到最近的路径点
    min_idx = np.argmin([np.hypot(x - curr_x, y - curr_y) for x, y in route])
    
    # 计算预瞄点
    for i in range(min_idx + 1, len(route)):
        distance = np.hypot(route[i][0] - curr_x, route[i][1] - curr_y)
        if distance > config.Ld:
            min_idx = i
            break

    target_point = route[min_idx]
    return target_point

# 动态控制车辆速度，车辆距离转弯点小于安全距离时，车辆减速
def dynamic_speed(curr_x, curr_y):
    new_speed = config.speed

    for turning_point in config.turning_points:
        x = turning_point['x']
        y = turning_point['y']
        distance_to_turning_point = np.hypot(curr_x - x, curr_y - y)
        if distance_to_turning_point < config.braking_distance:
            new_speed = config.turning_speed
            break

    return new_speed

# 冲突检测
def conflict_detection(my_vehicle: vehicle.VehicleData, all_vehicles: dict[str, vehicle.VehicleData]):
    for vehicle_name in all_vehicles:
        other_vehicle = all_vehicles[vehicle_name]
        if other_vehicle.name == my_vehicle.name:
            continue

        distance = np.hypot(my_vehicle.x - other_vehicle.x, my_vehicle.y - other_vehicle.y)
        if distance < config.safe_distance:
            print(f"距离车辆'{other_vehicle.name}'{distance}m，低于安全距离！")
            return True
    return False
