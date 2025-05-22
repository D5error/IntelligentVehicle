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


class AllVehicleData:
    def __init__(self):
        self.vehicle_data = dict()
    
    def update_vehicle_data(self, vehicle_data: VehicleData):
        if vehicle_data.name not in self.vehicle_data:
            self.vehicle_data[vehicle_data.name] = vehicle_data
        else:
            self.vehicle_data[vehicle_data.name].x = vehicle_data.x
            self.vehicle_data[vehicle_data.name].y = vehicle_data.y
            self.vehicle_data[vehicle_data.name].yaw = vehicle_data.yaw
            self.vehicle_data[vehicle_data.name].speed = vehicle_data.speed

    def get_all_vehicle_data(self):
        return self.vehicle_data
