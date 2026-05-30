import tkinter as tk
from tkinter import messagebox

class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account, account_manager):
        self.service = service
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback
        self.account = account
        self.account_manager = account_manager

        self.frame = tk.Frame(parent, bg="#2d1f00", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="Book a Ride",
            font=("Helvetica", 16, "bold"),
            bg="#2d1f00",
            fg="#FFD700"
        ).pack(pady=10)

        # Vehicle Type
        self.create_label("Vehicle Type:")
        self.vehicle_var = tk.StringVar(value="Car")
        vehicle_frame = tk.Frame(self.frame, bg="#2d1f00")
        vehicle_frame.pack(fill="x", pady=2)
        for vehicle in ["Car", "Van", "Bike"]:
            tk.Radiobutton(
                vehicle_frame,
                text=vehicle,
                variable=self.vehicle_var,
                value=vehicle,
                bg="#2d1f00",
                fg="white",
                selectcolor="#B8860B",
                activebackground="#2d1f00",
                activeforeground="#FFD700",
                font=("Helvetica", 11)
            ).pack(side="left", padx=5)

        # Start Location
        self.create_label("Start Location:")
        self.start_entry = self.create_entry()

        # End Location
        self.create_label("End Location:")
        self.end_entry = self.create_entry()

        # Distance
        self.create_label("Distance (km):")
        self.distance_entry = self.create_entry()

        # Pricing info
        pricing_frame = tk.Frame(self.frame, bg="#3d2a00", padx=8, pady=8)
        pricing_frame.pack(fill="x", pady=10)

        tk.Label(
            pricing_frame,
            text="💰 Pricing Info",
            font=("Helvetica", 10, "bold"),
            bg="#3d2a00",
            fg="#FFD700"
        ).pack(anchor="w")

        for text in ["🚗 Car: ₱40 base + ₱14/km",
                     "🚐 Van: ₱80 base + ₱20/km",
                     "🏍️ Bike: ₱20 base + ₱8/km",
                     "🚀 Surge: 1.5x (7-9AM, 5-8PM)"]:
            tk.Label(
                pricing_frame,
                text=text,
                font=("Helvetica", 9),
                bg="#3d2a00",
                fg="#FFA500"
            ).pack(anchor="w")

        # Wallet balance display
        self.wallet_label = tk.Label(
            self.frame,
            text=f"💳 Wallet Balance: ₱{self.account.wallet_balance:.2f}",
            font=("Helvetica", 11, "bold"),
            bg="#2d1f00",
            fg="#4ecca3"
        )
        self.wallet_label.pack(pady=5)

        # Book Button
        tk.Button(
            self.frame,
            text="Book Ride 🚗",
            font=("Helvetica", 12, "bold"),
            bg="#FFD700",
            fg="#1a1200",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.book_ride
        ).pack(pady=10, fill="x")

    def create_label(self, text):
        tk.Label(
            self.frame,
            text=text,
            font=("Helvetica", 11),
            bg="#2d1f00",
            fg="#FFA500"
        ).pack(anchor="w", pady=2)

    def create_entry(self):
        entry = tk.Entry(
            self.frame,
            font=("Helvetica", 11),
            bg="#3d2a00",
            fg="white",
            insertbackground="#FFD700",
            relief="flat",
            bd=5
        )
        entry.pack(fill="x", pady=2)
        return entry

    def book_ride(self):
        vehicle_type = self.vehicle_var.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        try:
            distance = float(self.distance_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid distance!")
            return

        if not all([start, end]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Calculate cost first to check wallet balance
        from models.car import Car
        from models.van import Van
        from models.bike import Bike
        from models.booking import Booking

        temp_vehicles = {
            "Car": Car(0),
            "Van": Van(0),
            "Bike": Bike(0)
        }
        temp_vehicle = temp_vehicles[vehicle_type]
        from datetime import datetime
        hour = datetime.now().hour
        surge = 1.5 if (7 <= hour <= 9) or (17 <= hour <= 20) else 1.0
        estimated_cost = temp_vehicle.calculate_cost(distance) * surge

        # Check wallet balance
        if self.account.wallet_balance < estimated_cost:
            messagebox.showerror(
                "Insufficient Balance!",
                f"Your wallet balance is ₱{self.account.wallet_balance:.2f}\n"
                f"Estimated cost is ₱{estimated_cost:.2f}\n"
                f"Please top up your wallet first!"
            )
            return

        # Confirm booking
        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Vehicle: {vehicle_type}\n"
            f"From: {start} → To: {end}\n"
            f"Distance: {distance} km\n"
            f"Estimated Cost: ₱{estimated_cost:.2f}\n"
            f"{'🚀 Surge pricing applied!' if surge > 1.0 else ''}\n\n"
            f"Confirm booking?"
        )

        if not confirm:
            return

        # Deduct wallet
        self.account.wallet_balance -= estimated_cost
        self.account_manager.update_account(self.account)

        # Book the ride
        user = self.account.name
        booking = self.service.book_ride(user, vehicle_type, start, end, distance)
        self.file_manager.save_bookings(self.service.get_all_bookings())

        # Update wallet display
        self.wallet_label.config(
            text=f"💳 Wallet Balance: ₱{self.account.wallet_balance:.2f}"
        )

        surge_text = f"\n🚀 Surge pricing applied! ({booking.surge}x)" if booking.surge > 1.0 else ""
        messagebox.showinfo(
            "Booking Confirmed! 🎉",
            f"Ride booked successfully!\n"
            f"Driver: {booking.driver.name}\n"
            f"Plate: {booking.driver.plate}\n"
            f"Total Cost: ₱{booking.total_cost:.2f}{surge_text}\n"
            f"Remaining Balance: ₱{self.account.wallet_balance:.2f}"
        )

        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.refresh_callback()