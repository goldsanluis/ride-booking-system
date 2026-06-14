"""
gui/driver_login.py
----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
from file_handler.driver_manager import DriverManager

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_APP      = "#1a0000"   # Deep dark maroon background
BG_SURFACE  = "#800000"   # Maroon card surface
BG_FIELD    = "#6b0000"   # Input field background
MAROON      = "#800000"   # PUP Maroon
GOLD        = "#FFD700"   # PUP Gold
TEXT_WHITE  = "#FFFFFF"   # White text
TEXT_MUTED  = "#FFFFFF"   # White subtext
RED_ERR     = "#FF6B6B"   # Error red
DIVIDER     = "#990000"   # Divider line


class DriverLoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Rides — Driver Login")
        self.root.geometry("420x600")
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

        self.driver_manager = DriverManager()
        self.logged_in_driver = None
        self._show_pw = False

        self.setup_ui()

    # ── Password toggle ───────────────────────────────────────────────────────
    def toggle_password(self):
        self._show_pw = not self._show_pw
        self.password_entry.configure(show="" if self._show_pw else "●")
        self.eye_btn.configure(text="🙈" if self._show_pw else "👁")

    # ── UI Setup ──────────────────────────────────────────────────────────────
    def setup_ui(self):
        # ── Header (matches login_window style) ───────────────────────────────
        header = tk.Frame(self.root, bg=MAROON, padx=18, pady=18)
        header.pack(fill="x")

        tk.Frame(header, bg=BG_APP, height=6).pack(fill="x", pady=(0, 10))

        title_row = tk.Frame(header, bg=MAROON)
        title_row.pack(fill="x")

        tk.Label(title_row, text="🚕", font=("Helvetica", 34),
                 bg=MAROON, fg=GOLD).pack(side="left")

        txt_wrap = tk.Frame(title_row, bg=MAROON)
        txt_wrap.pack(side="left", fill="x", expand=True, padx=(14, 0))

        tk.Label(txt_wrap, text="PUP Rides",
                 font=("Helvetica", 24, "bold"), bg=MAROON, fg=GOLD,
                 justify="left").pack(anchor="w")
        tk.Label(txt_wrap, text="Driver Portal",
                 font=("Helvetica", 10), bg=MAROON, fg=TEXT_MUTED,
                 justify="left").pack(anchor="w", pady=(4, 0))

        tk.Label(header, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 8), bg=MAROON, fg=GOLD).pack(anchor="w", pady=(10, 0))

        # Gold accent line
        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x", pady=(10, 0))

        # ── Card ──────────────────────────────────────────────────────────────
        card = tk.Frame(self.root, bg=BG_SURFACE, padx=34, pady=28)
        card.pack(fill="both", expand=True, padx=22, pady=18)

        tk.Label(card, text="Welcome, Driver",
                 font=("Helvetica", 16, "bold"), bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(card, text="Sign in to your driver dashboard",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 12))

        tk.Frame(card, bg=DIVIDER, height=1).pack(fill="x", pady=(0, 12))

        # Username
        tk.Label(card, text="Username", font=("Helvetica", 10, "bold"),
                 bg=BG_SURFACE, fg=GOLD).pack(anchor="w", pady=(8, 2))
        wrap_u = tk.Frame(card, bg=GOLD, pady=1)
        wrap_u.pack(fill="x", pady=(0, 6))
        inner_u = tk.Frame(wrap_u, bg=BG_FIELD, padx=12, pady=7)
        inner_u.pack(fill="x")
        self.username_entry = tk.Entry(
            inner_u, font=("Helvetica", 11),
            bg=BG_FIELD, fg=TEXT_WHITE, insertbackground=GOLD,
            relief="flat", bd=0)
        self.username_entry.pack(fill="x")

        # Password
        tk.Label(card, text="Password", font=("Helvetica", 10, "bold"),
                 bg=BG_SURFACE, fg=GOLD).pack(anchor="w", pady=(8, 2))
        wrap_p = tk.Frame(card, bg=GOLD, pady=1)
        wrap_p.pack(fill="x", pady=(0, 6))
        inner_p = tk.Frame(wrap_p, bg=BG_FIELD, padx=10, pady=6)
        inner_p.pack(fill="x")
        self.password_entry = tk.Entry(
            inner_p, font=("Helvetica", 11),
            bg=BG_FIELD, fg=TEXT_WHITE, insertbackground=GOLD,
            relief="flat", bd=0, show="●")
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.eye_btn = tk.Button(
            inner_p, text="👁",
            font=("Helvetica", 10, "bold"),
            bg=GOLD, fg=BG_APP, relief="flat", bd=0,
            padx=8, pady=4, cursor="hand2",
            activebackground=BG_APP, activeforeground=GOLD,
            command=self.toggle_password)
        self.eye_btn.pack(side="left", padx=(8, 0))

        # Error label
        self.err_label = tk.Label(card, text="", font=("Helvetica", 9),
                                  bg=BG_SURFACE, fg=RED_ERR, wraplength=320, justify="left")
        self.err_label.pack(anchor="w", pady=(2, 0))

        # Login button
        btn_wrap = tk.Frame(card, bg=GOLD, pady=1)
        btn_wrap.pack(fill="x", pady=(20, 6))
        tk.Button(btn_wrap, text="Sign In →",
                  font=("Helvetica", 12, "bold"),
                  bg=GOLD, fg=BG_APP, relief="flat",
                  padx=10, pady=12, cursor="hand2",
                  activebackground=BG_APP, activeforeground=GOLD,
                  command=self.login).pack(fill="x")

        # Divider
        tk.Frame(card, bg=DIVIDER, height=1).pack(fill="x", pady=12)

        # Back button
        tk.Button(card, text="← Back to Menu",
                  font=("Helvetica", 10), bg=BG_SURFACE, fg=GOLD,
                  relief="flat", cursor="hand2",
                  activeforeground=GOLD, activebackground=BG_SURFACE,
                  command=self.back_to_menu).pack()

        # Test account info
        info = tk.Frame(card, bg=BG_FIELD, padx=10, pady=8)
        info.pack(fill="x", pady=(12, 0))
        tk.Label(info, text="TEST ACCOUNT",
                 font=("Helvetica", 8, "bold"), bg=BG_FIELD, fg=GOLD).pack(anchor="w")
        tk.Label(info, text="Username: juan\nPassword: password123",
                 font=("Courier", 9), bg=BG_FIELD, fg=TEXT_MUTED, justify="left").pack(anchor="w")

        self.root.bind("<Return>", lambda e: self.login())
        self.username_entry.focus_set()

    # ── Login logic ───────────────────────────────────────────────────────────
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.err_label.config(text="Please enter username and password.")
            return

        driver = self.driver_manager.get_driver(username, password)

        if driver:
            if "wallet_balance" not in driver:
                driver["wallet_balance"] = 0.0
            self.logged_in_driver = driver
            self.root.destroy()
        else:
            self.err_label.config(text="Invalid username or password.")

    def back_to_menu(self):
        self.root.destroy()
        self.logged_in_driver = None

    def run(self):
        self.root.mainloop()
        return self.logged_in_driver