import json
import os

class AccountManager:
    def __init__(self, filename="data/accounts.json"):
        self.filename = filename
        self.accounts = []
        self.next_id = 1
        self.ensure_file_exists()
        self.load_accounts()

    def ensure_file_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def load_accounts(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                from models.account import Account
                for item in data:
                    account = Account(
                        item["user_id"],
                        item["username"],
                        item["password"],
                        item["name"]
                    )
                    self.accounts.append(account)
                if self.accounts:
                    self.next_id = max(a.user_id for a in self.accounts) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.accounts = []

    def save_accounts(self):
        data = []
        for account in self.accounts:
            data.append({
                "user_id": account.user_id,
                "username": account.username,
                "password": account.password,
                "name": account.name
            })
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def register(self, username, password, name):
        # Check if username already exists
        for account in self.accounts:
            if account.username == username:
                return None, "Username already exists!"
        from models.account import Account
        account = Account(self.next_id, username, password, name)
        self.accounts.append(account)
        self.next_id += 1
        self.save_accounts()
        return account, "Account created successfully!"

    def login(self, username, password):
        for account in self.accounts:
            if account.username == username:
                if account.check_password(password):
                    return account, "Login successful!"
                return None, "Incorrect password!"
        return None, "Username not found!"