import tkinter as tk
from tkinter import messagebox
from models.car import Car
from models.van import Van
from models.bike import Bike

class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account, account_manager):
        self.service = service
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback
        self.account = account
        self.account_manager = account_manager

        self.frame = tk.Frame(parent, bg="#2d1f00", padx=15, pady=15)

        # Title
        tk.Label(
            self.frame,
            text="📍 Book a Ride",
            font=("Helvetica", 14, "bold"),
            bg="#2d1f00",
            fg="#FFD700"
        ).pack(pady=10)

        # Start location
        tk.Label(self.frame, text="From:", bg="#2d1f00", fg="white").pack(anchor="w")
        self.start_location = tk.Entry(self.frame, width=30, bg="#3d2a00", fg="white")
        self.start_location.pack(fill="x", pady=5)

        # End location
        tk.Label(self.frame, text="To:", bg="#2d1f00", fg="white").pack(anchor="w")
        self.end_location = tk.Entry(self.frame, width=30, bg="#3d2a00", fg="white")
        self.end_location.pack(fill="x", pady=5)

        # Distance
        tk.Label(self.frame, text="Distance (km):", bg="#2d1f00", fg="white").pack(anchor="w")
        self.distance = tk.Entry(self.frame, width=30, bg="#3d2a00", fg="white")
        self.distance.pack(fill="x", pady=5)

        # Vehicle type
        tk.Label(self.frame, text="Vehicle Type:", bg="#2d1f00", fg="white").pack(anchor="w")
        self.vehicle_var = tk.StringVar(value="Car")
        vehicles = ["Bike", "Car", "Van"]
        for vehicle in vehicles:
            tk.Radiobutton(
                self.frame,
                text=vehicle,
                variable=self.vehicle_var,
                value=vehicle,
                bg="#2d1f00",
                fg="white",
                selectcolor="#FFD700",
                command=self.update_cost
            ).pack(anchor="w")

        # Cost display
        self.cost_label = tk.Label(
            self.frame,
            text="Estimated Cost: ₱0.00",
            font=("Helvetica", 11, "bold"),
            bg="#2d1f00",
            fg="#FFA500"
        )
        self.cost_label.pack(pady=10)

        # Book button
        tk.Button(
            self.frame,
            text="✅ Book Ride",
            font=("Helvetica", 12, "bold"),
            bg="#4ecca3",
            fg="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.book_ride
        ).pack(fill="x", pady=10)

    def update_cost(self):
        try:
            distance = float(self.distance.get()) if self.distance.get() else 0
            vehicle_type = self.vehicle_var.get()
            
            # Get vehicle costs
            vehicles = {
                "Bike": (20, 8),      # base, per_km
                "Car": (40, 14),
                "Van": (80, 20)
            }
            
            base, per_km = vehicles[vehicle_type]
            cost = base + (per_km * distance)
            
            # Check surge pricing (peak hours)
            from datetime import datetime
            hour = datetime.now().hour
            if (7 <= hour <= 9) or (17 <= hour <= 20):
                cost *= 1.5
                self.cost_label.config(text=f"Estimated Cost: ₱{cost:.2f} (1.5x surge)")
            else:
                self.cost_label.config(text=f"Estimated Cost: ₱{cost:.2f}")
        except:
            self.cost_label.config(text="Estimated Cost: ₱0.00")

    def book_ride(self):
        # Validate inputs
        if not self.start_location.get() or not self.end_location.get() or not self.distance.get():
            messagebox.showerror("Error", "Please fill all fields!")
            return

        try:
            distance = float(self.distance.get())
            if distance <= 0:
                messagebox.showerror("Error", "Distance must be greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number!")
            return

        # Calculate cost
        vehicle_type = self.vehicle_var.get()
        vehicles = {
            "Bike": (20, 8),
            "Car": (40, 14),
            "Van": (80, 20)
        }
        base, per_km = vehicles[vehicle_type]
        cost = base + (per_km * distance)

        # Check surge
        from datetime import datetime
        hour = datetime.now().hour
        if (7 <= hour <= 9) or (17 <= hour <= 20):
            cost *= 1.5

        # CHECK WALLET BALANCE
        if self.account.wallet_balance < cost:
            messagebox.showerror(
                "Insufficient Balance",
                f"Your balance: ₱{self.account.wallet_balance:.2f}\nCost: ₱{cost:.2f}\n\nPlease add money to your wallet!"
            )
            return

        # Book the ride
        booking = self.service.book_ride(
            self.account.username,
            vehicle_type,
            self.start_location.get(),
            self.end_location.get(),
            distance
        )

        if booking:
            # DEDUCT FROM WALLET
            self.account.wallet_balance -= cost
            accounts = self.account_manager.load_accounts()
            for acc in accounts:
                if acc["username"] == self.account.username:
                    acc["wallet_balance"] = self.account.wallet_balance
                    break
            self.account_manager.save_accounts(accounts)

            # Save booking and refresh
            self.file_manager.save_bookings(self.service.get_all_bookings())
            
            messagebox.showinfo(
                "Success",
                f"Ride booked! 🎉\n\nCost: ₱{cost:.2f}\nRemaining balance: ₱{self.account.wallet_balance:.2f}"
            )

            # Clear form
            self.start_location.delete(0, tk.END)
            self.end_location.delete(0, tk.END)
            self.distance.delete(0, tk.END)
            
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to book ride!")
