import tkinter as tk
from tkinter import messagebox

class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account):
        self.account = account
        self.service = service
        self.file_manager = file_manager
        self.refresh_callback = refresh_callback

        self.frame = tk.Frame(parent, bg="#16213e", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="Book a Ride",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(pady=10)

        # User
        self.create_label("Your Name:")
        self.user_entry = self.create_entry()

        # Vehicle Type
        self.create_label("Vehicle Type:")
        self.vehicle_var = tk.StringVar(value="Car")
        for vehicle in ["Car", "Van", "Bike"]:
            tk.Radiobutton(
                self.frame,
                text=vehicle,
                variable=self.vehicle_var,
                value=vehicle,
                bg="#16213e",
                fg="white",
                selectcolor="#e94560",
                font=("Helvetica", 11)
            ).pack(anchor="w")

        # Start Location
        self.create_label("Start Location:")
        self.start_entry = self.create_entry()

        # End Location
        self.create_label("End Location:")
        self.end_entry = self.create_entry()

        # Distance
        self.create_label("Distance (km):")
        self.distance_entry = self.create_entry()

        # Book Button
        tk.Button(
            self.frame,
            text="Book Ride 🚗",
            font=("Helvetica", 12, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.book_ride
        ).pack(pady=15, fill="x")

    def create_label(self, text):
        tk.Label(
            self.frame,
            text=text,
            font=("Helvetica", 11),
            bg="#16213e",
            fg="white"
        ).pack(anchor="w", pady=2)

    def create_entry(self):
        entry = tk.Entry(
            self.frame,
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=5
        )
        entry.pack(fill="x", pady=2)
        return entry

    def book_ride(self):
        user = self.account.name
        vehicle_type = self.vehicle_var.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        try:
            distance = float(self.distance_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid distance!")
            return

        if not all([user, start, end]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        booking = self.service.book_ride(user, vehicle_type, start, end, distance)
        self.file_manager.save_bookings(self.service.get_all_bookings())
        messagebox.showinfo("Success", f"Ride booked!\nTotal Cost:₱{booking.total_cost:.2f}")

        self.user_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)

        self.refresh_callback()