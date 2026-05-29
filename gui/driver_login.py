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
        self.root.geometry("400x500")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.driver_manager = DriverManager()
        self.logged_in_driver = None

        self.setup_ui()

    def setup_ui(self):
        # Logo/Header
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚕",
            font=("Helvetica", 40),
            bg=BG_DARK,
            fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Driver Login",
            font=("Helvetica", 18, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack()

        # Login form
        form_frame = tk.Frame(self.root, bg=BG_DARK)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Username
        tk.Label(
            form_frame,
            text="Username:",
            font=("Helvetica", 11),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(anchor="w", pady=(10, 5))

        self.username_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            width=30
        )
        self.username_entry.pack(fill="x", pady=(0, 15))

        # Password
        tk.Label(
            form_frame,
            text="Password:",
            font=("Helvetica", 11),
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(anchor="w", pady=(10, 5))

        self.password_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            show="*",
            width=30
        )
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Login button
        tk.Button(
            form_frame,
            text="Login 🚪",
            font=("Helvetica", 12, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.login
        ).pack(fill="x", pady=10)

        # Back button
        tk.Button(
            form_frame,
            text="← Back to Menu",
            font=("Helvetica", 10),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.back_to_menu
        ).pack(fill="x", pady=5)

        # Info label
        tk.Label(
            form_frame,
            text="Test account:\nUsername: driver\nPassword: password123",
            font=("Helvetica", 9),
            bg=BG_DARK,
            fg=TEXT_GRAY,
            justify="left"
        ).pack(anchor="w", pady=20)

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
