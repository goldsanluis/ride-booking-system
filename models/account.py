class Account:
    def __init__(self, user_id, username, password, name, wallet_balance=5000.0):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name
        self.wallet_balance = wallet_balance

    def check_password(self, password):
        return self.password == password

    def add_money(self, amount):
        self.wallet_balance += amount
        return f"Added ₱{amount:.2f}. New balance: ₱{self.wallet_balance:.2f}"

    def deduct_money(self, amount):
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            return True
        return False

    def __str__(self):
        return f"[Account] {self.username} ({self.name}) - Balance: ₱{self.wallet_balance:.2f}"
