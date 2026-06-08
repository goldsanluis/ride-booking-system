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
    MIN_USERNAME_LEN = 3
    MIN_PASSWORD_LEN = 6

    def __init__(self, user_id, username, password, name, wallet_balance=None):
        self.user_id  = user_id
        self.username = username
        self.password = password
        self.name     = name

        if wallet_balance is None:
            wallet_balance = self.STARTING_BALANCE

        # Ensure numeric type safety even when wallet is loaded from JSON.
        self._wallet_balance = float(wallet_balance)

    # ── Wallet property ───────────────────────────────────────────────────────

    @property
    def wallet_balance(self):
        """Current wallet balance, always a float."""
        return self._wallet_balance

    @wallet_balance.setter
    def wallet_balance(self, value):
        """Prevent the wallet from going below zero via direct assignment."""
        self._wallet_balance = max(0.0, float(value))

    # ── Input validation (used by login/register) ─────────────────────────────

    @staticmethod
    def is_valid_username(username):
        """
        A username is valid when it is at least MIN_USERNAME_LEN characters
        long and contains no spaces.

        Args:
            username (str): The username to check.

        Returns:
            tuple[bool, str]: (True, "") on success, or (False, reason) on failure.
        """
        if not username or len(username.strip()) < Account.MIN_USERNAME_LEN:
            return False, f"Username must be at least {Account.MIN_USERNAME_LEN} characters."
        if " " in username:
            return False, "Username must not contain spaces."
        return True, ""

    @staticmethod
    def is_valid_password(password):
        """
        A password is valid when it is at least MIN_PASSWORD_LEN characters long.

        Args:
            password (str): The password to check.

        Returns:
            tuple[bool, str]: (True, "") on success, or (False, reason) on failure.
        """
        if not password or len(password) < Account.MIN_PASSWORD_LEN:
            return False, f"Password must be at least {Account.MIN_PASSWORD_LEN} characters."
        return True, ""

    # ── Wallet operations ─────────────────────────────────────────────────────

    def check_password(self, password):
        """Verify whether the supplied password matches this account's password."""
        return self.password == password

    def add_money(self, amount):
        """Top up the wallet by the given amount.

        Args:
            amount (float): Amount to add. Must be greater than 0.

        Raises:
            ValueError: If amount <= 0.

        Returns:
            str: Confirmation message with new balance.
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        self._wallet_balance += amount
        return f"Added ₱{amount:.2f}. New balance: ₱{self._wallet_balance:.2f}"

    def deduct_money(self, amount):
        """Deduct a fare payment from the wallet, if funds are sufficient.

        Args:
            amount (float): Amount to deduct. Must be greater than 0.

        Raises:
            ValueError: If amount <= 0.

        Returns:
            bool: True if deducted successfully, False if insufficient funds.
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if self._wallet_balance >= amount:
            self._wallet_balance -= amount
            return True
        return False  # Insufficient funds

    def get_balance(self):
        """Return the wallet balance rounded to 2 decimals."""
        return round(self._wallet_balance, 2)

    # ── String representations ────────────────────────────────────────────────

    def __str__(self):
        return (
            f"[Account] {self.username} "
            f"({self.name}) - "
            f"Balance: ₱{self._wallet_balance:.2f}"
        )

    def __repr__(self):
        return (
            f"Account(user_id={self.user_id!r}, username={self.username!r}, "
            f"name={self.name!r}, wallet_balance={self._wallet_balance!r})"
        )