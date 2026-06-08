"""services/wallet_service.py
----------------------------
Watermark signature (hidden).

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

class WalletService:

    DEFAULT_PASSENGER_BALANCE = 5000.0
    DEFAULT_DRIVER_BALANCE = 0.0
    
    # -----Constructor-----
    def __init__(self, account_manager, driver_manager):
        self.account_manager = account_manager
        self.driver_manager = driver_manager
        
    # -----Protected Helpers Methods-----
    def _find_account(self, username: str):
        # load all accounts and return account_dict and accounts list if found, else None
        accounts = self.account_manager.load_accounts()
        for account in accounts:
            if accounts["username"] == username:
                return account, accounts
        return None, None
    
    def _find_driver(self, driver_id: str):
        # load all drivers and return driver_dict and drivers list if found, else None
        drivers = self.driver_manager.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                return driver, drivers
        return None, None
    
    @staticmethod
    # Validate amount is a positive number
    def _validate_amount(amount) -> tuple:
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number!"
        if amount <= 0:
            return False, "Amount must be greater than zero!"
        return True, ""
    
    # -----Public Methods-----
    def deduct_passenger_wallet(self, username: str, amount: float) -> tuple:
        # Deduct money from a passenger's wallet.
        valid, err = self._validate_amount(amount)
        if not valid:
            return False, err
        
        account, accounts = self._find_account(username)
        if account is None:
            return False, "Account not found!"
 
        balance = account.get("wallet_balance", self.DEFAULT_PASSENGER_BALANCE)
        if balance < amount:
            return False, f"Insufficient balance! You have ₱{balance:.2f}."
 
        account["wallet_balance"] = round(balance - amount, 2)
        self.account_manager.save_accounts(accounts)
        return True, f"Deducted ₱{amount:.2f}. New balance: ₱{account['wallet_balance']:.2f}"

    def add_passenger_balance(self, username: str, amount: float) -> tuple:
        # Add money to a passenger's wallet (simulated top-up).
        valid, err = self._validate_amount(amount)
        if not valid:
            return False, err
 
        account, accounts = self._find_account(username)
        if account is None:
            return False, "Account not found!"
 
        account["wallet_balance"] = round(
            account.get("wallet_balance", self.DEFAULT_PASSENGER_BALANCE) + amount, 2
        )
        self.account_manager.save_accounts(accounts)
        return True, f"Added ₱{amount:.2f}. New balance: ₱{account['wallet_balance']:.2f}"
 
    def get_passenger_balance(self, username: str) -> float:
        # Return a passenger's current wallet balance.
        account, _ = self._find_account(username)
        if account is None:
            return 0.0
        return account.get("wallet_balance", self.DEFAULT_PASSENGER_BALANCE)
 
    def add_driver_earnings(self, driver_id: str, amount: float) -> tuple:
        # Credit a driver's wallet with ride earnings.
        valid, err = self._validate_amount(amount)
        if not valid:
            return False, err
 
        driver, drivers = self._find_driver(driver_id)
        if driver is None:
            return False, "Driver not found!"
 
        driver["wallet_balance"] = round(
            driver.get("wallet_balance", self.DEFAULT_DRIVER_BALANCE) + amount, 2
        )
        self.driver_manager.save_drivers(drivers)
        return True, f"Earned ₱{amount:.2f}. New balance: ₱{driver['wallet_balance']:.2f}"
 
    def get_driver_balance(self, driver_id: str) -> float:
        # Return a driver's current wallet balance.
        driver, _ = self._find_driver(driver_id)
        if driver is None:
            return 0.0
        return driver.get("wallet_balance", self.DEFAULT_DRIVER_BALANCE)
