"""gui/wallet_panel.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

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


class WalletPanel:
    def __init__(self, parent, account, account_manager):
        self.account = account
        self.account_manager = account_manager

        # Main frame
        self.frame = tk.Frame(parent, bg=BG_APP, padx=15, pady=15)

        # Title
        tk.Label(
            self.frame,
            text="💰 My Wallet",
            font=("Helvetica", 14, "bold"),
            bg=BG_APP,
            fg=GOLD,
        ).pack(pady=(10, 4))

        tk.Frame(self.frame, bg=GOLD, height=2).pack(fill="x", pady=(0, 12))

        # Balance card
        balance_card = tk.Frame(self.frame, bg=BG_SURFACE, padx=20, pady=16)
        balance_card.pack(fill="x", pady=(0, 12))

        tk.Frame(balance_card, bg=GOLD, height=2).pack(fill="x", pady=(0, 10))

        tk.Label(
            balance_card,
            text="Current Balance",
            font=("Helvetica", 10),
            bg=BG_SURFACE,
            fg=TEXT_MUTED,
        ).pack()

        self.balance_label = tk.Label(
            balance_card,
            text=f"₱{self.account.wallet_balance:.2f}",
            font=("Helvetica", 26, "bold"),
            bg=BG_SURFACE,
            fg=GOLD,
        )
        self.balance_label.pack(pady=(4, 0))

        tk.Label(
            balance_card,
            text="Ride Wallet",
            font=("Helvetica", 9),
            bg=BG_SURFACE,
            fg=TEXT_MUTED,
        ).pack()

        # Add money button
        tk.Button(
            self.frame,
            text="➕ Add Money",
            font=("Helvetica", 11, "bold"),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self.add_money,
        ).pack(fill="x", pady=(0, 6))

        # Refresh button
        tk.Button(
            self.frame,
            text="🔄 Refresh Balance",
            font=("Helvetica", 10),
            bg=BG_SURFACE,
            fg=TEXT_WHITE,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self.refresh_balance,
        ).pack(fill="x", pady=(0, 6))

        # Info note
        tk.Label(
            self.frame,
            text="Minimum top-up: ₱50  •  Maximum: ₱50,000",
            font=("Helvetica", 8),
            bg=BG_APP,
            fg=GOLD_DIM,
        ).pack(pady=(8, 0))

    def add_money(self):
        dialog = simpledialog.askfloat(
            "Add Money",
            "Enter amount to add (₱):",
            minvalue=50,
            maxvalue=50000,
        )

        if dialog:
            success, message = self.add_balance(dialog)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_balance()
            else:
                messagebox.showerror("Error", message)

    def add_balance(self, amount):
        accounts = self.account_manager.load_accounts()
        for acc in accounts:
            if acc["username"] == self.account.username:
                acc["wallet_balance"] = acc.get("wallet_balance", 5000.0) + amount
                self.account_manager.save_accounts(accounts)
                self.account.wallet_balance += amount
                return True, f"Added ₱{amount:.2f}!\nNew balance: ₱{self.account.wallet_balance:.2f}"
        return False, "Error updating balance"

    def refresh_balance(self):
        accounts = self.account_manager.load_accounts()
        for acc in accounts:
            if acc["username"] == self.account.username:
                self.account.wallet_balance = acc.get("wallet_balance", 5000.0)
                self.balance_label.config(text=f"₱{self.account.wallet_balance:.2f}")
                return