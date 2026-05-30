"""
file_handler/driver_manager.py
-------------------------------
Handles persistence for driver accounts: login, wallet updates,
and rating recalculation. Driver data is stored in data/drivers.json
as a dictionary with a single "drivers" list.
"""

import json
import os


class DriverManager:
    """
    Manages CRUD operations for driver records in drivers.json.

    Each driver record contains:
        driver_id, username, password, name, plate,
        rating, rating_count, wallet_balance.
    """

    def __init__(self, filename="data/drivers.json"):
        self.filename = filename
        self.ensure_file_exists()

    # ── File Setup ────────────────────────────────────────────────────────────

    def ensure_file_exists(self):
        """
        Create the data directory and an empty drivers file
        if they don't already exist.
        """
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"drivers": []}, f)

    # ── Raw JSON Access ───────────────────────────────────────────────────────

    def load_drivers(self):
        """
        Read all driver records from the JSON file.

        Returns:
            list[dict]: List of driver dictionaries,
                        or an empty list on read error.
        """
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return data.get("drivers", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_drivers(self, drivers):
        """
        Write the full list of driver dictionaries back to the JSON file,
        preserving the top-level {"drivers": [...]} structure.

        Args:
            drivers (list[dict]): Complete list of driver records to persist.
        """
        with open(self.filename, "w") as f:
            json.dump({"drivers": drivers}, f, indent=4)

    # ── Authentication ────────────────────────────────────────────────────────

    def get_driver(self, username, password):
        """
        Look up a driver by username and password.

        Args:
            username (str): Driver's login username.
            password (str): Driver's login password.

        Returns:
            dict | None: The matching driver dictionary, or None if not found.
        """
        drivers = self.load_drivers()
        for driver in drivers:
            if driver["username"] == username and driver["password"] == password:
                return driver
        return None

    # ── Wallet ────────────────────────────────────────────────────────────────

    def update_driver_wallet(self, driver_id, amount):
        """
        Add earnings to a driver's wallet after completing a ride.

        Args:
            driver_id (str): The driver's unique ID.
            amount    (float): Amount in ₱ to add.

        Returns:
            bool: True if the driver was found and updated, False otherwise.
        """
        drivers = self.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                # Use .get() with a default in case wallet_balance is missing
                driver["wallet_balance"] = driver.get("wallet_balance", 0.0) + amount
                self.save_drivers(drivers)
                return True
        return False

    # ── Rating ────────────────────────────────────────────────────────────────

    def update_driver_rating(self, driver_id, new_rating):
        """
        Recalculate a driver's average rating after receiving a new
        passenger star rating, using a running average formula:
            new_avg = (old_avg × old_count + new_rating) / (old_count + 1)

        Args:
            driver_id  (str): The driver's unique ID.
            new_rating (int): New rating value (1–5).

        Returns:
            bool: True if the driver was found and updated, False otherwise.
        """
        drivers = self.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                current_avg   = driver.get("rating",       5.0)
                current_count = driver.get("rating_count", 1)

                # Running average: incorporate the new rating into the existing mean
                driver["rating"]        = round(
                    (current_avg * current_count + new_rating) / (current_count + 1), 2
                )
                driver["rating_count"]  = current_count + 1
                self.save_drivers(drivers)
                return True
        return False

    # ── Stats ─────────────────────────────────────────────────────────────────

    def get_driver_stats(self, driver_id):
        """
        Retrieve the full record for a specific driver.

        Args:
            driver_id (str): The driver's unique ID.

        Returns:
            dict: The driver's data dictionary, or an empty dict if not found.
        """
        for d in self.load_drivers():
            if d["driver_id"] == driver_id:
                return d
        return {}
