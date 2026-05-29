from gui.login_window import LoginWindow
from gui.main_window import MainWindow

def main():
    # Show login first
    login = LoginWindow()
    account = login.run()

    # Only open main window if login successful
    if account:
        app = MainWindow(account)
        app.run()

if __name__ == "__main__":
    main()