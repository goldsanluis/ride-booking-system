"""gui/about_window.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk

BG_DARK     = "#1a1200"

BG_CARD     = "#2d1f00"
GOLD        = "#FFD700"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"


class AboutWindow:
    def __init__(self, parent, app_name, version, group_members, section):
        self.win = tk.Toplevel(parent)
        self.win.title("About")
        self.win.configure(bg=BG_DARK)
        self.win.resizable(False, False)

        tk.Label(
            self.win,
            text="🧾 About Ride Booking System",
            font=("Helvetica", 16, "bold"),
            bg=BG_DARK,
            fg=GOLD,
        ).pack(pady=(16, 8), padx=20)

        card = tk.Frame(self.win, bg=BG_CARD, padx=18, pady=14)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        def row(label, value):
            fr = tk.Frame(card, bg=BG_CARD)
            fr.pack(fill="x", pady=4)
            tk.Label(fr, text=f"{label}", font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=GOLD_ACCENT, width=16, anchor="w").pack(side="left")
            tk.Label(fr, text=value, font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_WHITE, justify="left", wraplength=420, anchor="w").pack(side="left", fill="x", expand=True)

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
            fg="#1a1200",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.win.destroy,
        ).pack(pady=(6, 16))

