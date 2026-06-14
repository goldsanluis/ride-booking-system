"""
gui/main_menu.py
----------------
First screen the user sees after launching the app.
Presents two role buttons — Passenger and Driver — and routes
the user to the appropriate login window based on their choice.
"""

import tkinter as tk

from gui.login_window import LoginWindow
from gui.driver_login import DriverLoginWindow
from gui.main_window import MainWindow
from gui.driver_dashboard import DriverDashboard


# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_DARK    = "#1a0000"
BG_CARD    = "#800000"
BG_CARD_LT = "#990000"
GOLD       = "#FFD700"
GOLD_DIM   = "#FFC200"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#FFEECC"
DIVIDER    = "#990000"


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Rides")
        self.root.geometry("520x560")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        tk.Frame(self.root, bg=GOLD, height=4).pack(fill="x")

        header = tk.Frame(self.root, bg=BG_CARD, padx=32, pady=24)
        header.pack(fill="x")

        row = tk.Frame(header, bg=BG_CARD)
        row.pack()

        tk.Label(
            row,
            text="🎓",
            font=("Helvetica", 40),
            bg=BG_CARD,
            fg=GOLD
        ).pack(side="left")

        txt = tk.Frame(row, bg=BG_CARD)
        txt.pack(side="left", padx=(14, 0))

        tk.Label(
            txt,
            text="PUP Rides",
            font=("Helvetica", 24, "bold"),
            bg=BG_CARD,
            fg=GOLD,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            txt,
            text="Polytechnic University of the Philippines",
            font=("Helvetica", 9),
            bg=BG_CARD,
            fg=TEXT_MUTED,
            anchor="w"
        ).pack(anchor="w", pady=(3, 0))

        tk.Frame(self.root, bg=GOLD, height=2).pack(fill="x")

        sub = tk.Frame(self.root, bg=BG_DARK, pady=18)
        sub.pack(fill="x")

        tk.Label(
            sub,
            text="Select your role to continue",
            font=("Helvetica", 11),
            bg=BG_DARK,
            fg=TEXT_MUTED
        ).pack()

        cards = tk.Frame(self.root, bg=BG_DARK)
        cards.pack(fill="both", expand=True, padx=32, pady=(0, 28))
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)

        self._role_card(
            cards, 0, "👤", "Passenger", "Book a ride",
            GOLD, BG_DARK, self.passenger_mode
        )

        self._role_card(
            cards, 1, "🚕", "Driver", "Accept rides",
            BG_CARD, GOLD, self.driver_mode
        )

        tk.Frame(self.root, bg=DIVIDER, height=1).pack(fill="x", padx=32)

        tk.Label(
            self.root,
            text="PUP — Ang Paaralan ng Bayan  🎓",
            font=("Helvetica", 8, "italic"),
            bg=BG_DARK,
            fg=GOLD_DIM
        ).pack(pady=10)

    def _role_card(self, parent, col, icon, title, subtitle, bg, fg, cmd):
        pad = (0, 10) if col == 0 else (10, 0)

        card = tk.Frame(parent, bg=bg)
        card.grid(row=0, column=col, sticky="nsew", padx=pad)

        tk.Button(
            card,
            text=f"{icon}\n\n{title}\n{subtitle}",
            font=("Helvetica", 13, "bold"),
            bg=bg,
            fg=fg,
            relief="flat",
            pady=36,
            cursor="hand2",
            activebackground=BG_CARD_LT,
            activeforeground=GOLD,
            command=cmd,
            wraplength=160,
            justify="center",
        ).pack(fill="both", expand=True)

    # ── Navigation (CLEAN VERSION — NO BACK BUTTON LOGIC) ────────────────────

    def passenger_mode(self):
        self.root.destroy()
        login = LoginWindow()
        account = login.run()

        if account:
            MainWindow(account).run()
        else:
            MainMenu().run()

    def driver_mode(self):
        self.root.destroy()
        login = DriverLoginWindow()
        driver = login.run()

        if driver:
            DriverDashboard(driver).run()
        else:
            MainMenu().run()

    def run(self):
        self.root.mainloop()
        