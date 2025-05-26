import matplotlib.pyplot as plt
import json
import os
import sys
import numpy as np
sys.path.append(os.getcwd())
import matplotlib.image as mpimg
from lib.util import load_config


def draw_route(file_name):
    fig, ax = plt.subplots()

    config = load_config()
    bg_image = mpimg.imread(config.map_path)
        
    # 查看图片
    plt.imshow(bg_image, extent=[0, 160, 0, 160], aspect='auto') 


    # 存储坐标的列表
    XY = {"X": [], "Y": []}

    def on_move(event):
        if event.button == 1:  # 左键
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                XY["X"].append(x)
                XY["Y"].append(y)
                ax.scatter(x, y, color='red')
                fig.canvas.draw_idle()  # 更新图形

    # 连接鼠标移动事件
    cid = fig.canvas.mpl_connect('motion_notify_event', on_move)
    plt.show()

    # 将记录的坐标保存到 JSON 文件
    with open(f'route/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(XY, f)

    print(f"Coordinates saved to route/{file_name}.json")


def generate_route(file_name):
    min_value = 5
    max_value = 153

    interval = 0.5

    # 圆角半径
    radius = 5

    # 圆弧点数
    num_points = 50
    ##################################
    
    fig, ax = plt.subplots()

    config = load_config()
    bg_image = mpimg.imread(config.map_path)

    # 存储坐标的列表
    XY = {"X": [], "Y": []}

    # 顺时针绕地图一圈，添加圆角
    x = min_value + radius
    y = max_value
    # 从左上角开始，沿着上边界向右移动
    while x < max_value - radius:
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='red')
        x += interval
    
    # 上右圆角
    for t in np.linspace(0, np.pi / 2, num_points):
        x = max_value - radius + radius * np.sin(t) 
        y = max_value - radius + radius * np.cos(t)
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='blue')

    # 沿着右边界向下移动
    # x = max_value
    while y > min_value + radius:
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='red')
        y -= interval

    # 右下圆角
    for t in np.linspace(np.pi / 2, np.pi, num_points):
        x = max_value - radius + radius * np.sin(t) 
        y = min_value + radius + radius * np.cos(t)
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='blue')

    # 沿着下边界向左移动
    # y = min_value
    while x > min_value + radius:
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='red')
        x -= interval

    # 左下圆角
    for t in np.linspace(np.pi, 3 * np.pi / 2, num_points):
        x = min_value + radius + radius * np.sin(t) 
        y = min_value + radius + radius * np.cos(t)
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='blue')

    # # 沿着左边界向上移动
    while y < max_value - radius:
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='red')
        y += interval

    # 左上圆角
    for t in np.linspace(3 * np.pi / 2, 2 * np.pi, num_points):
        x = min_value + radius + radius * np.sin(t) 
        y = max_value - radius + radius * np.cos(t)
        XY["X"].append(x)
        XY["Y"].append(y)
        ax.scatter(x, y, color='blue')
        
    # 查看图片
    plt.imshow(bg_image, extent=[0, 160, 0, 160], aspect='auto') 
    plt.show()
    # fig.canvas.draw_idle()  # 更新图形

    # 将记录的坐标保存到 JSON 文件
    with open(f'route/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(XY, f)

    print(f"Coordinates saved to route/{file_name}.json")


if __name__ == "__main__":
    file_name = "完美外圈"
    # draw_route(file_name)

    generate_route(file_name)
