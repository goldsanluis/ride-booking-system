import tkinter as tk
from tkinter import messagebox

class BookingList:
    def __init__(self, parent, service):
        self.service = service

        self.frame = tk.Frame(parent, bg="#16213e", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="All Bookings",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(pady=10)

        # Scrollable list
        self.listbox = tk.Listbox(
            self.frame,
            font=("Helvetica", 10),
            bg="#0f3460",
            fg="white",
            selectbackground="#e94560",
            relief="flat",
            bd=5,
            height=20
        )
        self.listbox.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Cancel Button
        tk.Button(
            self.frame,
            text="Cancel Booking ❌",
            font=("Helvetica", 12, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.cancel_booking
        ).pack(pady=10, fill="x")

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        bookings = self.service.get_all_bookings()
        if not bookings:
            self.listbox.insert(tk.END, "No bookings yet!")
            return
        for booking in bookings:
            self.listbox.insert(tk.END, f"─────────────────────")
            self.listbox.insert(tk.END, f"ID: {booking.booking_id} | {booking.user}")
            self.listbox.insert(tk.END, f"🚗 {booking.vehicle.name}")
            self.listbox.insert(tk.END, f"📍 {booking.start_location} → {booking.end_location}")
            self.listbox.insert(tk.END, f"💰 ₱{booking.total_cost:.2f} | {booking.status}")
            self.listbox.insert(tk.END, f"📅 {booking.date}")

    def cancel_booking(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a booking to cancel!")
            return
        selected_text = self.listbox.get(selected[0])
        if "ID:" in selected_text:
            booking_id = int(selected_text.split("|")[0].replace("ID:", "").strip())
            result = self.service.cancel_booking(booking_id)
            messagebox.showinfo("Result", result)
            self.refresh()