"""gui/login_window.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
from file_handler.account_manager import AccountManager
from models.account import Account


# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
BG_ENTRY    = "#3d2a00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"
RED         = "#FF6B6B"


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ride Booking System - Login")
        self.root.geometry("400x560")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.account_manager   = AccountManager()
        self.logged_in_account = None

        self._show_login_pw  = False  # password visibility toggle state
        self._show_reg_pw    = False

        self.setup_ui()

    # ── Static layout ─────────────────────────────────────────────────────────

    def setup_ui(self):
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x")

        tk.Label(header, text="🚗", font=("Helvetica", 40),
                 bg=BG_DARK, fg=GOLD).pack()
        tk.Label(header, text="Ride Booking System",
                 font=("Helvetica", 18, "bold"), bg=BG_DARK, fg=GOLD).pack()
        tk.Label(header, text="Your ride, your way!",
                 font=("Helvetica", 10), bg=BG_DARK, fg=TEXT_GRAY).pack()

        self.login_frame = tk.Frame(self.root, bg=BG_CARD, padx=30, pady=20)
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_login()

    def _clear_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _make_entry(self, parent, show=None):
        """Create a styled Entry widget."""
        e = tk.Entry(
            parent,
            font=("Helvetica", 11),
            bg=BG_ENTRY, fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat", bd=5,
            show=show or "",
        )
        e.pack(fill="x", pady=5)
        return e

    def _make_label(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 11),
                 bg=BG_CARD, fg=GOLD_ACCENT).pack(anchor="w")

    def _make_pw_row(self, parent, entry_attr, show_flag_attr):
        """
        Build a password entry + show/hide toggle button in a row.
        entry_attr      -- name to store the Entry on self
        show_flag_attr  -- name of the bool toggle on self
        """
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", pady=5)

        entry = tk.Entry(
            row,
            font=("Helvetica", 11),
            bg=BG_ENTRY, fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat", bd=5,
            show="●",
        )
        entry.pack(side="left", fill="x", expand=True)
        setattr(self, entry_attr, entry)

        def toggle():
            current = getattr(self, show_flag_attr)
            new_val = not current
            setattr(self, show_flag_attr, new_val)
            entry.config(show="" if new_val else "●")
            btn.config(text="🙈" if new_val else "👁")

        btn = tk.Button(
            row, text="👁",
            font=("Helvetica", 10),
            bg=BG_ENTRY, fg=TEXT_GRAY,
            relief="flat", bd=0,
            cursor="hand2",
            command=toggle,
        )
        btn.pack(side="left", padx=(4, 0))

    def _make_error_label(self, parent):
        """A small red label used for inline validation feedback."""
        lbl = tk.Label(parent, text="", font=("Helvetica", 9),
                       bg=BG_CARD, fg=RED, wraplength=300, justify="left")
        lbl.pack(anchor="w")
        return lbl

    # ── Login screen ──────────────────────────────────────────────────────────

    def show_login(self):
        self._clear_frame()
        self._show_login_pw = False

        tk.Label(self.login_frame, text="Welcome Back! 👑",
                 font=("Helvetica", 16, "bold"), bg=BG_CARD, fg=GOLD).pack(pady=10)

        self._make_label(self.login_frame, "Username")
        self.username_entry = self._make_entry(self.login_frame)

        self._make_label(self.login_frame, "Password")
        self._make_pw_row(self.login_frame, "password_entry", "_show_login_pw")

        self.login_err = self._make_error_label(self.login_frame)

        tk.Button(
            self.login_frame, text="Login",
            font=("Helvetica", 12, "bold"),
            bg=GOLD, fg=BG_DARK, relief="flat",
            padx=10, pady=8, cursor="hand2",
            command=self.login,
        ).pack(fill="x", pady=15)

        tk.Label(self.login_frame, text="Don't have an account?",
                 font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_GRAY).pack()
        tk.Button(
            self.login_frame, text="Register here",
            font=("Helvetica", 10, "underline"),
            bg=BG_CARD, fg=GOLD, relief="flat",
            cursor="hand2", command=self.show_register,
        ).pack()

        # Allow Enter key to submit
        self.root.bind("<Return>", lambda e: self.login())
        self.username_entry.focus_set()

    # ── Register screen ───────────────────────────────────────────────────────

    def show_register(self):
        self._clear_frame()
        self._show_reg_pw = False

        tk.Label(self.login_frame, text="Create Account",
                 font=("Helvetica", 16, "bold"), bg=BG_CARD, fg=GOLD).pack(pady=10)

        self._make_label(self.login_frame, "Full Name")
        self.name_entry = self._make_entry(self.login_frame)

        self._make_label(self.login_frame, "Username")
        self.reg_username_entry = self._make_entry(self.login_frame)

        self._make_label(self.login_frame, "Password")
        self._make_pw_row(self.login_frame, "reg_password_entry", "_show_reg_pw")

        self.reg_err = self._make_error_label(self.login_frame)

        tk.Button(
            self.login_frame, text="Register",
            font=("Helvetica", 12, "bold"),
            bg=GOLD, fg=BG_DARK, relief="flat",
            padx=10, pady=8, cursor="hand2",
            command=self.register,
        ).pack(fill="x", pady=15)

        tk.Button(
            self.login_frame, text="← Back to Login",
            font=("Helvetica", 10, "underline"),
            bg=BG_CARD, fg=GOLD, relief="flat",
            cursor="hand2", command=self.show_login,
        ).pack()

        self.root.bind("<Return>", lambda e: self.register())
        self.name_entry.focus_set()

    # ── Actions ───────────────────────────────────────────────────────────────

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.login_err.config(text="Please fill in all fields.")
            return

        # Admin login check
        from gui.admin_dashboard import is_admin, AdminDashboard
        if is_admin(username, password):
            self.root.destroy()
            AdminDashboard().run()
            return

        account, message = self.account_manager.login(username, password)
        if account:
            self.logged_in_account = account
            self.root.destroy()
        else:
            self.login_err.config(text=message)

    def register(self):
        name     = self.name_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()

        if not name:
            self.reg_err.config(text="Full name is required.")
            return

        ok, reason = Account.is_valid_username(username)
        if not ok:
            self.reg_err.config(text=reason)
            return

        ok, reason = Account.is_valid_password(password)
        if not ok:
            self.reg_err.config(text=reason)
            return

        success, message = self.account_manager.register(username, password, name)
        if success:
            messagebox.showinfo("Success", message + "\nPlease login!")
            self.show_login()
        else:
            self.reg_err.config(text=message)

    def run(self):
        self.root.mainloop()
        return self.logged_in_account