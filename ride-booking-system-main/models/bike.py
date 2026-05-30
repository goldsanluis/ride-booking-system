from models.vehicle import Vehicle

class Bike(Vehicle):
    def __init__(self, vehicle_id, capacity=1):
        super().__init__(vehicle_id, "Bike", capacity, cost_per_km=8.0)

    def calculate_cost(self, distance):
        # Base fare ₱20 + ₱8/km
        return 20.0 + (self.cost_per_km * distance)

    def __str__(self):
        return f"Bike (Capacity: {self.capacity}, Base fare: ₱20, Cost per km: ₱{self.cost_per_km})"