"""
models/account.py
-----------------
Represents a registered passenger account.
Encapsulates user credentials and wallet balance in one object.
"""


class Account:
    """
    A passenger account with login credentials and an in-app wallet.

    Attributes:
        user_id        (int):   Unique numeric ID assigned at registration.
        username       (str):   Login username (must be unique).
        password       (str):   Plain-text password (stored as-is for simplicity).
        name           (str):   Passenger's display name.
        wallet_balance (float): Current in-app wallet balance in ₱.
    """

    def __init__(self, user_id, username, password, name, wallet_balance=5000.0):
        self.user_id        = user_id
        self.username       = username
        self.password       = password
        self.name           = name
        self.wallet_balance = wallet_balance  # New accounts start with ₱5,000

    def check_password(self, password):
        """
        Verify whether the supplied password matches this account's password.

        Args:
            password (str): Password to check.

        Returns:
            bool: True if passwords match, False otherwise.
        """
        return self.password == password

    def add_money(self, amount):
        """
        Top up the wallet by the given amount.

        Args:
            amount (float): Amount in ₱ to add.

        Returns:
            str: Confirmation message with the new balance.
        """
        self.wallet_balance += amount
        return f"Added ₱{amount:.2f}. New balance: ₱{self.wallet_balance:.2f}"

    def deduct_money(self, amount):
        """
        Deduct a fare payment from the wallet, if funds are sufficient.

        Args:
            amount (float): Amount in ₱ to deduct.

        Returns:
            bool: True if the deduction succeeded, False if balance is too low.
        """
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            return True
        return False  # Insufficient funds

    def __str__(self):
        return (f"[Account] {self.username} "
                f"({self.name}) - "
                f"Balance: ₱{self.wallet_balance:.2f}")
