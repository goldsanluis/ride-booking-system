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


# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
BG_ENTRY    = "#3d2a00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"


class DriverLoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ride Booking System - Driver Login")
        self.root.geometry("520x720")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.driver_manager = DriverManager()
        self.logged_in_driver = None

        self.setup_ui()

    # ---------------- BUTTON HOVER ----------------
    def on_enter(self, btn, color):
        btn.configure(bg=color)

    def on_leave(self, btn, color):
        btn.configure(bg=color)

    # ---------------- PASSWORD TOGGLE ----------------
    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="🙈")
        else:
            self.password_entry.configure(show="*")
            self.eye_btn.configure(text="👁")

    # ---------------- FLOATING LABEL BEHAVIOR ----------------
    def float_up(self, label):
        label.configure(fg=GOLD)

    def float_down(self, label, entry):
        if not entry.get():
            label.configure(fg=TEXT_GRAY)

    # ---------------- UI SETUP ----------------
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_DARK, pady=25)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚕",
            font=("Segoe UI Emoji", 44),
            bg=BG_DARK,
            fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Driver Login",
            font=("Segoe UI", 26, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack(pady=(5, 0))

        # CARD
        form_frame = tk.Frame(
            self.root,
            bg=BG_CARD,
            padx=35,
            pady=35
        )
        form_frame.pack(fill="both", expand=True, padx=30, pady=(10, 25))

        # ---------------- USERNAME (Floating Label) ----------------
        self.username_label = tk.Label(
            form_frame,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=BG_CARD,
            fg=TEXT_GRAY
        )
        self.username_label.pack(anchor="w")

        self.username_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat",
            bd=0
        )
        self.username_entry.pack(fill="x", ipady=10, pady=(5, 18))

        self.username_entry.bind("<FocusIn>", lambda e: self.float_up(self.username_label))
        self.username_entry.bind("<FocusOut>", lambda e: self.float_down(self.username_label, self.username_entry))

        # ---------------- PASSWORD (Floating Label + Eye Button) ----------------
        self.password_label = tk.Label(
            form_frame,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=BG_CARD,
            fg=TEXT_GRAY
        )
        self.password_label.pack(anchor="w")

        pass_frame = tk.Frame(form_frame, bg=BG_CARD)
        pass_frame.pack(fill="x", pady=(5, 22))

        self.password_entry = tk.Entry(
            pass_frame,
            font=("Segoe UI", 13),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat",
            bd=0,
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=10)

        self.eye_btn = tk.Button(
            pass_frame,
            text="👁",
            font=("Segoe UI", 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        )
        self.eye_btn.pack(side="right", padx=(8, 0))

        self.password_entry.bind("<FocusIn>", lambda e: self.float_up(self.password_label))
        self.password_entry.bind("<FocusOut>", lambda e: self.float_down(self.password_label, self.password_entry))

        # ---------------- LOGIN BUTTON (Pseudo-rounded) ----------------
        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=("Segoe UI", 13, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            pady=14,
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(fill="x", pady=(10, 8))

        login_btn.bind("<Enter>", lambda e: self.on_enter(login_btn, GOLD_ACCENT))
        login_btn.bind("<Leave>", lambda e: self.on_leave(login_btn, GOLD))

        # ---------------- BACK BUTTON ----------------
        back_btn = tk.Button(
            form_frame,
            text="← BACK TO MENU",
            font=("Segoe UI", 11),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.back_to_menu
        )
        back_btn.pack(fill="x", pady=5)

        back_btn.bind("<Enter>", lambda e: self.on_enter(back_btn, "#996f00"))
        back_btn.bind("<Leave>", lambda e: self.on_leave(back_btn, GOLD_DARK))

        # Divider
        tk.Frame(form_frame, bg="#5c4200", height=1).pack(fill="x", pady=20)

        # Test Account Info
        tk.Message(
            form_frame,
            text="TEST ACCOUNT\nUsername: juan\nPassword: password123",
            font=("Consolas", 10),
            bg=BG_CARD,
            fg=TEXT_GRAY,
            width=320
        ).pack(anchor="w")

    # ---------------- LOGIN LOGIC ----------------
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        driver = self.driver_manager.get_driver(username, password)

        if driver:
            if "wallet_balance" not in driver:
                driver["wallet_balance"] = 0.0

            self.logged_in_driver = driver
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def back_to_menu(self):
        self.root.destroy()
        self.logged_in_driver = None

    def run(self):
        self.root.mainloop()
        return self.logged_in_driver
    