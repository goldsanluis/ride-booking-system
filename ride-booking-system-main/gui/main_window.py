import tkinter as tk
from gui.booking_form import BookingForm
from gui.booking_list import BookingList
from gui.wallet_panel import WalletPanel
from services.booking_service import BookingService
from file_handler.file_manager import FileManager
from file_handler.account_manager import AccountManager

class MainWindow:
    def __init__(self, account):
        self.account = account
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1a1200")

        self.file_manager = FileManager()
        self.account_manager = AccountManager()
        self.service = BookingService(self.file_manager)

        self.setup_header()
        self.setup_tabs()

    def setup_header(self):
        header = tk.Frame(self.root, bg="#2d1f00", pady=10)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg="#2d1f00")
        title_frame.pack(fill="x", padx=20)

        tk.Label(
            title_frame,
            text="🚗 Ride Booking System",
            font=("Helvetica", 20, "bold"),
            bg="#2d1f00",
            fg="#FFD700"
        ).pack(side="left")

        # Add Refresh button
        tk.Button(
            title_frame,
            text="🔄 Refresh",
            font=("Helvetica", 10, "bold"),
            bg="#FFA500",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.refresh_bookings
        ).pack(side="right", padx=5)

        tk.Button(
            title_frame,
            text="Logout 🚪",
            font=("Helvetica", 10, "bold"),
            bg="#B8860B",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.logout
        ).pack(side="right")

        tk.Label(
            header,
            text=f"Welcome, {self.account.name}! 👑",
            font=("Helvetica", 11),
            bg="#2d1f00",
            fg="#FFA500"
        ).pack()

    def setup_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#1a1200")
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left side: Booking form + wallet
        left_frame = tk.Frame(tab_frame, bg="#1a1200")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.booking_form = BookingForm(
            left_frame,
            self.service,
            self.file_manager,
            self.refresh,
            self.account,
            self.account_manager
        )
        self.booking_form.frame.pack(fill="both", expand=True, pady=5)

        # Wallet panel
        self.wallet_panel = WalletPanel(left_frame, self.account, self.account_manager)
        self.wallet_panel.frame.pack(fill="x", pady=5)

        # Right side: Booking list
        self.booking_list = BookingList(tab_frame, self.service, self.account)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.booking_list.refresh()

    def refresh_bookings(self):
        # Reload bookings and wallet from file
        self.service = BookingService(self.file_manager)
        self.wallet_panel.refresh_balance()
        self.booking_list.service = self.service
        self.refresh()

    def logout(self):
        from tkinter import messagebox
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            from gui.login_window import LoginWindow
            from gui.main_window import MainWindow
            login = LoginWindow()
            account = login.run()
            if account:
                app = MainWindow(account)
                app.run()

    def run(self):
        self.root.mainloop()
