import json
import yaml
from box import Box


# 提取IP、端口、发送端口和车辆名称
def split_net(net: str):
    vehicle_name, ip, port, send_port = net.split(",")
    port, send_port = int(port), int(send_port)
    return ip, port, send_port, vehicle_name

# 加载路径
def load_route() -> list:
    path = load_config().route_path
    with open(path, 'r', encoding='utf-8') as f:
        route = json.load(f)
        X = route['X']
        Y = route['Y']


    route = list(zip(X, Y))
    return route

# 加载配置文件
def load_config():
    with open("config.yaml", 'r', encoding='utf-8') as f:
        config = Box(yaml.safe_load(f))
    return config
