import tkinter as tk
from gui.booking_form import BookingForm
from gui.booking_list import BookingList
from services.booking_service import BookingService
from file_handler.file_manager import FileManager

class MainWindow:
    def __init__(self, account):
        self.account = account
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")

        self.file_manager = FileManager()
        self.service = BookingService(self.file_manager)

        self.setup_header()
        self.setup_tabs()

    def setup_header(self):
        header = tk.Frame(self.root, bg="#16213e", pady=10)
        header.pack(fill="x")

        # Title and welcome
        title_frame = tk.Frame(header, bg="#16213e")
        title_frame.pack(fill="x", padx=20)

        tk.Label(
            title_frame,
            text="🚗 Ride Booking System",
            font=("Helvetica", 20, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(side="left")

        # Logout button
        tk.Button(
            title_frame,
            text="Logout 🚪",
            font=("Helvetica", 10, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.logout
        ).pack(side="right")

        tk.Label(
            header,
            text=f"Welcome, {self.account.name}! 👋",
            font=("Helvetica", 11),
            bg="#16213e",
            fg="white"
        ).pack()

    def setup_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#1a1a2e")
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.booking_form = BookingForm(
            tab_frame,
            self.service,
            self.file_manager,
            self.refresh,
            self.account
        )
        self.booking_form.frame.pack(side="left", fill="both", expand=True, padx=5)

        self.booking_list = BookingList(tab_frame, self.service, self.account)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.booking_list.refresh()

    def logout(self):
        from tkinter import messagebox
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            # Restart login
            from gui.login_window import LoginWindow
            from gui.main_window import MainWindow
            login = LoginWindow()
            account = login.run()
            if account:
                app = MainWindow(account)
                app.run()

    def run(self):
        self.root.mainloop()