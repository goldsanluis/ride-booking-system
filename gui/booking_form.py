import tkinter as tk
from tkinter import messagebox

class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account):
        self.service = service
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback
        self.account = account

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
        ).pack(pady=15, fill="x")

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

        user = self.account.name
        booking = self.service.book_ride(user, vehicle_type, start, end, distance)
        self.file_manager.save_bookings(self.service.get_all_bookings())

        surge_text = f"\n🚀 Surge pricing applied! ({booking.surge}x)" if booking.surge > 1.0 else ""
        messagebox.showinfo("Booking Confirmed! 🎉",
                          f"Ride booked successfully!\n"
                          f"Driver: {booking.driver.name}\n"
                          f"Plate: {booking.driver.plate}\n"
                          f"Total Cost: ₱{booking.total_cost:.2f}{surge_text}")

        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.refresh_callback()