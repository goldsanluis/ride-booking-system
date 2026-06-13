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


# Professional Slate & Blue Theme Colors
BG_DARK     = "#0f172a"   # deep slate background
BG_CARD     = "#1e293b"   # card surface
BG_ENTRY    = "#334155"   # input field background
ACCENT      = "#3b82f6"   # primary blue accent
ACCENT_DARK = "#1d4ed8"   # darker blue (hover)
ACCENT_LIGHT = "#60a5fa"  # lighter blue (focus highlight)
TEXT_WHITE  = "#f8fafc"
TEXT_GRAY   = "#94a3b8"
BORDER      = "#475569"

FONT_FAMILY = "Segoe UI"


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
            self.eye_btn.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.eye_btn.configure(text="Show")

    # ---------------- FLOATING LABEL BEHAVIOR ----------------
    def float_up(self, label):
        label.configure(fg=ACCENT_LIGHT)

    def float_down(self, label, entry):
        if not entry.get():
            label.configure(fg=TEXT_GRAY)

    # ---------------- UI SETUP ----------------
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_DARK, pady=30)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚕",
            font=("Segoe UI Emoji", 48),
            bg=BG_DARK,
            fg=ACCENT_LIGHT
        ).pack()

        tk.Label(
            header,
            text="Driver Login",
            font=(FONT_FAMILY, 28, "bold"),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(pady=(8, 2))

        tk.Label(
            header,
            text="Sign in to access your driver dashboard",
            font=(FONT_FAMILY, 10),
            bg=BG_DARK,
            fg=TEXT_GRAY
        ).pack()

        # CARD
        form_frame = tk.Frame(
            self.root,
            bg=BG_CARD,
            padx=35,
            pady=35,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        form_frame.pack(fill="both", expand=True, padx=30, pady=(15, 25))

        # ---------------- USERNAME (Floating Label) ----------------
        self.username_label = tk.Label(
            form_frame,
            text="Username",
            font=(FONT_FAMILY, 10, "bold"),
            bg=BG_CARD,
            fg=TEXT_GRAY
        )
        self.username_label.pack(anchor="w")

        self.username_entry = tk.Entry(
            form_frame,
            font=(FONT_FAMILY, 13),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        self.username_entry.pack(fill="x", ipady=10, pady=(6, 20))

        self.username_entry.bind("<FocusIn>", lambda e: self.float_up(self.username_label))
        self.username_entry.bind("<FocusOut>", lambda e: self.float_down(self.username_label, self.username_entry))

        # ---------------- PASSWORD (Floating Label + Eye Button) ----------------
        self.password_label = tk.Label(
            form_frame,
            text="Password",
            font=(FONT_FAMILY, 10, "bold"),
            bg=BG_CARD,
            fg=TEXT_GRAY
        )
        self.password_label.pack(anchor="w")

        pass_frame = tk.Frame(
            form_frame,
            bg=BG_ENTRY,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT
        )
        pass_frame.pack(fill="x", pady=(6, 24))

        self.password_entry = tk.Entry(
            pass_frame,
            font=(FONT_FAMILY, 13),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat",
            bd=0,
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(8, 0))

        self.eye_btn = tk.Button(
            pass_frame,
            text="Show",
            font=(FONT_FAMILY, 9, "bold"),
            bg=BG_ENTRY,
            fg=ACCENT_LIGHT,
            relief="flat",
            cursor="hand2",
            activebackground=BG_ENTRY,
            activeforeground=ACCENT_LIGHT,
            command=self.toggle_password
        )
        self.eye_btn.pack(side="right", padx=(8, 10))

        self.password_entry.bind("<FocusIn>", lambda e: self.float_up(self.password_label))
        self.password_entry.bind("<FocusOut>", lambda e: self.float_down(self.password_label, self.password_entry))

        # ---------------- LOGIN BUTTON ----------------
        login_btn = tk.Button(
            form_frame,
            text="LOG IN",
            font=(FONT_FAMILY, 13, "bold"),
            bg=ACCENT,
            fg=TEXT_WHITE,
            activebackground=ACCENT_DARK,
            activeforeground=TEXT_WHITE,
            relief="flat",
            pady=14,
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(fill="x", pady=(12, 10))

        login_btn.bind("<Enter>", lambda e: self.on_enter(login_btn, ACCENT_DARK))
        login_btn.bind("<Leave>", lambda e: self.on_leave(login_btn, ACCENT))

        # ---------------- BACK BUTTON ----------------
        back_btn = tk.Button(
            form_frame,
            text="← Back to Menu",
            font=(FONT_FAMILY, 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            activebackground=BORDER,
            activeforeground=TEXT_WHITE,
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.back_to_menu
        )
        back_btn.pack(fill="x", pady=5)

        back_btn.bind("<Enter>", lambda e: self.on_enter(back_btn, BORDER))
        back_btn.bind("<Leave>", lambda e: self.on_leave(back_btn, BG_ENTRY))

        # Divider
        tk.Frame(form_frame, bg=BORDER, height=1).pack(fill="x", pady=22)

        # Test Account Info
        info_frame = tk.Frame(
            form_frame,
            bg=BG_ENTRY,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        info_frame.pack(fill="x")

        tk.Label(
            info_frame,
            text="TEST ACCOUNT",
            font=(FONT_FAMILY, 9, "bold"),
            bg=BG_ENTRY,
            fg=ACCENT_LIGHT,
            anchor="w"
        ).pack(fill="x", padx=12, pady=(10, 2))

        tk.Message(
            info_frame,
            text="Username: juan\nPassword: password123",
            font=("Consolas", 10),
            bg=BG_ENTRY,
            fg=TEXT_GRAY,
            width=320
        ).pack(anchor="w", padx=12, pady=(0, 10))

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
    