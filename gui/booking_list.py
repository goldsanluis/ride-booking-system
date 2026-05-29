import tkinter as tk
from tkinter import messagebox

# Gold Theme Colors
BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
BG_ENTRY    = "#3d2a00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
GOLD_LIGHT  = "#FFE55C"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"
GREEN       = "#4ecca3"
RED_CANCEL  = "#cc4400"

class BookingList:
    def __init__(self, parent, service, account):
        self.service = service
        self.account = account
        self.selected_booking_id = None
        self.card_frames = {}

        self.frame = tk.Frame(parent, bg=BG_DARK, padx=10, pady=10)

        tk.Label(
            self.frame,
            text="My Bookings",
            font=("Helvetica", 16, "bold"),
            bg=BG_DARK,
            fg=GOLD
        ).pack(pady=10)

        self.canvas = tk.Canvas(self.frame, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Buttons frame
        btn_frame = tk.Frame(self.frame, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=5)

        tk.Button(
            btn_frame,
            text="Receipt 🧾",
            font=("Helvetica", 10, "bold"),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=5,
            pady=5,
            cursor="hand2",
            command=self.show_receipt
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            btn_frame,
            text="Complete ✅",
            font=("Helvetica", 10, "bold"),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=5,
            pady=5,
            cursor="hand2",
            command=self.complete_booking
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            btn_frame,
            text="Rate ⭐",
            font=("Helvetica", 10, "bold"),
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=5,
            pady=5,
            cursor="hand2",
            command=self.rate_booking
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            btn_frame,
            text="Cancel ❌",
            font=("Helvetica", 10, "bold"),
            bg=RED_CANCEL,
            fg=TEXT_WHITE,
            relief="flat",
            padx=5,
            pady=5,
            cursor="hand2",
            command=self.cancel_booking
        ).pack(side="left", fill="x", expand=True, padx=2)

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

        bookings = self.service.get_user_bookings(self.account.name)

        if not bookings:
            tk.Label(
                self.inner_frame,
                text="No bookings yet!",
                font=("Helvetica", 12),
                bg=BG_DARK,
                fg=TEXT_GRAY
            ).pack(pady=20)
            return

        for booking in bookings:
            self.create_booking_card(booking)

    def create_booking_card(self, booking):
        if booking.status == "Active":
            card_color = "#2d1f00"
            border_color = GOLD
        elif booking.status == "Completed":
            card_color = "#1a2a00"
            border_color = GREEN
        else:
            card_color = "#2a2a2a"
            border_color = TEXT_GRAY

        border_frame = tk.Frame(
            self.inner_frame,
            bg=border_color,
            padx=2,
            pady=2
        )
        border_frame.pack(fill="x", padx=5, pady=5)

        card = tk.Frame(border_frame, bg=card_color, padx=10, pady=8, cursor="hand2")
        card.pack(fill="x")

        surge_text = f" 🚀 SURGE {booking.surge}x" if booking.surge > 1.0 else ""
        rating_text = f"⭐{booking.rating}" if booking.rating else "Not rated"

        labels = [
            (f"Booking #{booking.booking_id}{surge_text}", "Helvetica 11 bold", GOLD),
            (f"👤 {booking.user}", "Helvetica 10", TEXT_WHITE),
            (f"🚗 {booking.vehicle.name}", "Helvetica 10", TEXT_WHITE),
            (f"🧑‍✈️ Driver: {booking.driver.name} | {booking.driver.plate}", "Helvetica 10", TEXT_WHITE),
            (f"⭐ Driver Rating: {booking.driver.rating}", "Helvetica 10", TEXT_WHITE),
            (f"📍 {booking.start_location} → {booking.end_location}", "Helvetica 10", TEXT_WHITE),
            (f"📏 {booking.distance} km", "Helvetica 10", TEXT_WHITE),
            (f"💰 ₱{booking.total_cost:.2f}", "Helvetica 10 bold", GOLD),
            (f"📅 {booking.date}", "Helvetica 9", TEXT_GRAY),
            (f"● {booking.status}", "Helvetica 10 bold", GOLD_ACCENT if booking.status == "Active" else TEXT_GRAY),
            (f"Your Rating: {rating_text}", "Helvetica 10", GOLD_ACCENT if booking.rating else TEXT_GRAY),
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
                if booking.status == "Active":
                    frame.configure(bg=GOLD)
                elif booking.status == "Completed":
                    frame.configure(bg=GREEN)
                else:
                    frame.configure(bg=TEXT_GRAY)
        border_frame.configure(bg=GOLD_LIGHT)
        self.selected_booking_id = booking_id

    def get_selected(self):
        if not self.selected_booking_id:
            messagebox.showerror("Error", "Please select a booking first!")
            return None
        booking = self.service.find_booking_by_id(self.selected_booking_id)
        if not booking:
            messagebox.showerror("Error", "Booking not found!")
            return None
        return booking

    def show_receipt(self):
        booking = self.get_selected()
        if not booking:
            return

        receipt = tk.Toplevel()
        receipt.title(f"Receipt - Booking #{booking.booking_id}")
        receipt.geometry("350x470")
        receipt.configure(bg=BG_DARK)
        receipt.resizable(False, False)

        tk.Label(receipt, text="🧾 BOOKING RECEIPT",
                font=("Helvetica", 14, "bold"),
                bg=BG_DARK, fg=GOLD).pack(pady=10)

        tk.Label(receipt, text="─" * 40,
                bg=BG_DARK, fg=GOLD_DARK).pack()

        surge_text = f"(Surge {booking.surge}x applied)" if booking.surge > 1.0 else ""
        rating_text = f"⭐{booking.rating}" if booking.rating else "Not yet rated"

        details = [
            ("Booking ID", f"#{booking.booking_id}"),
            ("Passenger", booking.user),
            ("Vehicle", booking.vehicle.name),
            ("Driver", booking.driver.name),
            ("Plate No.", booking.driver.plate),
            ("From", booking.start_location),
            ("To", booking.end_location),
            ("Distance", f"{booking.distance} km"),
            ("Base Cost", f"₱{booking.vehicle.calculate_cost(booking.distance):.2f}"),
            ("Surge", surge_text if surge_text else "None"),
            ("Total Cost", f"₱{booking.total_cost:.2f}"),
            ("Date", booking.date),
            ("Status", booking.status),
            ("Your Rating", rating_text),
        ]

        for label, value in details:
            row = tk.Frame(receipt, bg=BG_CARD, padx=10, pady=3)
            row.pack(fill="x", padx=20, pady=1)
            tk.Label(row, text=label, font=("Helvetica", 10),
                    bg=BG_CARD, fg=TEXT_GRAY, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10, "bold"),
                    bg=BG_CARD, fg=GOLD, anchor="w").pack(side="left")

        tk.Button(receipt, text="Close",
                font=("Helvetica", 11, "bold"),
                bg=GOLD, fg=BG_DARK, relief="flat",
                cursor="hand2",
                command=receipt.destroy).pack(pady=15)

    def complete_booking(self):
        booking = self.get_selected()
        if not booking:
            return
        if booking.status != "Active":
            messagebox.showerror("Error", "Only active bookings can be completed!")
            return
        confirm = messagebox.askyesno("Confirm", f"Mark Booking #{booking.booking_id} as completed?")
        if confirm:
            result = self.service.complete_booking(self.selected_booking_id, self.account.name)
            self.service.file_manager.save_bookings(self.service.get_all_bookings())
            messagebox.showinfo("Result", result)
            self.refresh()

    def rate_booking(self):
        booking = self.get_selected()
        if not booking:
            return
        if booking.status != "Completed":
            messagebox.showerror("Error", "You can only rate completed bookings!")
            return
        if booking.rating:
            messagebox.showerror("Error", "You already rated this booking!")
            return

        rate_window = tk.Toplevel()
        rate_window.title("Rate your ride")
        rate_window.geometry("300x270")
        rate_window.configure(bg=BG_DARK)
        rate_window.resizable(False, False)

        tk.Label(rate_window, text="⭐ Rate Your Ride",
                font=("Helvetica", 14, "bold"),
                bg=BG_DARK, fg=GOLD).pack(pady=15)

        tk.Label(rate_window, text=f"Driver: {booking.driver.name}",
                font=("Helvetica", 11),
                bg=BG_DARK, fg=TEXT_WHITE).pack()

        tk.Label(rate_window, text="Select Rating:",
                font=("Helvetica", 11),
                bg=BG_DARK, fg=GOLD_ACCENT).pack(pady=10)

        rating_var = tk.IntVar(value=5)

        stars_frame = tk.Frame(rate_window, bg=BG_DARK)
        stars_frame.pack()

        for i in range(1, 6):
            tk.Radiobutton(
                stars_frame,
                text=f"{'⭐' * i}",
                variable=rating_var,
                value=i,
                bg=BG_DARK,
                fg=TEXT_WHITE,
                selectcolor=GOLD_DARK,
                activebackground=BG_DARK,
                activeforeground=GOLD,
                font=("Helvetica", 11)
            ).pack(anchor="w")

        def submit_rating():
            result = self.service.rate_booking(
                self.selected_booking_id,
                self.account.name,
                rating_var.get()
            )
            self.service.file_manager.save_bookings(self.service.get_all_bookings())
            messagebox.showinfo("Result", result)
            rate_window.destroy()
            self.refresh()

        tk.Button(rate_window, text="Submit Rating",
                font=("Helvetica", 11, "bold"),
                bg=GOLD, fg=BG_DARK, relief="flat",
                cursor="hand2",
                command=submit_rating).pack(pady=15)

    def cancel_booking(self):
        booking = self.get_selected()
        if not booking:
            return
        if booking.status != "Active":
            messagebox.showerror("Error", "Only active bookings can be cancelled!")
            return
        confirm = messagebox.askyesno("Confirm", f"Cancel Booking #{self.selected_booking_id}?")
        if confirm:
            result = self.service.cancel_booking(self.selected_booking_id, self.account.name)
            self.service.file_manager.save_bookings(self.service.get_all_bookings())
            messagebox.showinfo("Result", result)
            self.refresh()