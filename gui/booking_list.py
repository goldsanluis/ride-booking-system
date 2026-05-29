import tkinter as tk
from tkinter import messagebox
from file_handler.driver_manager import DriverManager

# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"

class BookingList:
    def __init__(self, parent, service, account):
        self.service = service
        self.account = account
        self.driver_manager = DriverManager()

        self.frame = tk.Frame(parent, bg=BG_DARK)

        # Title
        tk.Label(
            self.frame,
            text="📋 My Bookings",
            font=("Helvetica", 14, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack(pady=10)

        # Canvas for scrolling
        self.canvas = tk.Canvas(self.frame, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.refresh()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def refresh(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        bookings = self.service.get_user_bookings(self.account.username)

        if not bookings:
            tk.Label(
                self.inner_frame,
                text="No bookings yet 😴",
                font=("Helvetica", 11),
                bg=BG_DARK,
                fg=TEXT_GRAY
            ).pack(pady=20)
            return

        for booking in bookings:
            self.create_booking_card(booking)

    def create_booking_card(self, booking):
        card_frame = tk.Frame(self.inner_frame, bg=BG_CARD, padx=10, pady=10)
        card_frame.pack(fill="x", padx=5, pady=5)

        # Booking ID and Status
        header_frame = tk.Frame(card_frame, bg=BG_CARD)
        header_frame.pack(fill="x", pady=5)

        status_color = {
            "Active": "#FFA500",
            "Completed": "#4ecca3",
            "Cancelled": "#FF6B6B"
        }.get(booking.status, GOLD_ACCENT)

        tk.Label(
            header_frame,
            text=f"Booking #{booking.booking_id}",
            font=("Helvetica", 11, "bold"),
            bg=BG_CARD,
            fg=GOLD
        ).pack(side="left")

        tk.Label(
            header_frame,
            text=f"Status: {booking.status}",
            font=("Helvetica", 10, "bold"),
            bg=BG_CARD,
            fg=status_color
        ).pack(side="right")

        # Driver info
        tk.Label(
            card_frame,
            text=f"🚗 Driver: {booking.driver.name}",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w", pady=2)

        tk.Label(
            card_frame,
            text=f"📍 Route: {booking.start_location} → {booking.end_location}",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=TEXT_WHITE
        ).pack(anchor="w", pady=2)

        # Details
        details = f"📏 {booking.distance} km  |  💰 ₱{booking.total_cost:.2f}  |  🚗 {booking.vehicle.name}"
        tk.Label(
            card_frame,
            text=details,
            font=("Helvetica", 9),
            bg=BG_CARD,
            fg=TEXT_GRAY
        ).pack(anchor="w", pady=2)

        # Date
        tk.Label(
            card_frame,
            text=f"📅 {booking.date}",
            font=("Helvetica", 9),
            bg=BG_CARD,
            fg=TEXT_GRAY
        ).pack(anchor="w", pady=2)

        # Buttons
        button_frame = tk.Frame(card_frame, bg=BG_CARD)
        button_frame.pack(fill="x", pady=8)

        if booking.status == "Active":
            tk.Button(
                button_frame,
                text="✅ Complete",
                font=("Helvetica", 9, "bold"),
                bg="#4ecca3",
                fg="white",
                relief="flat",
                padx=8,
                pady=5,
                cursor="hand2",
                command=lambda: self.complete_booking(booking)
            ).pack(side="left", padx=2)

            tk.Button(
                button_frame,
                text="❌ Cancel",
                font=("Helvetica", 9, "bold"),
                bg="#FF6B6B",
                fg="white",
                relief="flat",
                padx=8,
                pady=5,
                cursor="hand2",
                command=lambda: self.cancel_booking(booking)
            ).pack(side="left", padx=2)

        elif booking.status == "Completed" and not booking.rating:
            tk.Button(
                button_frame,
                text="⭐ Rate Ride",
                font=("Helvetica", 9, "bold"),
                bg=GOLD,
                fg="black",
                relief="flat",
                padx=8,
                pady=5,
                cursor="hand2",
                command=lambda: self.rate_booking(booking)
            ).pack(side="left", padx=2)

        if booking.rating:
            tk.Label(
                button_frame,
                text=f"Your rating: {'⭐' * booking.rating}",
                font=("Helvetica", 9),
                bg=BG_CARD,
                fg=GOLD_ACCENT
            ).pack(side="left", padx=10)

    def cancel_booking(self, booking):
        confirm = messagebox.askyesno(
            "Cancel Booking",
            f"Cancel booking #{booking.booking_id}?"
        )
        if confirm:
            message = self.service.cancel_booking(booking.booking_id, self.account.username)
            messagebox.showinfo("Success", message)
            self.refresh()

    def complete_booking(self, booking):
        confirm = messagebox.askyesno(
            "Complete Booking",
            f"Mark booking #{booking.booking_id} as completed?"
        )
        if confirm:
            # Complete the booking
            message = self.service.complete_booking(booking.booking_id, self.account.username)
            
            # ADD EARNINGS TO DRIVER WALLET
            if booking.driver.driver_id and booking.driver.driver_id != "unassigned":
                self.driver_manager.update_driver_wallet(
                    booking.driver.driver_id,
                    booking.total_cost
                )
            
            # Save changes
            from file_handler.file_manager import FileManager
            file_manager = FileManager()
            file_manager.save_bookings(self.service.get_all_bookings())
            
            messagebox.showinfo("Success", message)
            self.refresh()

    def rate_booking(self, booking):
        from tkinter import simpledialog
        rating = simpledialog.askinteger(
            "Rate Ride",
            "Rate your ride (1-5 stars):",
            minvalue=1,
            maxvalue=5
        )
        if rating:
            message = self.service.rate_booking(booking.booking_id, self.account.username, rating)
            from file_handler.file_manager import FileManager
            file_manager = FileManager()
            file_manager.save_bookings(self.service.get_all_bookings())
            messagebox.showinfo("Success", message)
            self.refresh()
