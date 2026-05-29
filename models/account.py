class Account:
    def __init__(self, user_id, username, password, name):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name

    def check_password(self, password):
        return self.password == password

    def __str__(self):
        return f"[Account] {self.username} ({self.name})"