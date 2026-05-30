import tkinter as tk
from tkinter import messagebox
from gui.login_window import LoginWindow
from gui.driver_login import DriverLoginWindow
from gui.main_window import MainWindow
from gui.driver_dashboard import DriverDashboard

# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_DARK, pady=30)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚗 Ride Booking System 🚗",
            font=("Helvetica", 20, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Select your role",
            font=("Helvetica", 12),
            bg=BG_DARK,
            fg=TEXT_GRAY
        ).pack(pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg=BG_DARK)
        buttons_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Passenger Button
        tk.Button(
            buttons_frame,
            text="👤 Passenger\nBook a Ride",
            font=("Helvetica", 14, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            padx=20,
            pady=40,
            cursor="hand2",
            command=self.passenger_mode
        ).pack(fill="both", expand=True, pady=10)

        # Driver Button
        tk.Button(
            buttons_frame,
            text="🚕 Driver\nAccept Rides",
            font=("Helvetica", 14, "bold"),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=20,
            pady=40,
            cursor="hand2",
            command=self.driver_mode
        ).pack(fill="both", expand=True, pady=10)

    def passenger_mode(self):
        self.root.destroy()
        login = LoginWindow()
        account = login.run()
        if account:
            app = MainWindow(account)
            app.run()

    def driver_mode(self):
        self.root.destroy()
        login = DriverLoginWindow()
        driver = login.run()
        if driver:
            app = DriverDashboard(driver)
            app.run()

    def run(self):
        self.root.mainloop()
