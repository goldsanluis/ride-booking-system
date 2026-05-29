from datetime import datetime
from models.driver import Driver

class Booking:
    def __init__(self, booking_id, user, vehicle, start_location, end_location, distance):
        self.booking_id = booking_id
        self.user = user
        self.vehicle = vehicle
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Active"
        self.driver = Driver.get_random_driver()
        self.rating = None
        self.surge = self.check_surge()
        self.total_cost = self.calculate_total_cost()

    def check_surge(self):
        hour = datetime.now().hour
        # Peak hours: 7-9AM and 5-8PM
        if (7 <= hour <= 9) or (17 <= hour <= 20):
            return 1.5
        return 1.0

    def calculate_total_cost(self):
        base_cost = self.vehicle.calculate_cost(self.distance)
        return base_cost * self.surge

    def cancel(self):
        self.status = "Cancelled"

    def complete(self):
        self.status = "Completed"

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.rating = rating
            return f"Rating of {rating}⭐ added successfully!"
        return "Rating must be between 1 and 5!"

    def __str__(self):
        surge_text = f" (Surge: {self.surge}x)" if self.surge > 1.0 else ""
        rating_text = f"⭐{self.rating}" if self.rating else "Not rated"
        return (f"Booking ID: {self.booking_id}\n"
                f"User: {self.user}\n"
                f"Vehicle: {self.vehicle}\n"
                f"Driver: {self.driver}\n"
                f"From: {self.start_location} → To: {self.end_location}\n"
                f"Distance: {self.distance} km\n"
                f"Total Cost: ₱{self.total_cost:.2f}{surge_text}\n"
                f"Date: {self.date}\n"
                f"Status: {self.status}\n"
                f"Rating: {rating_text}")