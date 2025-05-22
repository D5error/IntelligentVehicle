from PIL import Image

# 打开原始大图
img = Image.open("map.png")

# 设置目标大小（根据你的显示区域调整）
target_size = (500, 500)  # 修改为你需要的分辨率

# 缩放图像
img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

# 保存为新文件
img_resized.save("map_small.png")