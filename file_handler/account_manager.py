import json
import os
from models.account import Account

class AccountManager:
    def __init__(self, filename="data/accounts.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_accounts(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_accounts(self, accounts):
        with open(self.filename, "w") as f:
            json.dump(accounts, f, indent=4)

    def register(self, username, password, name):
        accounts = self.load_accounts()
        
        # Check if username exists
        for acc in accounts:
            if acc["username"] == username:
                return False, "Username already exists!"
        
        # Create new account with wallet
        new_id = max([acc["user_id"] for acc in accounts], default=0) + 1
        new_account = {
            "user_id": new_id,
            "username": username,
            "password": password,
            "name": name,
            "wallet_balance": 5000.0
        }
        
        accounts.append(new_account)
        self.save_accounts(accounts)
        return True, "Account created successfully!"

    def login(self, username, password):
        accounts = self.load_accounts()
        for acc in accounts:
            if acc["username"] == username and acc["password"] == password:
                account = Account(
                    acc["user_id"],
                    acc["username"],
                    acc["password"],
                    acc["name"],
                    acc.get("wallet_balance", 5000.0)
                )
                return account, "Login successful!"
        return None, "Invalid username or password!"

    def update_account(self, account):
        accounts = self.load_accounts()
        for acc in accounts:
            if acc["username"] == account.username:
                acc["wallet_balance"] = account.wallet_balance
                self.save_accounts(accounts)
                return True
        return False
