from models.vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, vehicle_id, capacity=10):
        super().__init__(vehicle_id, "Van", capacity, cost_per_km=20.0)

    def calculate_cost(self, distance):
        # Base fare ₱80 + ₱20/km
        return 80.0 + (self.cost_per_km * distance)

    def __str__(self):
        return f"Van (Capacity: {self.capacity}, Base fare: ₱80, Cost per km: ₱{self.cost_per_km})"