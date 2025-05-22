import matplotlib.pyplot as plt
import json
import os
import sys
import matplotlib.image as mpimg
sys.path.append(os.getcwd())
from lib.util import load_config


file_name = ""

fig, ax = plt.subplots()

# 加载背景图片（路径根据你的实际情况修改）
config = load_config("config.yaml")
bg_image = mpimg.imread(config['map_path'])

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