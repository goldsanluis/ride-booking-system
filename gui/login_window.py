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


BG_APP      = "#1a0000"
BG_SURFACE  = "#800000"
BG_FIELD    = "#6b0000"
MAROON      = "#800000"
MAROON_LT   = "#990000"
GOLD        = "#FFD700"
GOLD_DIM    = "#FFC200"
TEXT_WHITE  = "#FFFFFF"
TEXT_MUTED  = "#FFEECC"
RED_ERR     = "#FF6B6B"
DIVIDER     = "#990000"


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Rides — Login")
        self.root.geometry("440x680")
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

        self.account_manager   = AccountManager()
        self.logged_in_account = None

        self._show_login_pw = False
        self._show_reg_pw   = False

        self._setup_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        tk.Frame(self.root, bg=GOLD, height=4).pack(fill="x")

        header = tk.Frame(self.root, bg=MAROON, padx=28, pady=22)
        header.pack(fill="x")

        row = tk.Frame(header, bg=MAROON)
        row.pack(fill="x")

        tk.Label(row, text="🎓", font=("Helvetica", 36),
                 bg=MAROON, fg=GOLD).pack(side="left")

        txt = tk.Frame(row, bg=MAROON)
        txt.pack(side="left", padx=(14, 0))

        tk.Label(txt, text="PUP Rides",
                 font=("Helvetica", 22, "bold"),
                 bg=MAROON, fg=GOLD).pack(anchor="w")

        tk.Label(txt, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 9),
                 bg=MAROON, fg=TEXT_MUTED).pack(anchor="w", pady=(3, 0))

        tk.Frame(self.root, bg=GOLD, height=2).pack(fill="x")

        self.card = tk.Frame(self.root, bg=BG_SURFACE, padx=32, pady=26)
        self.card.pack(fill="both", expand=True, padx=20, pady=18)

        self._show_login()

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _clear(self):
        for w in self.card.winfo_children():
            w.destroy()

    def _label(self, text):
        tk.Label(self.card, text=text,
                 font=("Helvetica", 9, "bold"),
                 bg=BG_SURFACE, fg=GOLD_DIM).pack(anchor="w", pady=(8, 2))

    def _entry(self, show=None):
        outer = tk.Frame(self.card, bg=DIVIDER, pady=1)
        outer.pack(fill="x", pady=(0, 2))

        inner = tk.Frame(outer, bg=BG_FIELD, padx=10, pady=7)
        inner.pack(fill="x")

        e = tk.Entry(inner, font=("Helvetica", 10),
                     bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=GOLD,
                     relief="flat",
                     show=show or "")
        e.pack(fill="x")
        return e

    def _pw(self, entry_name, flag_name):
        outer = tk.Frame(self.card, bg=DIVIDER, pady=1)
        outer.pack(fill="x", pady=(0, 2))

        inner = tk.Frame(outer, bg=BG_FIELD, padx=10, pady=6)
        inner.pack(fill="x")

        entry = tk.Entry(inner, font=("Helvetica", 10),
                         bg=BG_FIELD, fg=TEXT_WHITE,
                         insertbackground=GOLD,
                         relief="flat",
                         show="●")
        entry.pack(side="left", fill="x", expand=True)

        setattr(self, entry_name, entry)

        def toggle():
            val = not getattr(self, flag_name)
            setattr(self, flag_name, val)
            entry.config(show="" if val else "●")
            btn.config(text="🙈" if val else "👁")

        btn = tk.Button(inner, text="👁",
                        font=("Helvetica", 9),
                        bg=BG_FIELD,
                        fg=GOLD_DIM,
                        relief="flat",
                        command=toggle)
        btn.pack(side="left", padx=(6, 0))

    def _btn_primary(self, text, cmd):
        tk.Button(self.card, text=text,
                  font=("Helvetica", 11, "bold"),
                  bg=GOLD, fg=BG_APP,
                  relief="flat",
                  padx=10, pady=11,
                  command=cmd).pack(fill="x", pady=(16, 4))

    def _btn_secondary(self, text, cmd):
        tk.Button(self.card, text=text,
                  font=("Helvetica", 10),
                  bg=BG_FIELD, fg=TEXT_WHITE,
                  relief="flat",
                  command=cmd).pack(fill="x", pady=(0, 4))

    def _divider(self):
        tk.Frame(self.card, bg=DIVIDER, height=1).pack(fill="x", pady=10)

    def _error(self):
        lbl = tk.Label(self.card, text="",
                       font=("Helvetica", 9),
                       bg=BG_SURFACE, fg=RED_ERR,
                       wraplength=340, justify="left")
        lbl.pack(anchor="w", pady=(4, 0))
        return lbl

    # ── Screens ──────────────────────────────────────────────────────────────

    def _show_login(self):
        self._clear()
        self._show_login_pw = False

        tk.Label(self.card, text="Welcome back",
                 font=("Helvetica", 15, "bold"),
                 bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")

        tk.Label(self.card, text="Sign in to your account",
                 font=("Helvetica", 9),
                 bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w")

        self._label("Username")
        self.username_entry = self._entry()

        self._label("Password")
        self._pw("password_entry", "_show_login_pw")

        self.login_err = self._error()

        self._btn_primary("Sign In →", self.login)
        self._divider()
        self._btn_secondary("Create Account", self._show_register)

        self.username_entry.focus_set()

    def _show_register(self):
        self._clear()
        self._show_reg_pw = False

        tk.Label(self.card, text="Create account",
                 font=("Helvetica", 15, "bold"),
                 bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")

        self._label("Full Name")
        self.name_entry = self._entry()

        self._label("Username")
        self.reg_username_entry = self._entry()

        self._label("Password")
        self._pw("reg_password_entry", "_show_reg_pw")

        self.reg_err = self._error()

        self._btn_primary("Create Account", self.register)
        self._divider()
        self._btn_secondary("← Back", self._show_login)

    # ── Logic ────────────────────────────────────────────────────────────────

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

        account, msg = self.account_manager.login(username, password)

        if account:
            self.logged_in_account = account
            self.root.destroy()
        else:
            self.login_err.config(text=msg)

    def register(self):
        name = self.name_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()

        if not name:
            self.reg_err.config(text="Full name is required.")
            return

        ok, msg = Account.is_valid_username(username)
        if not ok:
            self.reg_err.config(text=msg)
            return

        ok, msg = Account.is_valid_password(password)
        if not ok:
            self.reg_err.config(text=msg)
            return

        success, msg = self.account_manager.register(username, password, name)

        if success:
            messagebox.showinfo("Success", msg)
            self._show_login()
        else:
            self.reg_err.config(text=msg)

    def run(self):
        self.root.mainloop()
        return self.logged_in_account
    