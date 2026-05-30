"""
gui/main_menu.py
----------------
First screen the user sees after launching the app.
Presents two role buttons — Passenger and Driver — and routes
the user to the appropriate login window based on their choice.
"""

import tkinter as tk
from gui.login_window      import LoginWindow
from gui.driver_login      import DriverLoginWindow
from gui.main_window       import MainWindow
from gui.driver_dashboard  import DriverDashboard

# ── Gold Theme Palette ────────────────────────────────────────────────────────
BG_DARK     = "#1a1200"   # Very dark brown background
BG_CARD     = "#2d1f00"   # Slightly lighter card background
GOLD        = "#FFD700"   # Bright gold (primary accent)
GOLD_DARK   = "#B8860B"   # Dark goldenrod (secondary accent)
GOLD_ACCENT = "#FFA500"   # Orange-gold (highlight)
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"   # Muted warm grey for subtitles


class MainMenu:
    """
    Role-selection screen shown at application startup.

    Attributes:
        root (tk.Tk): The main Tkinter window for this screen.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)  # Fixed window size

        self.setup_ui()

    def setup_ui(self):
        """Build the header label and the Passenger / Driver role buttons."""

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=BG_DARK, pady=30)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚗 Ride Booking System 🚗",
            font=("Helvetica", 20, "bold"),
            bg=BG_DARK, fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Select your role",
            font=("Helvetica", 12),
            bg=BG_DARK, fg=TEXT_GRAY
        ).pack(pady=10)

        # ── Role Buttons ──────────────────────────────────────────────────────
        buttons_frame = tk.Frame(self.root, bg=BG_DARK)
        buttons_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Passenger button → LoginWindow → MainWindow
        tk.Button(
            buttons_frame,
            text="👤 Passenger\nBook a Ride",
            font=("Helvetica", 14, "bold"),
            bg=GOLD, fg=BG_DARK,
            relief="flat", padx=20, pady=40,
            cursor="hand2",
            command=self.passenger_mode
        ).pack(fill="both", expand=True, pady=10)

        # Driver button → DriverLoginWindow → DriverDashboard
        tk.Button(
            buttons_frame,
            text="🚕 Driver\nAccept Rides",
            font=("Helvetica", 14, "bold"),
            bg=GOLD_DARK, fg=TEXT_WHITE,
            relief="flat", padx=20, pady=40,
            cursor="hand2",
            command=self.driver_mode
        ).pack(fill="both", expand=True, pady=10)

    def passenger_mode(self):
        """
        Close this menu, open the passenger login screen, and if
        authentication succeeds, launch the main passenger dashboard.
        """
        self.root.destroy()
        login   = LoginWindow()
        account = login.run()   # Blocks until login window closes
        if account:
            app = MainWindow(account)
            app.run()

    def driver_mode(self):
        """
        Close this menu, open the driver login screen, and if
        authentication succeeds, launch the driver dashboard.
        """
        self.root.destroy()
        login  = DriverLoginWindow()
        driver = login.run()    # Blocks until login window closes
        if driver:
            app = DriverDashboard(driver)
            app.run()

    def run(self):
        """Start the Tkinter event loop for this window."""
        self.root.mainloop()
