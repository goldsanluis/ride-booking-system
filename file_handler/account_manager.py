"""
file_handler/account_manager.py
--------------------------------
Handles persistence for passenger accounts: registration, login,
and wallet balance updates. Accounts are stored in data/accounts.json.
"""

import json
import os

from models.account import Account


class AccountManager:
    """
    Manages CRUD operations for passenger accounts in accounts.json.

    Each account is stored as a plain dictionary with the fields:
        user_id, username, password, name, wallet_balance.
    """

    def __init__(self, filename="data/accounts.json"):
        self.filename = filename
        self.ensure_file_exists()

    # ── File Setup ────────────────────────────────────────────────────────────

    def ensure_file_exists(self):
        """
        Create the data directory and an empty accounts file
        if they don't already exist. Called once at startup.
        """
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)  # Start with an empty list

    # ── Raw JSON Access ───────────────────────────────────────────────────────

    def load_accounts(self):
        """
        Read all accounts from the JSON file.

        Returns:
            list[dict]: List of account dictionaries,
                        or an empty list on read error.
        """
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_accounts(self, accounts):
        """
        Write the full list of account dictionaries back to the JSON file.

        Args:
            accounts (list[dict]): Complete list of all accounts to persist.
        """
        with open(self.filename, "w") as f:
            json.dump(accounts, f, indent=4)

    # ── Authentication ────────────────────────────────────────────────────────

    def register(self, username, password, name):
        """
        Create a new passenger account if the username is not taken.
        New accounts receive a ₱5,000 starting wallet balance.

        Args:
            username (str): Desired username.
            password (str): Account password.
            name     (str): Passenger's full display name.

        Returns:
            tuple[bool, str]: (True, success_message) or (False, error_message).
        """
        accounts = self.load_accounts()

        # Reject duplicate usernames
        for acc in accounts:
            if acc["username"] == username:
                return False, "Username already exists!"

        # Auto-increment user_id from the current maximum
        new_id = max((acc["user_id"] for acc in accounts), default=0) + 1

        new_account = {
            "user_id":        new_id,
            "username":       username,
            "password":       password,
            "name":           name,
            "wallet_balance": 5000.0  # Starting balance for all new accounts
        }

        accounts.append(new_account)
        self.save_accounts(accounts)
        return True, "Account created successfully!"

    def login(self, username, password):
        """
        Authenticate a passenger by matching username and password.

        Args:
            username (str): Username to look up.
            password (str): Password to verify.

        Returns:
            tuple[Account | None, str]:
                (Account object, success_message) on success,
                (None, error_message) on failure.
        """
        accounts = self.load_accounts()
        for acc in accounts:
            if acc["username"] == username and acc["password"] == password:
                # Reconstruct an Account object from the stored dictionary
                account = Account(
                    acc["user_id"],
                    acc["username"],
                    acc["password"],
                    acc["name"],
                    acc.get("wallet_balance", 5000.0)
                )
                return account, "Login successful!"
        return None, "Invalid username or password!"

    # ── Wallet Sync ───────────────────────────────────────────────────────────

    def update_account(self, account):
        """
        Persist any changes to an Account object (primarily wallet balance)
        back to the JSON file.

        Args:
            account (Account): The Account object with updated values.

        Returns:
            bool: True if the account was found and updated, False otherwise.
        """
        accounts = self.load_accounts()
        for acc in accounts:
            if acc["username"] == account.username:
                acc["wallet_balance"] = account.wallet_balance
                self.save_accounts(accounts)
                return True
        return False  # Account not found
