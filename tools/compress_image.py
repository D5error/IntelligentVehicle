import os
import sys
sys.path.append(os.getcwd())
from PIL import Image


def compress(map_name, target_size):
    # 打开原始大图
    img = Image.open(f"map/{map_name}")

    # 缩放图像
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

    # 保存为新文件
    img_resized.save(f"map/map_{target_size[0]}_{target_size[1]}.png")

    print(f"保存为 map/map_{target_size[0]}_{target_size[1]}.png")


if __name__ == "__main__":
    map_name = "map.png"
    target_size = (250, 250)  # 修改为你需要的分辨率
    compress(map_name, target_size)

