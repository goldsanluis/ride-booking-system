import tkinter as tk
from tkinter import messagebox
from services.booking_service import BookingService
from file_handler.file_manager import FileManager
from file_handler.driver_manager import DriverManager
from models.driver import Driver

# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"
GREEN       = "#4ecca3"

class DriverDashboard:
    def __init__(self, driver):
        self.driver = driver
        self.root = tk.Tk()
        self.root.title("Ride Booking System - Driver Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_DARK)

        self.file_manager = FileManager()
        self.driver_manager = DriverManager()
        self.service = BookingService(self.file_manager)

        self.header_frame = None
        self.setup_header()
        self.setup_content()

    def setup_header(self):
        if self.header_frame:
            self.header_frame.destroy()

        self.header_frame = tk.Frame(self.root, bg=BG_CARD, pady=15)
        self.header_frame.pack(fill="x")

        info_frame = tk.Frame(self.header_frame, bg=BG_CARD)
        info_frame.pack(fill="x", padx=20)

        tk.Label(
            info_frame,
            text=f"🚕 {self.driver['name']}",
            font=("Helvetica", 16, "bold"),
            bg=BG_CARD,
            fg=GOLD
        ).pack(side="left")

        tk.Label(
            info_frame,
            text=f"Plate: {self.driver['plate']}",
            font=("Helvetica", 11),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(side="left", padx=20)

        tk.Label(
            info_frame,
            text=f"⭐ {self.driver['rating']}",
            font=("Helvetica", 11),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(side="left")

        earnings = self.driver.get("wallet_balance", 0.0)
        self.earnings_label = tk.Label(
            info_frame,
            text=f"💰 Earnings: ₱{earnings:.2f}",
            font=("Helvetica", 11, "bold"),
            bg=BG_CARD,
            fg=GREEN
        )
        self.earnings_label.pack(side="left", padx=20)

        tk.Button(
            info_frame,
            text="🔄 Refresh",
            font=("Helvetica", 10, "bold"),
            bg=GOLD_ACCENT,
            fg=BG_DARK,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.refresh_all
        ).pack(side="right", padx=5)

        tk.Button(
            info_frame,
            text="Logout 🚪",
            font=("Helvetica", 10, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.logout
        ).pack(side="right")

    def setup_content(self):
        self.content_frame = tk.Frame(self.root, bg=BG_DARK)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            self.content_frame,
            text="Available Ride Requests 📍",
            font=("Helvetica", 14, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack(pady=10)

        self.canvas = tk.Canvas(self.content_frame, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.refresh_requests()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def refresh_all(self):
        # Reload bookings from file
        self.service = BookingService(self.file_manager)
        # Reload driver wallet from file
        drivers = self.driver_manager.load_drivers()
        for d in drivers:
            if d["driver_id"] == self.driver["driver_id"]:
                self.driver["wallet_balance"] = d.get("wallet_balance", 0.0)
                break
        # Update earnings label
        self.earnings_label.config(
            text=f"💰 Earnings: ₱{self.driver['wallet_balance']:.2f}"
        )
        self.refresh_requests()

    def refresh_requests(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        bookings = self.service.get_all_bookings()
        active_bookings = [
            b for b in bookings
            if b.status == "Active" and b.driver.driver_id != self.driver['driver_id']
        ]

        if not active_bookings:
            tk.Label(
                self.inner_frame,
                text="No ride requests available right now 😴",
                font=("Helvetica", 12),
                bg=BG_DARK,
                fg=TEXT_GRAY
            ).pack(pady=20)
            return

        for booking in active_bookings:
            self.create_request_card(booking)

    def create_request_card(self, booking):
        card_frame = tk.Frame(
            self.inner_frame,
            bg=BG_CARD,
            padx=15,
            pady=15
        )
        card_frame.pack(fill="x", padx=10, pady=8)

        tk.Label(
            card_frame,
            text=f"👤 {booking.user}",
            font=("Helvetica", 12, "bold"),
            bg=BG_CARD,
            fg=GOLD
        ).pack(anchor="w")

        tk.Label(
            card_frame,
            text=f"📍 {booking.start_location} → {booking.end_location}",
            font=("Helvetica", 11),
            bg=BG_CARD,
            fg=TEXT_WHITE
        ).pack(anchor="w", pady=5)

        details_text = f"📏 {booking.distance} km  |  💰 ₱{booking.total_cost:.2f}  |  🚗 {booking.vehicle.name}"
        tk.Label(
            card_frame,
            text=details_text,
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        surge_text = f"🚀 Surge: {booking.surge}x" if booking.surge > 1.0 else ""
        if surge_text:
            tk.Label(
                card_frame,
                text=surge_text,
                font=("Helvetica", 10, "bold"),
                bg=BG_CARD,
                fg=GREEN
            ).pack(anchor="w")

        tk.Button(
            card_frame,
            text="✅ Accept Ride",
            font=("Helvetica", 11, "bold"),
            bg=GREEN,
            fg=TEXT_WHITE,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=lambda b=booking: self.accept_ride(b)
        ).pack(pady=10)

    def accept_ride(self, booking):
        confirm = messagebox.askyesno(
            "Accept Ride?",
            f"Accept ride from {booking.user}?\n"
            f"{booking.start_location} → {booking.end_location}\n"
            f"You will earn: ₱{booking.total_cost:.2f}"
        )

        if confirm:
            # Assign driver to booking
            booking.driver = Driver(
                self.driver['name'],
                self.driver['plate'],
                self.driver['rating'],
                driver_id=self.driver['driver_id']
            )

            # Save booking
            self.file_manager.save_bookings(self.service.get_all_bookings())

            # Add earnings to driver wallet
            self.driver_manager.update_driver_wallet(
                self.driver['driver_id'],
                booking.total_cost
            )

            # Update driver dict wallet balance
            self.driver['wallet_balance'] = self.driver.get('wallet_balance', 0.0) + booking.total_cost

            # Update earnings label
            self.earnings_label.config(
                text=f"💰 Earnings: ₱{self.driver['wallet_balance']:.2f}"
            )

            messagebox.showinfo(
                "Ride Accepted! 🎉",
                f"You accepted ride from {booking.user}!\n"
                f"Route: {booking.start_location} → {booking.end_location}\n"
                f"You earned: ₱{booking.total_cost:.2f}\n"
                f"Total Earnings: ₱{self.driver['wallet_balance']:.2f}"
            )

            self.refresh_requests()

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            from gui.main_menu import MainMenu
            menu = MainMenu()
            menu.run()

    def run(self):
        self.root.mainloop()