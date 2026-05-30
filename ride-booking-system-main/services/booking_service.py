from models.booking import Booking
from models.car import Car
from models.van import Van
from models.bike import Bike
from models.driver import Driver

class BookingService:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.bookings = []
        self.next_id = self.file_manager.get_next_id()
        self.load_bookings()

    def get_vehicle(self, vehicle_type):
        vehicles = {
            "Car": Car(self.next_id),
            "Van": Van(self.next_id),
            "Bike": Bike(self.next_id)
        }
        return vehicles.get(vehicle_type, None)

    def load_bookings(self):
        data = self.file_manager.load_bookings()
        for item in data:
            vehicle = self.get_vehicle(item["vehicle_type"])
            if vehicle:
                booking = Booking(
                    item["booking_id"],
                    item["user"],
                    vehicle,
                    item["start_location"],
                    item["end_location"],
                    item["distance"],
                    passengers=item.get("passengers", 1),
                    notes=item.get("notes", ""),
                    promo_code=item.get("promo_code", None),
                    discount=item.get("discount", 0.0),
                )
                booking.total_cost = item["total_cost"]
                booking.date = item["date"]
                booking.status = item["status"]
                booking.surge = item.get("surge", 1.0)
                booking.rating = item.get("rating", None)
                booking.driver = Driver(
                    item.get("driver_name", "Unknown"),
                    item.get("driver_plate", "Unknown"),
                    item.get("driver_rating", 0.0),
                    driver_id=item.get("driver_id")
                )
                self.bookings.append(booking)

    def book_ride(self, user, vehicle_type, start_location, end_location, distance,
                  passengers=1, notes="", promo_code=None, discount=0.0):
        vehicle = self.get_vehicle(vehicle_type)
        if not vehicle:
            return "Invalid vehicle type!"
        booking = Booking(
            self.next_id, user, vehicle,
            start_location, end_location, distance,
            passengers=passengers, notes=notes,
            promo_code=promo_code, discount=discount
        )
        self.bookings.append(booking)
        self.next_id += 1
        return booking

    def get_all_bookings(self):
        return self.bookings

    def get_user_bookings(self, username):
        return [b for b in self.bookings if b.user == username]

    def cancel_booking(self, booking_id, username):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only cancel your own bookings!"
                booking.cancel()
                return f"Booking #{booking_id} cancelled successfully!"
        return "Booking not found!"

    def complete_booking(self, booking_id, username):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only complete your own bookings!"
                booking.complete()
                return f"Booking #{booking_id} completed!"
        return "Booking not found!"

    def rate_booking(self, booking_id, username, rating):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                if booking.user != username:
                    return "You can only rate your own bookings!"
                if booking.status != "Completed":
                    return "You can only rate completed bookings!"
                return booking.add_rating(rating)
        return "Booking not found!"

    def get_active_bookings(self):
        return [b for b in self.bookings if b.status == "Active"]

    def find_booking_by_id(self, booking_id):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
