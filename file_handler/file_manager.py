import json
import os

class FileManager:
    def __init__(self, filename="data/bookings.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def save_bookings(self, bookings):
        data = []
        for booking in bookings:
            data.append({
                "booking_id": booking.booking_id,
                "user": booking.user,
                "vehicle_type": booking.vehicle.name,
                "start_location": booking.start_location,
                "end_location": booking.end_location,
                "distance": booking.distance,
                "total_cost": booking.total_cost,
                "date": booking.date,
                "status": booking.status
            })
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_bookings(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []