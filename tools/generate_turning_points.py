import os
import sys
from matplotlib import patches
import matplotlib.image as mpimg
sys.path.append(os.getcwd())
from lib import util
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体或其他支持中文的字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题


fig, ax = plt.subplots()
config = util.load_config()
map_img = mpimg.imread(config.map_path)

plt.imshow(map_img, extent=[0, 160, 0, 160], aspect='auto')
turning_points = []

ax.plot([], [], color='blue', label="转弯距离")
ax.scatter([], [], color='red', label="转弯点")
ax.legend()


def on_click(event):
    if event.button == 1:  # 左键
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            turning_points.append((x, y))
            ax.scatter(x, y, color='red')
            ax.add_patch(patches.Circle((x, y), radius=config.braking_distance, color='blue', fill=False))
            fig.canvas.draw_idle()  # 更新图形

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()

for point in turning_points:
    print(f"  - x: {point[0]}")
    print(f"    y: {point[1]}")
    print()
