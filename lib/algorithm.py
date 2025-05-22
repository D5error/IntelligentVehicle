import numpy as np
import math


# 纯跟踪控制算法：https://blog.csdn.net/Ronnie_Hu/article/details/115817922
# https://blog.csdn.net/weixin_42301220/article/details/124882144
def pure_pursuit(curr_x, curr_y, curr_yaw, route, Ld, L):
    # 计算预瞄点
    target_point = get_target_point(curr_x, curr_y, route, Ld)

    # 计算alpha
    dx = target_point[0] - curr_x
    dy = target_point[1] - curr_y
    alpha = math.atan2(dy, dx) - curr_yaw
    
    # 计算转向角
    delta = math.atan2(2.0 * L * np.sin(alpha), Ld)

    return delta, target_point

# 寻找预瞄点
def get_target_point(curr_x, curr_y, route, Ld):
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
