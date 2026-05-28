class Vehicle:
    def __init__(self, vehicle_id, name, capacity, cost_per_km):
        self.vehicle_id = vehicle_id
        self.name = name
        self.capacity = capacity
        self.cost_per_km = cost_per_km

    def calculate_cost(self, distance):
        return self.cost_per_km * distance

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity}, Cost per km: ₱{self.cost_per_km})"