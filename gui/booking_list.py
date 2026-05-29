import tkinter as tk
from tkinter import messagebox

class BookingList:
    def __init__(self, parent, service, account):
        self.service = service
        self.account = account
        self.selected_booking_id = None
        self.card_frames = {}

        self.frame = tk.Frame(parent, bg="#16213e", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="My Bookings",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(pady=10)

        self.canvas = tk.Canvas(self.frame, bg="#16213e", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="#16213e")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        tk.Button(
            self.frame,
            text="Cancel Booking ❌",
            font=("Helvetica", 12, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.cancel_booking
        ).pack(pady=10, fill="x")

        self.refresh()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def refresh(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.selected_booking_id = None
        self.card_frames = {}

        # Only show current user's bookings
        bookings = self.service.get_user_bookings(self.account.name)

        if not bookings:
            tk.Label(
                self.inner_frame,
                text="No bookings yet!",
                font=("Helvetica", 12),
                bg="#16213e",
                fg="gray"
            ).pack(pady=20)
            return

        for booking in bookings:
            self.create_booking_card(booking)

    def create_booking_card(self, booking):
        card_color = "#0f3460" if booking.status == "Active" else "#2d2d2d"
        border_color = "#e94560" if booking.status == "Active" else "gray"

        border_frame = tk.Frame(
            self.inner_frame,
            bg=border_color,
            padx=2,
            pady=2
        )
        border_frame.pack(fill="x", padx=5, pady=5)

        card = tk.Frame(border_frame, bg=card_color, padx=10, pady=8, cursor="hand2")
        card.pack(fill="x")

        labels = [
            (f"Booking #{booking.booking_id}", "Helvetica 11 bold", "#e94560"),
            (f"👤 {booking.user}", "Helvetica 10", "white"),
            (f"🚗 {booking.vehicle.name}", "Helvetica 10", "white"),
            (f"📍 {booking.start_location} → {booking.end_location}", "Helvetica 10", "white"),
            (f"📏 {booking.distance} km", "Helvetica 10", "white"),
            (f"💰 ₱{booking.total_cost:.2f}", "Helvetica 10 bold", "#4ecca3"),
            (f"📅 {booking.date}", "Helvetica 9", "gray"),
            (f"● {booking.status}", "Helvetica 10 bold", "#4ecca3" if booking.status == "Active" else "gray"),
        ]

        for text, font, color in labels:
            lbl = tk.Label(card, text=text, font=font, bg=card_color, fg=color)
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>", lambda e, bid=booking.booking_id, bf=border_frame: self.select_booking(bid, bf))

        card.bind("<Button-1>", lambda e, bid=booking.booking_id, bf=border_frame: self.select_booking(bid, bf))
        border_frame.bind("<Button-1>", lambda e, bid=booking.booking_id, bf=border_frame: self.select_booking(bid, bf))

        self.card_frames[booking.booking_id] = border_frame

    def select_booking(self, booking_id, border_frame):
        for bid, frame in self.card_frames.items():
            booking = self.service.find_booking_by_id(bid)
            if booking:
                frame.configure(bg="#e94560" if booking.status == "Active" else "gray")
        border_frame.configure(bg="white")
        self.selected_booking_id = booking_id

    def cancel_booking(self):
        if not self.selected_booking_id:
            messagebox.showerror("Error", "Please select a booking first!")
            return

        booking = self.service.find_booking_by_id(self.selected_booking_id)
        if not booking:
            messagebox.showerror("Error", "Booking not found!")
            return

        if booking.status == "Cancelled":
            messagebox.showerror("Error", "This booking is already cancelled!")
            return

        confirm = messagebox.askyesno("Confirm", f"Cancel Booking #{self.selected_booking_id}?")
        if confirm:
            result = self.service.cancel_booking(self.selected_booking_id, self.account.name)
            self.service.file_manager.save_bookings(self.service.get_all_bookings())
            messagebox.showinfo("Result", result)
            self.refresh()