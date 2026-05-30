import tkinter as tk
from tkinter import messagebox, simpledialog

class WalletPanel:
    def __init__(self, parent, account, account_manager):
        self.account = account
        self.account_manager = account_manager
        
        # Main frame
        self.frame = tk.Frame(parent, bg="#2d1f00", padx=15, pady=15)
        
        # Title
        tk.Label(
            self.frame,
            text="💰 My Wallet",
            font=("Helvetica", 14, "bold"),
            bg="#2d1f00",
            fg="#FFD700"
        ).pack(pady=10)
        
        # Balance display
        self.balance_label = tk.Label(
            self.frame,
            text=f"Balance: ₱{self.account.wallet_balance:.2f}",
            font=("Helvetica", 16, "bold"),
            bg="#2d1f00",
            fg="#FFA500"
        )
        self.balance_label.pack(pady=10)
        
        # Add money button
        tk.Button(
            self.frame,
            text="➕ Add Money",
            font=("Helvetica", 11, "bold"),
            bg="#4ecca3",
            fg="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.add_money
        ).pack(fill="x", pady=5)
        
        # Refresh button
        tk.Button(
            self.frame,
            text="🔄 Refresh Balance",
            font=("Helvetica", 10),
            bg="#B8860B",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.refresh_balance
        ).pack(fill="x", pady=5)

    def add_money(self):
        dialog = simpledialog.askfloat(
            "Add Money",
            "Enter amount to add (₱):",
            minvalue=50,
            maxvalue=50000
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
                self.balance_label.config(text=f"Balance: ₱{self.account.wallet_balance:.2f}")
                return
