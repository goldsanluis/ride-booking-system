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
    
    # --Constructor--
    def __init__(self, account_manager, driver_manager):
        self.account_manager = account_manager
        self.driver_manager = driver_manager
        
    # --Private Helpers Methods--
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
    
    # --Public Methods--
    def deduct_passenger_wallet(self, username, amount):
        """Deduct money from passenger wallet"""
        accounts = self.account_manager.load_accounts()
        for account in accounts:
            if account["username"] == username:
                if account["wallet_balance"] >= amount:
                    account["wallet_balance"] -= amount
                    self.account_manager.save_accounts(accounts)
                    return True, f"Deducted ₱{amount:.2f}"
                else:
                    return False, "Insufficient balance!"
        return False, "Account not found!"

    def add_driver_earnings(self, driver_id, amount):
        """Add money to driver wallet"""
        drivers = self.driver_manager.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                driver["wallet_balance"] = driver.get("wallet_balance", 0.0) + amount
                self.driver_manager.save_drivers(drivers)
                return True, f"Earned ₱{amount:.2f}"
        return False, "Driver not found!"

    def get_passenger_balance(self, username):
        """Get passenger wallet balance"""
        accounts = self.account_manager.load_accounts()
        for account in accounts:
            if account["username"] == username:
                return account.get("wallet_balance", 5000.0)
        return 0.0

    def get_driver_balance(self, driver_id):
        """Get driver wallet balance"""
        drivers = self.driver_manager.load_drivers()
        for driver in drivers:
            if driver["driver_id"] == driver_id:
                return driver.get("wallet_balance", 0.0)
        return 0.0

    def add_passenger_balance(self, username, amount):
        """Add money to passenger wallet (simulated top-up)"""
        accounts = self.account_manager.load_accounts()
        for account in accounts:
            if account["username"] == username:
                account["wallet_balance"] = account.get("wallet_balance", 5000.0) + amount
                self.account_manager.save_accounts(accounts)
                return True, f"Added ₱{amount:.2f}. New balance: ₱{account['wallet_balance']:.2f}"
        return False, "Account not found!"
