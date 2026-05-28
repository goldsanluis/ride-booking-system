from datetime import datetime

class Booking:
    def __init__(self, booking_id, user, vehicle, start_location, end_location, distance):
        self.booking_id = booking_id
        self.user = user
        self.vehicle = vehicle
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance
        self.total_cost = vehicle.calculate_cost(distance)
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Active"

    def cancel(self):
        self.status = "Cancelled"

    def __str__(self):
        return (f"Booking ID: {self.booking_id}\n"
                f"User: {self.user}\n"
                f"Vehicle: {self.vehicle}\n"
                f"From: {self.start_location} → To: {self.end_location}\n"
                f"Distance: {self.distance} km\n"
                f"Total Cost:₱{self.total_cost:.2f}\n"
                f"Date: {self.date}\n"
                f"Status: {self.status}")