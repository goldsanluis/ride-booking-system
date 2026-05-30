import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from services.promo_service import apply_promo, list_promos

BG_DARK     = "#2d1f00"
BG_FIELD    = "#3d2a00"
GOLD        = "#FFD700"
GOLD_ACCENT = "#FFA500"
GREEN       = "#4ecca3"
TEXT_WHITE  = "#FFFFFF"

class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account, account_manager):
        self.service          = service
        self.file_manager     = file_manager
        self.refresh_callback = refresh_callback
        self.account          = account
        self.account_manager  = account_manager
        self._discount        = 0.0
        self._promo_applied   = None

        self.frame = tk.Frame(parent, bg=BG_DARK, padx=10, pady=10)
        self._build()

    # ── build UI ─────────────────────────────────────────────────────────────
    def _build(self):
        tk.Label(self.frame, text="Book a Ride",
                 font=("Helvetica", 16, "bold"),
                 bg=BG_DARK, fg=GOLD).pack(pady=(10, 4))

        # Vehicle selector
        self._lbl("Vehicle Type:")
        self.vehicle_var = tk.StringVar(value="Car")
        vf = tk.Frame(self.frame, bg=BG_DARK); vf.pack(fill="x", pady=2)
        for v in ["Car", "Van", "Bike"]:
            tk.Radiobutton(vf, text=v, variable=self.vehicle_var, value=v,
                           bg=BG_DARK, fg=TEXT_WHITE, selectcolor="#B8860B",
                           activebackground=BG_DARK, activeforeground=GOLD,
                           font=("Helvetica", 11),
                           command=self._update_estimate).pack(side="left", padx=5)

        # Locations
        self._lbl("Start Location:")
        self.start_entry = self._entry()

        self._lbl("End Location:")
        self.end_entry = self._entry()

        # Distance + live estimator
        self._lbl("Distance (km):")
        dist_row = tk.Frame(self.frame, bg=BG_DARK); dist_row.pack(fill="x", pady=2)
        self.distance_entry = tk.Entry(dist_row, font=("Helvetica", 11),
                                       bg=BG_FIELD, fg=TEXT_WHITE,
                                       insertbackground=GOLD, relief="flat", bd=5)
        self.distance_entry.pack(side="left", fill="x", expand=True)
        self.distance_entry.bind("<KeyRelease>", lambda e: self._update_estimate())

        # ── Fare Estimator panel ──────────────────────────────────────────────
        est_frame = tk.Frame(self.frame, bg="#1a3300", padx=8, pady=6)
        est_frame.pack(fill="x", pady=(8, 0))
        tk.Label(est_frame, text="💡 Fare Estimator",
                 font=("Helvetica", 10, "bold"), bg="#1a3300", fg=GREEN).pack(anchor="w")
        self.estimate_label = tk.Label(est_frame, text="Enter distance to see estimate",
                                       font=("Helvetica", 10), bg="#1a3300", fg=TEXT_WHITE)
        self.estimate_label.pack(anchor="w")
        self.surge_label = tk.Label(est_frame, text="",
                                    font=("Helvetica", 9, "italic"), bg="#1a3300", fg=GOLD_ACCENT)
        self.surge_label.pack(anchor="w")

        # ── Passengers ───────────────────────────────────────────────────────
        self._lbl("Passengers:")
        pax_frame = tk.Frame(self.frame, bg=BG_DARK); pax_frame.pack(fill="x", pady=2)
        self.passengers_var = tk.IntVar(value=1)
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            tk.Radiobutton(pax_frame, text=str(n), variable=self.passengers_var, value=n,
                           bg=BG_DARK, fg=TEXT_WHITE, selectcolor="#B8860B",
                           activebackground=BG_DARK, activeforeground=GOLD,
                           font=("Helvetica", 10)).pack(side="left", padx=2)

        # ── Notes / Special Instructions ─────────────────────────────────────
        self._lbl("Notes / Special Instructions (optional):")
        self.notes_text = tk.Text(self.frame, font=("Helvetica", 10),
                                  bg=BG_FIELD, fg=TEXT_WHITE,
                                  insertbackground=GOLD, relief="flat", bd=5,
                                  height=3, wrap="word")
        self.notes_text.pack(fill="x", pady=2)

        # ── Promo code ────────────────────────────────────────────────────────
        promo_outer = tk.Frame(self.frame, bg=BG_FIELD, padx=8, pady=6)
        promo_outer.pack(fill="x", pady=(8, 0))
        promo_top = tk.Frame(promo_outer, bg=BG_FIELD); promo_top.pack(fill="x")
        tk.Label(promo_top, text="🎟️ Promo Code:",
                 font=("Helvetica", 10, "bold"), bg=BG_FIELD, fg=GOLD).pack(side="left")
        tk.Button(promo_top, text="View Promos", font=("Helvetica", 9),
                  bg="#B8860B", fg=TEXT_WHITE, relief="flat", padx=6, pady=2,
                  cursor="hand2", command=self._show_promos).pack(side="right")
        promo_row = tk.Frame(promo_outer, bg=BG_FIELD); promo_row.pack(fill="x", pady=4)
        self.promo_entry = tk.Entry(promo_row, font=("Helvetica", 11),
                                    bg="#2d1f00", fg=TEXT_WHITE,
                                    insertbackground=GOLD, relief="flat", bd=4)
        self.promo_entry.pack(side="left", fill="x", expand=True)
        tk.Button(promo_row, text="Apply", font=("Helvetica", 10, "bold"),
                  bg=GOLD, fg="#1a1200", relief="flat", padx=10,
                  cursor="hand2", command=self._apply_promo).pack(side="left", padx=(6, 0))
        self.promo_label = tk.Label(promo_outer, text="", font=("Helvetica", 9),
                                    bg=BG_FIELD, fg=GREEN)
        self.promo_label.pack(anchor="w")

        # ── Pricing reference ─────────────────────────────────────────────────
        pf = tk.Frame(self.frame, bg="#3d2a00", padx=8, pady=6)
        pf.pack(fill="x", pady=8)
        tk.Label(pf, text="💰 Pricing Info",
                 font=("Helvetica", 10, "bold"), bg="#3d2a00", fg=GOLD).pack(anchor="w")
        for t in ["🚗 Car: ₱40 base + ₱14/km (cap 4)",
                  "🚐 Van: ₱80 base + ₱20/km (cap 10)",
                  "🏍️ Bike: ₱20 base + ₱8/km (cap 1)",
                  "🚀 Surge: 1.5× (7–9 AM, 5–8 PM)"]:
            tk.Label(pf, text=t, font=("Helvetica", 9),
                     bg="#3d2a00", fg=GOLD_ACCENT).pack(anchor="w")

        # Wallet balance
        self.wallet_label = tk.Label(
            self.frame,
            text=f"💳 Wallet Balance: ₱{self.account.wallet_balance:.2f}",
            font=("Helvetica", 11, "bold"), bg=BG_DARK, fg=GREEN)
        self.wallet_label.pack(pady=5)

        # Book button
        tk.Button(self.frame, text="Book Ride 🚗",
                  font=("Helvetica", 12, "bold"),
                  bg=GOLD, fg="#1a1200", relief="flat",
                  padx=10, pady=8, cursor="hand2",
                  command=self.book_ride).pack(pady=10, fill="x")

    # ── helpers ───────────────────────────────────────────────────────────────
    def _lbl(self, text):
        tk.Label(self.frame, text=text, font=("Helvetica", 11),
                 bg=BG_DARK, fg=GOLD_ACCENT).pack(anchor="w", pady=2)

    def _entry(self):
        e = tk.Entry(self.frame, font=("Helvetica", 11),
                     bg=BG_FIELD, fg=TEXT_WHITE,
                     insertbackground=GOLD, relief="flat", bd=5)
        e.pack(fill="x", pady=2)
        return e

    def _get_base_fare(self, vehicle_type, distance):
        from models.car import Car; from models.van import Van; from models.bike import Bike
        tmp = {"Car": Car(0), "Van": Van(0), "Bike": Bike(0)}.get(vehicle_type)
        return tmp.calculate_cost(distance) if tmp else 0.0

    def _current_surge(self):
        h = datetime.now().hour
        return 1.5 if (7 <= h <= 9) or (17 <= h <= 20) else 1.0

    def _update_estimate(self):
        try:
            dist = float(self.distance_entry.get())
            if dist <= 0:
                raise ValueError
        except ValueError:
            self.estimate_label.config(text="Enter distance to see estimate")
            self.surge_label.config(text="")
            return

        vehicle = self.vehicle_var.get()
        base    = self._get_base_fare(vehicle, dist)
        surge   = self._current_surge()
        gross   = base * surge
        net     = max(0.0, gross - self._discount)

        surge_text = f"🚀 Surge ×{surge} applied (+{int((surge-1)*100)}%)" if surge > 1.0 else "No surge right now ✅"
        if self._discount > 0:
            self.estimate_label.config(
                text=f"Estimated Fare: ₱{gross:.2f} − ₱{self._discount:.2f} promo = ₱{net:.2f}")
        else:
            self.estimate_label.config(text=f"Estimated Fare: ₱{net:.2f}")
        self.surge_label.config(text=surge_text)

    def _apply_promo(self):
        code = self.promo_entry.get().strip()
        try:
            dist = float(self.distance_entry.get())
        except ValueError:
            dist = 0.0
        vehicle = self.vehicle_var.get()
        base    = self._get_base_fare(vehicle, dist)
        surge   = self._current_surge()
        fare    = base * surge

        discount, desc, err = apply_promo(code, fare)
        if err:
            self.promo_label.config(text=f"❌ {err}", fg="#FF6B6B")
            self._discount      = 0.0
            self._promo_applied = None
        else:
            self._discount      = discount
            self._promo_applied = code.upper()
            self.promo_label.config(
                text=f"✅ {code.upper()} applied: {desc} (−₱{discount:.2f})", fg=GREEN)
        self._update_estimate()

    def _show_promos(self):
        messagebox.showinfo("Available Promo Codes", list_promos())

    # ── booking action ────────────────────────────────────────────────────────
    def book_ride(self):
        vehicle_type = self.vehicle_var.get()
        start        = self.start_entry.get().strip()
        end          = self.end_entry.get().strip()
        passengers   = self.passengers_var.get()
        notes        = self.notes_text.get("1.0", tk.END).strip()

        try:
            distance = float(self.distance_entry.get())
            if distance <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid distance (> 0)!")
            return

        if not all([start, end]):
            messagebox.showerror("Error", "Please fill in start and end locations!")
            return

        # Capacity guard
        caps = {"Car": 4, "Van": 10, "Bike": 1}
        if passengers > caps.get(vehicle_type, 99):
            messagebox.showerror(
                "Over Capacity",
                f"{vehicle_type} holds max {caps[vehicle_type]} passenger(s).\n"
                f"You selected {passengers}. Please choose a larger vehicle or fewer passengers."
            )
            return

        base         = self._get_base_fare(vehicle_type, distance)
        surge        = self._current_surge()
        gross        = base * surge
        discount     = self._discount
        promo_code   = self._promo_applied
        est_cost     = max(0.0, gross - discount)

        if self.account.wallet_balance < est_cost:
            messagebox.showerror(
                "Insufficient Balance",
                f"Wallet: ₱{self.account.wallet_balance:.2f}\n"
                f"Required: ₱{est_cost:.2f}\n"
                "Please top up your wallet first!"
            )
            return

        # Build confirmation message
        surge_txt  = f"\n🚀 Surge ×{surge}" if surge > 1.0 else ""
        promo_txt  = f"\n🎟️ Promo {promo_code}: −₱{discount:.2f}" if promo_code else ""
        pax_txt    = f"\n👥 Passengers: {passengers}" if passengers > 1 else ""
        notes_txt  = f"\n📝 Notes: {notes[:60]}" if notes else ""

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Vehicle: {vehicle_type}\n"
            f"From: {start} → To: {end}\n"
            f"Distance: {distance} km{pax_txt}{surge_txt}{promo_txt}\n"
            f"Total Cost: ₱{est_cost:.2f}{notes_txt}\n\n"
            "Confirm booking?"
        )
        if not confirm:
            return

        # Deduct wallet
        self.account.wallet_balance -= est_cost
        self.account_manager.update_account(self.account)

        # Create booking
        booking = self.service.book_ride(
            self.account.name, vehicle_type, start, end, distance,
            passengers=passengers, notes=notes,
            promo_code=promo_code, discount=discount
        )
        self.file_manager.save_bookings(self.service.get_all_bookings())

        # Update wallet label
        self.wallet_label.config(text=f"💳 Wallet Balance: ₱{self.account.wallet_balance:.2f}")

        surge_msg  = f"\n🚀 Surge ×{booking.surge}" if booking.surge > 1.0 else ""
        promo_msg  = f"\n🎟️ Discount: −₱{discount:.2f}" if promo_code else ""
        messagebox.showinfo(
            "Booking Confirmed! 🎉",
            f"Ride booked successfully!\n"
            f"Driver: {booking.driver.name}\n"
            f"Plate: {booking.driver.plate}\n"
            f"Total Cost: ₱{booking.total_cost:.2f}{surge_msg}{promo_msg}\n"
            f"Remaining Balance: ₱{self.account.wallet_balance:.2f}"
        )

        # Reset form
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
        self.promo_entry.delete(0, tk.END)
        self.promo_label.config(text="")
        self.passengers_var.set(1)
        self._discount      = 0.0
        self._promo_applied = None
        self.estimate_label.config(text="Enter distance to see estimate")
        self.surge_label.config(text="")
        self.refresh_callback()
