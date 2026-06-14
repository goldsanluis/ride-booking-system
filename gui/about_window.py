"""gui/about_window.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_APP      = "#1a0000"   # Deep dark maroon background
BG_SURFACE  = "#800000"   # Maroon card surface
BG_FIELD    = "#6b0000"   # Input field background
MAROON      = "#800000"   # PUP Maroon
MAROON_LT   = "#990000"   # Lighter maroon for hover
GOLD        = "#FFD700"   # PUP Gold
GOLD_DIM    = "#FFC200"   # Slightly dimmer gold
TEXT_WHITE  = "#FFFFFF"   # White text
TEXT_MUTED  = "#FFEECC"   # Warm muted white


class AboutWindow:
    def __init__(self, parent, app_name, version, group_members, section):
        self.win = tk.Toplevel(parent)
        self.win.title("About")
        self.win.configure(bg=BG_APP)
        self.win.resizable(False, False)

        # Header strip
        header = tk.Frame(self.win, bg=MAROON, padx=18, pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎓  PUP Rides",
            font=("Helvetica", 18, "bold"),
            bg=MAROON,
            fg=GOLD,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Polytechnic University of the Philippines",
            font=("Helvetica", 9),
            bg=MAROON,
            fg=TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        # Gold accent line
        tk.Frame(self.win, bg=GOLD, height=3).pack(fill="x")

        tk.Label(
            self.win,
            text="🧾 About Ride Booking System",
            font=("Helvetica", 14, "bold"),
            bg=BG_APP,
            fg=GOLD,
        ).pack(pady=(16, 8), padx=20)

        card = tk.Frame(self.win, bg=BG_SURFACE, padx=18, pady=14)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # Gold top border on card
        tk.Frame(card, bg=GOLD, height=2).pack(fill="x", pady=(0, 10))

        def row(label, value):
            fr = tk.Frame(card, bg=BG_SURFACE)
            fr.pack(fill="x", pady=4)
            tk.Label(
                fr, text=f"{label}",
                font=("Helvetica", 10, "bold"),
                bg=BG_SURFACE, fg=GOLD,
                width=16, anchor="w"
            ).pack(side="left")
            tk.Label(
                fr, text=value,
                font=("Helvetica", 10),
                bg=BG_SURFACE, fg=TEXT_WHITE,
                justify="left", wraplength=420, anchor="w"
            ).pack(side="left", fill="x", expand=True)
            tk.Frame(card, bg=MAROON_LT, height=1).pack(fill="x", pady=(2, 0))

        row("App Name", app_name)
        row("Version", version)
        row("Section", section)

        members_text = "\n".join([f"{i}. {m}" for i, m in enumerate(group_members, start=1)])
        row("Group Members", members_text)

        tk.Button(
            self.win,
            text="Close",
            font=("Helvetica", 10, "bold"),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self.win.destroy,
        ).pack(pady=(6, 16))