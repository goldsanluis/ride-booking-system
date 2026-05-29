import json
import os

class DriverManager:
    def __init__(self):
        self.drivers_file = "data/drivers.json"
        self.drivers = self.load_drivers()

    def load_drivers(self):
        if os.path.exists(self.drivers_file):
            with open(self.drivers_file, 'r') as f:
                data = json.load(f)
                return data.get('drivers', [])
        return []

    def save_drivers(self):
        with open(self.drivers_file, 'w') as f:
            json.dump({'drivers': self.drivers}, f, indent=2)

    def login(self, username, password):
        for driver in self.drivers:
            if driver['username'] == username and driver['password'] == password:
                return driver, "Login successful!"
        return None, "Invalid username or password!"

    def register(self, username, password, name, phone, plate, vehicle_type):
        for driver in self.drivers:
            if driver['username'] == username:
                return None, "Username already exists!"
        
        new_driver = {
            "driver_id": f"D{len(self.drivers) + 1:03d}",
            "username": username,
            "password": password,
            "name": name,
            "phone": phone,
            "plate": plate,
            "vehicle_type": vehicle_type,
            "rating": 5.0,
            "total_rides": 0,
            "status": "offline"
        }
        
        self.drivers.append(new_driver)
        self.save_drivers()
        return new_driver, "Registration successful!"

    def update_driver_status(self, driver_id, status):
        for driver in self.drivers:
            if driver['driver_id'] == driver_id:
                driver['status'] = status
                self.save_drivers()
                return True
        return False

    def get_driver_by_id(self, driver_id):
        for driver in self.drivers:
            if driver['driver_id'] == driver_id:
                return driver
        return None