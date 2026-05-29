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
        self.root.geometry("400x750")
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
            text="Driver Portal",
            font=("Helvetica", 18, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack()

        tk.Label(
            header,
            text="Start earning today!",
            font=("Helvetica", 10),
            bg=BG_DARK,
            fg=TEXT_GRAY
        ).pack()

        # Login Frame
        self.login_frame = tk.Frame(self.root, bg=BG_CARD, padx=30, pady=20)
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_login()

    def clear_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()

        tk.Label(
            self.login_frame,
            text="Welcome Back! 🚗",
            font=("Helvetica", 16, "bold"),
            bg=BG_CARD,
            fg=GOLD
        ).pack(pady=10)

        # Username
        tk.Label(
            self.login_frame,
            text="Username",
            font=("Helvetica", 11),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5
        )
        self.username_entry.pack(fill="x", pady=5)

        # Password
        tk.Label(
            self.login_frame,
            text="Password",
            font=("Helvetica", 11),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 11),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5,
            show="●"
        )
        self.password_entry.pack(fill="x", pady=5)

        # Login Button
        tk.Button(
            self.login_frame,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.login
        ).pack(fill="x", pady=15)

        # Register Link
        tk.Label(
            self.login_frame,
            text="Don't have an account?",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=TEXT_GRAY
        ).pack()

        tk.Button(
            self.login_frame,
            text="Register as Driver",
            font=("Helvetica", 10, "underline"),
            bg=BG_CARD,
            fg=GOLD,
            relief="flat",
            cursor="hand2",
            command=self.show_register
        ).pack()

    def show_register(self):
        self.clear_frame()

        tk.Label(
            self.login_frame,
            text="Driver Registration",
            font=("Helvetica", 16, "bold"),
            bg=BG_CARD,
            fg=GOLD
        ).pack(pady=10)

        # Name
        tk.Label(
            self.login_frame,
            text="Full Name",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.name_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 10),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5
        )
        self.name_entry.pack(fill="x", pady=3)

        # Username
        tk.Label(
            self.login_frame,
            text="Username",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.reg_username_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 10),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5
        )
        self.reg_username_entry.pack(fill="x", pady=3)

        # Password
        tk.Label(
            self.login_frame,
            text="Password",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.reg_password_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 10),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5,
            show="●"
        )
        self.reg_password_entry.pack(fill="x", pady=3)

        # Phone
        tk.Label(
            self.login_frame,
            text="Phone",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.phone_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 10),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5
        )
        self.phone_entry.pack(fill="x", pady=3)

        # Plate
        tk.Label(
            self.login_frame,
            text="Vehicle Plate",
            font=("Helvetica", 10),
            bg=BG_CARD,
            fg=GOLD_ACCENT
        ).pack(anchor="w")

        self.plate_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 10),
            bg=BG_ENTRY,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5
        )
        self.plate_entry.pack(fill="x", pady=3)

        # Register Button
        tk.Button(
            self.login_frame,
            text="Register",
            font=("Helvetica", 11, "bold"),
            bg=GOLD,
            fg=BG_DARK,
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.register
        ).pack(fill="x", pady=10)

        # Back to Login
        tk.Button(
            self.login_frame,
            text="← Back to Login",
            font=("Helvetica", 10, "underline"),
            bg=BG_CARD,
            fg=GOLD,
            relief="flat",
            cursor="hand2",
            command=self.show_login
        ).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        driver, message = self.driver_manager.login(username, password)
        if driver:
            self.logged_in_driver = driver
            self.root.destroy()
        else:
            messagebox.showerror("Error", message)

    def register(self):
        name = self.name_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        phone = self.phone_entry.get()
        plate = self.plate_entry.get()

        if not all([name, username, password, phone, plate]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        driver, message = self.driver_manager.register(username, password, name, phone, plate, "Car")
        if driver:
            messagebox.showinfo("Success", message + "\nPlease login!")
            self.show_login()
        else:
            messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()
        return self.logged_in_driver