class VehicleData:
    def __init__(self):
        self.name = ""
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.speed = 0

    def __repr__(self):
        return ("VehicleData(name = {}, x = {:.2f}, y = {:.2f}, yaw = {:.2f}, speed = {:.2f})"
            .format(self.name, self.x, self.y, self.yaw, self.speed))
    
    # 用于冲突检测，设置一个假的车辆在指定的位置上
    def set_vehicle_stake(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.speed = 0
        self.yaw = 0

class AllVehicleData:
    def __init__(self):
        self.all_vehicle_data = dict()
    
    def update_vehicle_data(self, vehicle_data: VehicleData) -> None:
        if vehicle_data.name not in self.all_vehicle_data:
            self.all_vehicle_data[vehicle_data.name] = vehicle_data
        else:
            self.all_vehicle_data[vehicle_data.name].x = vehicle_data.x
            self.all_vehicle_data[vehicle_data.name].y = vehicle_data.y
            self.all_vehicle_data[vehicle_data.name].yaw = vehicle_data.yaw
            self.all_vehicle_data[vehicle_data.name].speed = vehicle_data.speed

    def get_data(self) -> dict[str, VehicleData]:
        return self.all_vehicle_data
