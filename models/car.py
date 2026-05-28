from models.vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, vehicle_id, capacity=4):
        super().__init__(vehicle_id, "Car", capacity, cost_per_km=14.0)

    def calculate_cost(self, distance):
        # Base fare ₱40 + ₱14/km
        return 40.0 + (self.cost_per_km * distance)

    def __str__(self):
        return f"Car (Capacity: {self.capacity}, Base fare: ₱40, Cost per km: ₱{self.cost_per_km})"