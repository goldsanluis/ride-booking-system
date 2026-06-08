"""
models/account.py
-----------------
Represents a registered passenger account.
Encapsulates user credentials and wallet balance in one object.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""


class Account:
    """A passenger account with login credentials and an in-app wallet."""

    STARTING_BALANCE = 5000.0

    def __init__(self, user_id, username, password, name, wallet_balance=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name

        if wallet_balance is None:
            wallet_balance = self.STARTING_BALANCE

        # Ensure numeric type safety even when wallet is loaded from JSON.
        self.wallet_balance = float(wallet_balance)

    def check_password(self, password):
        """Verify whether the supplied password matches this account's password."""
        return self.password == password

    def add_money(self, amount):
        """Top up the wallet by the given amount.

        Raises:
            ValueError: If amount <= 0
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")

        self.wallet_balance += amount
        return f"Added ₱{amount:.2f}. New balance: ₱{self.wallet_balance:.2f}"

    def deduct_money(self, amount):
        """Deduct a fare payment from the wallet, if funds are sufficient.

        Raises:
            ValueError: If amount <= 0
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")

        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            return True
        return False  # Insufficient funds

    def get_balance(self):
        """Return the wallet balance rounded to 2 decimals."""
        return round(self.wallet_balance, 2)

    def __str__(self):
        return (
            f"[Account] {self.username} "
            f"({self.name}) - "
            f"Balance: ₱{self.wallet_balance:.2f}"
        )

    def __repr__(self):
        return (
            f"Account(user_id={self.user_id!r}, username={self.username!r}, "
            f"name={self.name!r}, wallet_balance={self.wallet_balance!r})"
        )

