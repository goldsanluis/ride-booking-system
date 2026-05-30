from datetime import datetime
from models.driver import Driver

class Booking:
    def __init__(self, booking_id, user, vehicle, start_location, end_location, distance,
                 passengers=1, notes="", promo_code=None, discount=0.0,
                 scheduled_time=None):
        self.booking_id = booking_id
        self.user = user
        self.vehicle = vehicle
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance
        self.passengers = passengers
        self.notes = notes
        self.promo_code = promo_code
        self.discount = discount
        self.scheduled_time = scheduled_time  # NEW: future scheduled datetime string
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Scheduled" if scheduled_time else "Active"
        self.driver = Driver("Unassigned", "Unassigned", 0.0, driver_id="unassigned")
        self.rating = None
        self.surge = self.check_surge()
        self.total_cost = self.calculate_total_cost()

    def check_surge(self):
        hour = datetime.now().hour
        if (7 <= hour <= 9) or (17 <= hour <= 20):
            return 1.5
        return 1.0

    def calculate_total_cost(self):
        base_cost = self.vehicle.calculate_cost(self.distance)
        return max(0.0, (base_cost * self.surge) - self.discount)

    def cancel(self):
        self.status = "Cancelled"

    def complete(self):
        self.status = "Completed"

    def activate(self):
        """Change Scheduled → Active"""
        self.status = "Active"

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.rating = rating
            return f"Rating of {rating}⭐ added successfully!"
        return "Rating must be between 1 and 5!"

    def __str__(self):
        surge_text = f" (Surge: {self.surge}x)" if self.surge > 1.0 else ""
        rating_text = f"⭐{self.rating}" if self.rating else "Not rated"
        promo_text = f"\nPromo: {self.promo_code} (-₱{self.discount:.2f})" if self.promo_code else ""
        passengers_text = f"\nPassengers: {self.passengers}" if self.passengers > 1 else ""
        notes_text = f"\nNotes: {self.notes}" if self.notes else ""
        sched_text = f"\nScheduled: {self.scheduled_time}" if self.scheduled_time else ""
        return (f"Booking ID: {self.booking_id}\n"
                f"User: {self.user}\n"
                f"Vehicle: {self.vehicle}\n"
                f"Driver: {self.driver}\n"
                f"From: {self.start_location} → To: {self.end_location}\n"
                f"Distance: {self.distance} km\n"
                f"Total Cost: ₱{self.total_cost:.2f}{surge_text}{promo_text}\n"
                f"Date: {self.date}\n"
                f"Status: {self.status}\n"
                f"Rating: {rating_text}{passengers_text}{notes_text}{sched_text}")
