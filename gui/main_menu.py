"""
gui/main_menu.py
----------------
author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk

BG_DARK    = "#1a0000"
BG_CARD    = "#800000"
BG_CARD_LT = "#990000"
BG_FIELD   = "#6b0000"
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
        tk.Label(row, text="🎓", font=("Helvetica", 40),
                 bg=BG_CARD, fg=GOLD).pack(side="left")
        txt = tk.Frame(row, bg=BG_CARD)
        txt.pack(side="left", padx=(14, 0))
        tk.Label(txt, text="PUP Rides",
                 font=("Helvetica", 24, "bold"), bg=BG_CARD, fg=GOLD,
                 anchor="w").pack(anchor="w")
        tk.Label(txt, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_MUTED,
                 anchor="w").pack(anchor="w", pady=(3, 0))

        tk.Frame(self.root, bg=GOLD, height=2).pack(fill="x")

        sub = tk.Frame(self.root, bg=BG_DARK, pady=18)
        sub.pack(fill="x")
        tk.Label(sub, text="Select your role to continue",
                 font=("Helvetica", 11), bg=BG_DARK, fg=TEXT_MUTED).pack()

        cards = tk.Frame(self.root, bg=BG_DARK)
        cards.pack(fill="both", expand=True, padx=32, pady=(0, 28))
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)

        self._role_card(cards, col=0, icon="👤", title="Passenger",
                        subtitle="Book a ride", bg=GOLD, fg=BG_DARK,
                        cmd=self.passenger_mode)
        self._role_card(cards, col=1, icon="🚕", title="Driver",
                        subtitle="Accept rides", bg=BG_CARD, fg=GOLD,
                        cmd=self.driver_mode)

        tk.Frame(self.root, bg=DIVIDER, height=1).pack(fill="x", padx=32)
        tk.Label(self.root, text="PUP — Ang Paaralan ng Bayan  🎓",
                 font=("Helvetica", 8, "italic"), bg=BG_DARK, fg=GOLD_DIM,
                 ).pack(pady=10)

    def _role_card(self, parent, col, icon, title, subtitle, bg, fg, cmd):
        pad = (0, 10) if col == 0 else (10, 0)
        card = tk.Frame(parent, bg=bg)
        card.grid(row=0, column=col, sticky="nsew", padx=pad)
        tk.Button(
            card,
            text=f"{icon}\n\n{title}\n{subtitle}",
            font=("Helvetica", 13, "bold"),
            bg=bg, fg=fg, relief="flat", pady=36, cursor="hand2",
            activebackground=BG_CARD_LT, activeforeground=GOLD,
            command=cmd, wraplength=160, justify="center",
        ).pack(fill="both", expand=True)

    # ── Navigation ────────────────────────────────────────────────────────────

    def passenger_mode(self):
        # Hide (don't destroy) the menu while login is open.
        self.root.withdraw()

        from gui.login_window import LoginWindow
        login   = LoginWindow(on_back=self._return_to_menu)
        account = login.run()   # blocks until login window closes

        if account:
            # Successful login — destroy menu and open dashboard.
            self.root.destroy()
            from gui.main_window import MainWindow
            MainWindow(account).run()
        elif self.root.winfo_exists():
            # Back button was used — _return_to_menu already showed the root,
            # so we don't need to do anything else here.
            pass

    def _return_to_menu(self):
        # Called by the Back button in LoginWindow.
        # Just un-hide the already-existing menu window.
        if self.root.winfo_exists():
            self.root.deiconify()

    def driver_mode(self):
        self.root.withdraw()

        from gui.driver_login import DriverLoginWindow
        login  = DriverLoginWindow()
        driver = login.run()

        if driver:
            self.root.destroy()
            from gui.driver_dashboard import DriverDashboard
            DriverDashboard(driver).run()
        elif self.root.winfo_exists():
            self.root.deiconify()

    def run(self):
        self.root.mainloop()
        