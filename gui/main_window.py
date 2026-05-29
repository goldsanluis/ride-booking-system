import tkinter as tk
from gui.booking_form import BookingForm
from gui.booking_list import BookingList
from services.booking_service import BookingService
from file_handler.file_manager import FileManager

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")

        # FileManager must be created FIRST before BookingService
        self.file_manager = FileManager()
        self.service = BookingService(self.file_manager)

        self.setup_header()
        self.setup_tabs()

    def setup_header(self):
        header = tk.Frame(self.root, bg="#16213e", pady=10)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚗 Ride Booking System",
            font=("Helvetica", 20, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack()

    def setup_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#1a1a2e")
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.booking_form = BookingForm(
            tab_frame,
            self.service,
            self.file_manager,
            self.refresh
        )
        self.booking_form.frame.pack(side="left", fill="both", expand=True, padx=5)

        self.booking_list = BookingList(tab_frame, self.service)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.booking_list.refresh()

    def run(self):
        self.root.mainloop()