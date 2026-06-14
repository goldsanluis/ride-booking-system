"""
gui/main_menu.py
----------------
First screen the user sees after launching the app.
Presents two role buttons — Passenger and Driver — and routes
the user to the appropriate login window based on their choice.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


import tkinter as tk
from gui.login_window      import LoginWindow
from gui.driver_login      import DriverLoginWindow
from gui.main_window       import MainWindow
from gui.driver_dashboard  import DriverDashboard

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_APP      = "#1a0000"   # Deep dark maroon background
BG_SURFACE  = "#800000"   # Maroon card surface
MAROON      = "#800000"   # PUP Maroon
GOLD        = "#FFD700"   # PUP Gold
TEXT_WHITE  = "#FFFFFF"   # White text
TEXT_MUTED  = "#FFFFFF"   # White subtext
DIVIDER     = "#990000"   # Divider line


class MainMenu:
    """
    Role-selection screen shown at application startup.

    Attributes:
        root (tk.Tk): The main Tkinter window for this screen.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Rides — Ride Booking System")
        self.root.geometry("600x540")
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        """Build the header and the Passenger / Driver role buttons."""

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=MAROON, padx=18, pady=18)
        header.pack(fill="x")

        top_glow = tk.Frame(header, bg=BG_APP, height=6)
        top_glow.pack(fill="x", pady=(0, 10))

        title_row = tk.Frame(header, bg=MAROON)
        title_row.pack(fill="x")

        tk.Label(title_row, text="🎓", font=("Helvetica", 34),
                 bg=MAROON, fg=GOLD).pack(side="left")

        txt_wrap = tk.Frame(title_row, bg=MAROON)
        txt_wrap.pack(side="left", fill="x", expand=True, padx=(14, 0))

        tk.Label(txt_wrap, text="PUP Rides",
                 font=("Helvetica", 24, "bold"), bg=MAROON, fg=GOLD,
                 justify="left").pack(anchor="w")

        tk.Label(txt_wrap, text="Ride Booking System",
                 font=("Helvetica", 10), bg=MAROON, fg=TEXT_MUTED,
                 justify="left").pack(anchor="w", pady=(4, 0))

        tk.Label(header, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 8), bg=MAROON, fg=GOLD).pack(anchor="w", pady=(10, 0))

        # Gold accent line
        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x")

        # ── Subtitle ──────────────────────────────────────────────────────────
        sub_frame = tk.Frame(self.root, bg=BG_APP, pady=20)
        sub_frame.pack(fill="x")

        tk.Label(sub_frame, text="Select your role to get started",
                 font=("Helvetica", 12), bg=BG_APP, fg=TEXT_MUTED).pack()

        # ── Role Buttons ──────────────────────────────────────────────────────
        buttons_frame = tk.Frame(self.root, bg=BG_APP)
        buttons_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        # Passenger button — gold fill
        pass_wrap = tk.Frame(buttons_frame, bg=GOLD, pady=2)
        pass_wrap.pack(fill="both", expand=True, pady=10)
        tk.Button(
            pass_wrap,
            text="👤  Passenger\nBook a Ride",
            font=("Helvetica", 14, "bold"),
            bg=GOLD, fg=BG_APP,
            relief="flat", padx=20, pady=30,
            cursor="hand2",
            activebackground=BG_APP,
            activeforeground=GOLD,
            command=self.passenger_mode
        ).pack(fill="both", expand=True)

        # Driver button — maroon fill with gold text
        drv_wrap = tk.Frame(buttons_frame, bg=GOLD, pady=2)
        drv_wrap.pack(fill="both", expand=True, pady=10)
        tk.Button(
            drv_wrap,
            text="🚕  Driver\nAccept Rides",
            font=("Helvetica", 14, "bold"),
            bg=BG_SURFACE, fg=GOLD,
            relief="flat", padx=20, pady=30,
            cursor="hand2",
            activebackground=GOLD,
            activeforeground=BG_APP,
            command=self.driver_mode
        ).pack(fill="both", expand=True)

    def passenger_mode(self):
        """
        Close this menu, open the passenger login screen, and if
        authentication succeeds, launch the main passenger dashboard.
        """
        self.root.destroy()
        login   = LoginWindow()
        account = login.run()
        if account:
            app = MainWindow(account)
            app.run()
        else:
            MainMenu().run()

    def driver_mode(self):
        """
        Close this menu, open the driver login screen, and if
        authentication succeeds, launch the driver dashboard.
        """
        self.root.destroy()
        login  = DriverLoginWindow()
        driver = login.run()
        if driver:
            app = DriverDashboard(driver)
            app.run()
        else:
            MainMenu().run()

    def run(self):
        """Start the Tkinter event loop for this window."""
        self.root.mainloop()