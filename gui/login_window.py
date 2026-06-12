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

# ── PUP Maroon & Gold Design System ──────────────────────────────────────────
BG_APP      = "#1C0A0A"   # Deep maroon-black background
BG_SURFACE  = "#2A1010"   # Card surface
BG_FIELD    = "#3A1818"   # Input field background
BG_FIELD_HV = "#4A2020"   # Input hover
MAROON      = "#800000"   # PUP Maroon primary
MAROON_LT   = "#A01515"   # Lighter maroon for hover
GOLD        = "#C8A951"   # PUP Gold
GOLD_BRIGHT = "#E8C96B"   # Brighter gold for highlights
GOLD_DIM    = "#8B7535"   # Dimmer gold for secondary text
TEXT_WHITE  = "#F5F0E8"   # Warm white
TEXT_MUTED  = "#7A6060"   # Muted text
RED_ERR     = "#FF6B6B"   # Error red
DIVIDER     = "#3D1A1A"   # Divider line


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Rides — Login")
        self.root.geometry("420x600")
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

        self.account_manager   = AccountManager()
        self.logged_in_account = None
        self._show_login_pw    = False
        self._show_reg_pw      = False

        self._setup_ui()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        # Top brand strip
        brand = tk.Frame(self.root, bg=MAROON, pady=22)
        brand.pack(fill="x")

        tk.Label(brand, text="🎓", font=("Helvetica", 32),
                 bg=MAROON, fg=GOLD_BRIGHT).pack()
        tk.Label(brand, text="PUP Rides",
                 font=("Helvetica", 22, "bold"), bg=MAROON, fg=GOLD_BRIGHT).pack()
        tk.Label(brand, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 8), bg=MAROON, fg=GOLD_DIM).pack()

        # Gold accent line
        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x")

        # Card area
        self.card = tk.Frame(self.root, bg=BG_SURFACE, padx=32, pady=24)
        self.card.pack(fill="both", expand=True, padx=24, pady=20)

        self._show_login()

    def _clear_card(self):
        for w in self.card.winfo_children():
            w.destroy()

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _label(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 10, "bold"),
                 bg=BG_SURFACE, fg=GOLD_DIM).pack(anchor="w", pady=(8, 2))

    def _entry(self, parent, show=None):
        e = tk.Entry(parent, font=("Helvetica", 11), bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=GOLD, relief="flat", bd=0, show=show or "")
        # Padding via inner frame trick
        wrap = tk.Frame(parent, bg=GOLD_DIM, pady=1)
        wrap.pack(fill="x", pady=(0, 4))
        inner = tk.Frame(wrap, bg=BG_FIELD, padx=10, pady=6)
        inner.pack(fill="x")
        e = tk.Entry(inner, font=("Helvetica", 11), bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=GOLD, relief="flat", bd=0, show=show or "")
        e.pack(fill="x")
        return e

    def _pw_row(self, parent, entry_attr, flag_attr):
        wrap = tk.Frame(parent, bg=GOLD_DIM, pady=1)
        wrap.pack(fill="x", pady=(0, 4))
        inner = tk.Frame(wrap, bg=BG_FIELD, padx=10, pady=6)
        inner.pack(fill="x")

        entry = tk.Entry(inner, font=("Helvetica", 11), bg=BG_FIELD, fg=TEXT_WHITE,
                         insertbackground=GOLD, relief="flat", bd=0, show="●")
        entry.pack(side="left", fill="x", expand=True)
        setattr(self, entry_attr, entry)

        def toggle():
            val = not getattr(self, flag_attr)
            setattr(self, flag_attr, val)
            entry.config(show="" if val else "●")
            btn.config(text="🙈" if val else "👁")

        btn = tk.Button(inner, text="👁", font=("Helvetica", 10), bg=BG_FIELD,
                        fg=TEXT_MUTED, relief="flat", bd=0, cursor="hand2", command=toggle)
        btn.pack(side="left", padx=(6, 0))

    def _error_label(self, parent):
        lbl = tk.Label(parent, text="", font=("Helvetica", 9),
                       bg=BG_SURFACE, fg=RED_ERR, wraplength=320, justify="left")
        lbl.pack(anchor="w", pady=(2, 0))
        return lbl

    def _btn_primary(self, parent, text, cmd):
        f = tk.Frame(parent, bg=GOLD, pady=1)
        f.pack(fill="x", pady=(16, 4))
        tk.Button(f, text=text, font=("Helvetica", 12, "bold"),
                  bg=MAROON, fg=GOLD_BRIGHT, relief="flat",
                  padx=10, pady=10, cursor="hand2", activebackground=MAROON_LT,
                  activeforeground=GOLD_BRIGHT, command=cmd).pack(fill="x")

    # ── Login screen ──────────────────────────────────────────────────────────

    def _show_login(self):
        self._clear_card()
        self._show_login_pw = False

        tk.Label(self.card, text="Welcome back",
                 font=("Helvetica", 16, "bold"), bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(self.card, text="Sign in to your account",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 12))

        tk.Frame(self.card, bg=DIVIDER, height=1).pack(fill="x", pady=(0, 12))

        self._label(self.card, "Username")
        self.username_entry = self._entry(self.card)

        self._label(self.card, "Password")
        self._pw_row(self.card, "password_entry", "_show_login_pw")

        self.login_err = self._error_label(self.card)
        self._btn_primary(self.card, "Sign In →", self.login)

        sep = tk.Frame(self.card, bg=BG_SURFACE)
        sep.pack(fill="x", pady=12)
        tk.Frame(sep, bg=DIVIDER, height=1).pack(fill="x")

        tk.Label(self.card, text="Don't have an account?",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=TEXT_MUTED).pack()
        tk.Button(self.card, text="Create account",
                  font=("Helvetica", 10, "bold"), bg=BG_SURFACE, fg=GOLD_BRIGHT,
                  relief="flat", cursor="hand2", activeforeground=GOLD,
                  activebackground=BG_SURFACE, command=self._show_register).pack()

        self.root.bind("<Return>", lambda e: self.login())
        self.username_entry.focus_set()

    # ── Register screen ───────────────────────────────────────────────────────

    def _show_register(self):
        self._clear_card()
        self._show_reg_pw = False

        tk.Label(self.card, text="Create account",
                 font=("Helvetica", 16, "bold"), bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(self.card, text="Join PUP Rides today",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 12))

        tk.Frame(self.card, bg=DIVIDER, height=1).pack(fill="x", pady=(0, 12))

        self._label(self.card, "Full Name")
        self.name_entry = self._entry(self.card)

        self._label(self.card, "Username")
        self.reg_username_entry = self._entry(self.card)

        self._label(self.card, "Password")
        self._pw_row(self.card, "reg_password_entry", "_show_reg_pw")

        self.reg_err = self._error_label(self.card)
        self._btn_primary(self.card, "Create Account", self.register)

        tk.Button(self.card, text="← Back to sign in",
                  font=("Helvetica", 10), bg=BG_SURFACE, fg=GOLD_DIM,
                  relief="flat", cursor="hand2", activeforeground=GOLD,
                  activebackground=BG_SURFACE, command=self._show_login).pack(pady=(10, 0))

        self.root.bind("<Return>", lambda e: self.register())
        self.name_entry.focus_set()

    # ── Actions ───────────────────────────────────────────────────────────────

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.login_err.config(text="Please fill in all fields.")
            return
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
            messagebox.showinfo("Account Created", message + "\nYou can now sign in.")
            self._show_login()
        else:
            self.reg_err.config(text=message)

    def run(self):
        self.root.mainloop()
        return self.logged_in_account

    # Legacy alias kept for backward compat
    def setup_ui(self):
        pass

    def show_login(self):
        self._show_login()

    def show_register(self):
        self._show_register()