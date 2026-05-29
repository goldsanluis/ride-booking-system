import json
import os

class DriverManager:
    def __init__(self, filename="data/drivers.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"drivers": []}, f)

    def load_drivers(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return data.get("drivers", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_drivers(self, drivers):
        with open(self.filename, "w") as f:
            json.dump({"drivers": drivers}, f, indent=4)

    def get_driver(self, username, password):
        drivers = self.load_drivers()
        for driver in drivers:
            if driver["username"] == username and driver["password"] == password:
                return driver
        return None

    def update_driver_wallet(self, driver_id, amount):
        drivers = self.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                driver["wallet_balance"] = driver.get("wallet_balance", 0.0) + amount
                self.save_drivers(drivers)
                return True
        return False
