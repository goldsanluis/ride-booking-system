"""gui/booking_form.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

from services.promo_service import apply_promo, list_promos

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_APP      = "#1a0000"   # Deep dark maroon background
BG_SURFACE  = "#800000"   # Maroon card surface
BG_FIELD    = "#6b0000"   # Input field background
MAROON      = "#800000"   # PUP Maroon
MAROON_LT   = "#990000"   # Lighter maroon for hover
GOLD        = "#FFD700"   # PUP Gold
GOLD_DIM    = "#FFC200"   # Slightly dimmer gold
TEXT_WHITE  = "#FFFFFF"   # White text
TEXT_MUTED  = "#FFEECC"   # Warm muted white
RED_ERR     = "#FF6B6B"   # Error red
DIVIDER     = "#990000"   # Divider line


class BookingForm:
    def __init__(self, parent, service, file_manager, refresh_callback, account, account_manager):
        self.service          = service
        self.file_manager     = file_manager
        self.refresh_callback = refresh_callback
        self.account          = account
        self.account_manager  = account_manager
        self._discount        = 0.0
        self._promo_applied   = None
        self._scheduled_time  = None

        self.frame = tk.Frame(parent, bg=BG_APP, padx=10, pady=10)
        self._build()

    def _build(self):
        tk.Label(
            self.frame,
            text="Book a Ride",
            font=("Helvetica", 16, "bold"),
            bg=BG_APP,
            fg=GOLD,
        ).pack(pady=(10, 4))

        tk.Frame(self.frame, bg=GOLD, height=2).pack(fill="x", pady=(0, 8))

        fav_outer = tk.Frame(self.frame, bg=BG_SURFACE, padx=8, pady=6)
        fav_outer.pack(fill="x", pady=(0, 6))
        fav_top = tk.Frame(fav_outer, bg=BG_SURFACE)
        fav_top.pack(fill="x")
        tk.Label(
            fav_top,
            text="⭐ Favorite Routes",
            font=("Helvetica", 10, "bold"),
            bg=BG_SURFACE,
            fg=GOLD,
        ).pack(side="left")
        tk.Button(
            fav_top,
            text="Save Current Route",
            font=("Helvetica", 9),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self._save_favorite,
        ).pack(side="right")

        self.fav_var = tk.StringVar(value="— select a favorite —")
        self.fav_menu_btn = tk.OptionMenu(
            fav_outer,
            self.fav_var,
            "— select a favorite —",
            command=self._load_favorite,
        )
        self.fav_menu_btn.config(
            font=("Helvetica", 9),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            activebackground=MAROON_LT,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.fav_menu_btn["menu"].config(bg=BG_FIELD, fg=TEXT_WHITE, font=("Helvetica", 9))
        self.fav_menu_btn.pack(fill="x", pady=(4, 0))
        self._refresh_favorites_menu()

        self._lbl("Vehicle Type:")
        self.vehicle_var = tk.StringVar(value="Car")
        vf = tk.Frame(self.frame, bg=BG_APP)
        vf.pack(fill="x", pady=2)
        for v in ["Car", "Van", "Bike"]:
            tk.Radiobutton(
                vf,
                text=v,
                variable=self.vehicle_var,
                value=v,
                bg=BG_APP,
                fg=TEXT_WHITE,
                selectcolor=MAROON_LT,
                activebackground=BG_APP,
                activeforeground=GOLD,
                font=("Helvetica", 11),
                command=self._update_estimate,
            ).pack(side="left", padx=5)

        self._lbl("Start Location:")
        self.start_entry = self._entry()

        self._lbl("End Location:")
        self.end_entry = self._entry()

        self._lbl("Distance (km):")
        dist_row = tk.Frame(self.frame, bg=BG_APP)
        dist_row.pack(fill="x", pady=2)
        self.distance_entry = tk.Entry(
            dist_row,
            font=("Helvetica", 11),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5,
        )
        self.distance_entry.pack(side="left", fill="x", expand=True)
        self.distance_entry.bind("<KeyRelease>", lambda e: self._update_estimate())

        est_frame = tk.Frame(self.frame, bg=MAROON_LT, padx=8, pady=6)
        est_frame.pack(fill="x", pady=(8, 0))
        tk.Label(
            est_frame,
            text="💡 Fare Estimator",
            font=("Helvetica", 10, "bold"),
            bg=MAROON_LT,
            fg=GOLD,
        ).pack(anchor="w")
        self.estimate_label = tk.Label(
            est_frame,
            text="Enter distance to see estimate",
            font=("Helvetica", 10),
            bg=MAROON_LT,
            fg=TEXT_WHITE,
        )
        self.estimate_label.pack(anchor="w")
        self.surge_label = tk.Label(
            est_frame, text="", font=("Helvetica", 9, "italic"), bg=MAROON_LT, fg=GOLD_DIM
        )
        self.surge_label.pack(anchor="w")

        self._lbl("Passengers:")
        pax_frame = tk.Frame(self.frame, bg=BG_APP)
        pax_frame.pack(fill="x", pady=2)
        self.passengers_var = tk.IntVar(value=1)
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            tk.Radiobutton(
                pax_frame,
                text=str(n),
                variable=self.passengers_var,
                value=n,
                bg=BG_APP,
                fg=TEXT_WHITE,
                selectcolor=MAROON_LT,
                activebackground=BG_APP,
                activeforeground=GOLD,
                font=("Helvetica", 10),
            ).pack(side="left", padx=2)

        self._lbl("Notes / Special Instructions (optional):")
        self.notes_text = tk.Text(
            self.frame,
            font=("Helvetica", 10),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5,
            height=3,
            wrap="word",
        )
        self.notes_text.pack(fill="x", pady=2)

        promo_outer = tk.Frame(self.frame, bg=BG_SURFACE, padx=8, pady=6)
        promo_outer.pack(fill="x", pady=(8, 0))
        promo_top = tk.Frame(promo_outer, bg=BG_SURFACE)
        promo_top.pack(fill="x")
        tk.Label(
            promo_top,
            text="🎟️ Promo Code:",
            font=("Helvetica", 10, "bold"),
            bg=BG_SURFACE,
            fg=GOLD,
        ).pack(side="left")
        tk.Button(
            promo_top,
            text="View Promos",
            font=("Helvetica", 9),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self._show_promos,
        ).pack(side="right")

        promo_row = tk.Frame(promo_outer, bg=BG_SURFACE)
        promo_row.pack(fill="x", pady=4)
        self.promo_entry = tk.Entry(
            promo_row,
            font=("Helvetica", 11),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=4,
        )
        self.promo_entry.pack(side="left", fill="x", expand=True)
        tk.Button(
            promo_row,
            text="Apply",
            font=("Helvetica", 10, "bold"),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=10,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self._apply_promo,
        ).pack(side="left", padx=(6, 0))
        self.promo_label = tk.Label(promo_outer, text="", font=("Helvetica", 9), bg=BG_SURFACE, fg=GOLD_DIM)
        self.promo_label.pack(anchor="w")

        sched_outer = tk.Frame(self.frame, bg=MAROON, padx=8, pady=6)
        sched_outer.pack(fill="x", pady=(8, 0))
        sched_top = tk.Frame(sched_outer, bg=MAROON)
        sched_top.pack(fill="x")
        tk.Label(
            sched_top,
            text="🗓️ Schedule Ride (optional)",
            font=("Helvetica", 10, "bold"),
            bg=MAROON,
            fg=GOLD,
        ).pack(side="left")
        tk.Button(
            sched_top,
            text="Clear",
            font=("Helvetica", 9),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            relief="flat",
            padx=6,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self._clear_schedule,
        ).pack(side="right")

        sched_row = tk.Frame(sched_outer, bg=MAROON)
        sched_row.pack(fill="x", pady=4)
        tk.Label(
            sched_row,
            text="Date (YYYY-MM-DD):",
            font=("Helvetica", 9),
            bg=MAROON,
            fg=TEXT_MUTED,
        ).pack(side="left")
        self.sched_date = tk.Entry(
            sched_row,
            font=("Helvetica", 10),
            width=13,
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=4,
        )
        self.sched_date.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.sched_date.pack(side="left", padx=(4, 10))

        tk.Label(
            sched_row,
            text="Time (HH:MM):",
            font=("Helvetica", 9),
            bg=MAROON,
            fg=TEXT_MUTED,
        ).pack(side="left")
        self.sched_time = tk.Entry(
            sched_row,
            font=("Helvetica", 10),
            width=7,
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=4,
        )
        self.sched_time.insert(0, "08:00")
        self.sched_time.pack(side="left", padx=(4, 0))

        self.sched_enable = tk.BooleanVar(value=False)
        tk.Checkbutton(
            sched_outer,
            text="Enable scheduled booking",
            variable=self.sched_enable,
            bg=MAROON,
            fg=TEXT_WHITE,
            selectcolor=BG_FIELD,
            activebackground=MAROON,
            activeforeground=GOLD,
            font=("Helvetica", 9),
        ).pack(anchor="w")

        self.sched_status = tk.Label(sched_outer, text="", font=("Helvetica", 9, "italic"), bg=MAROON, fg=GOLD_DIM)
        self.sched_status.pack(anchor="w")

        pf = tk.Frame(self.frame, bg=BG_SURFACE, padx=8, pady=6)
        pf.pack(fill="x", pady=8)
        tk.Label(pf, text="💰 Pricing Info", font=("Helvetica", 10, "bold"), bg=BG_SURFACE, fg=GOLD).pack(anchor="w")
        for t in [
            "🚗 Car: P40 base + P14/km (cap 4)",
            "🚐 Van: P80 base + P20/km (cap 10)",
            "🏍️ Bike: P20 base + P8/km (cap 1)",
            "🚀 Surge: 1.5x (7-9 AM, 5-8 PM)",
        ]:
            tk.Label(pf, text=t, font=("Helvetica", 9), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w")

        # Payment method selector
        pm_frame = tk.Frame(self.frame, bg=MAROON, padx=8, pady=6)
        pm_frame.pack(fill="x", pady=(8, 0))
        pm_top = tk.Frame(pm_frame, bg=MAROON)
        pm_top.pack(fill="x")
        tk.Label(pm_top, text="💳 Payment Method:", font=("Helvetica", 10, "bold"), bg=MAROON, fg=GOLD).pack(
            side="left"
        )

        from services.payment_service import PaymentMethodService
        ps = PaymentMethodService()

        methods = ps.get_methods(self.account.username)
        self.payment_var = tk.StringVar()
        default_m = ps.get_default(self.account.username)
        self.payment_var.set(default_m.get("label", "Ride Wallet"))
        pm_menu = tk.OptionMenu(pm_frame, self.payment_var, *[m["label"] for m in methods])
        pm_menu.config(font=("Helvetica", 9), bg=BG_FIELD, fg=TEXT_WHITE, relief="flat", bd=0, highlightthickness=0,
                       activebackground=MAROON_LT)
        pm_menu["menu"].config(bg=BG_FIELD, fg=TEXT_WHITE, font=("Helvetica", 9))
        pm_menu.pack(fill="x", pady=4)

        self.wallet_label = tk.Label(
            self.frame,
            text=f"💳 Wallet Balance: P{self.account.wallet_balance:.2f}",
            font=("Helvetica", 11, "bold"),
            bg=BG_APP,
            fg=GOLD,
        )
        self.wallet_label.pack(pady=5)

        tk.Frame(self.frame, bg=GOLD, height=2).pack(fill="x", pady=(4, 0))
        tk.Button(
            self.frame,
            text="Book Ride 🚗",
            font=("Helvetica", 12, "bold"),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=10,
            pady=10,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self.book_ride,
        ).pack(pady=10, fill="x")

    def _lbl(self, text):
        tk.Label(self.frame, text=text, font=("Helvetica", 11), bg=BG_APP, fg=GOLD_DIM).pack(anchor="w", pady=2)

    def _entry(self):
        e = tk.Entry(self.frame, font=("Helvetica", 11), bg=BG_FIELD, fg=TEXT_WHITE, insertbackground=GOLD, relief="flat", bd=5)
        e.pack(fill="x", pady=2)
        return e

    def _get_base_fare(self, vehicle_type, distance):
        from models.car import Car
        from models.van import Van
        from models.bike import Bike

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
        base = self._get_base_fare(vehicle, dist)
        surge = self._current_surge()
        gross = base * surge
        net = max(0.0, gross - self._discount)

        surge_text = (
            f"🚀 Surge x{surge} applied (+{int((surge - 1) * 100)}%)" if surge > 1.0 else "No surge right now ✅"
        )
        if self._discount > 0:
            self.estimate_label.config(
                text=f"Estimated Fare: P{gross:.2f} - P{self._discount:.2f} promo = P{net:.2f}"
            )
        else:
            self.estimate_label.config(text=f"Estimated Fare: P{net:.2f}")
        self.surge_label.config(text=surge_text)

    def _apply_promo(self):
        code = self.promo_entry.get().strip()
        try:
            dist = float(self.distance_entry.get())
        except ValueError:
            dist = 0.0
        vehicle = self.vehicle_var.get()
        base = self._get_base_fare(vehicle, dist)
        surge = self._current_surge()
        fare = base * surge

        discount, desc, err = apply_promo(code, fare)
        if err:
            self.promo_label.config(text=f"❌ {err}", fg=RED_ERR)
            self._discount = 0.0
            self._promo_applied = None
        else:
            self._discount = discount
            self._promo_applied = code.upper()
            self.promo_label.config(text=f"✅ {code.upper()} applied: {desc} (-P{discount:.2f})", fg=GOLD)
        self._update_estimate()

    def _show_promos(self):
        messagebox.showinfo("Available Promo Codes", list_promos())

    def _parse_scheduled_time(self):
        if not self.sched_enable.get():
            return None
        date_str = self.sched_date.get().strip()
        time_str = self.sched_time.get().strip()
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        if dt <= datetime.now():
            raise ValueError("Scheduled time must be in the future")
        return dt.strftime("%Y-%m-%d %H:%M")

    def _clear_schedule(self):
        self.sched_enable.set(False)
        self.sched_status.config(text="")

    def _refresh_favorites_menu(self):
        favs = self.file_manager.load_favorites(self.account.username)
        menu = self.fav_menu_btn["menu"]
        menu.delete(0, "end")
        menu.add_command(label="— select a favorite —", command=lambda: self.fav_var.set("— select a favorite —"))
        if not favs:
            menu.add_command(label="(no favorites saved yet)", state="disabled")
            return
        for i, fav in enumerate(favs):
            label = f"{fav['name']}  ({fav['start']} to {fav['end']})"
            menu.add_command(label=label, command=lambda f=fav: self._load_favorite(f))
        menu.add_separator()
        for i, fav in enumerate(favs):
            menu.add_command(label=f"🗑 Delete: {fav['name']}", command=lambda idx=i: self._delete_favorite(idx))

    def _load_favorite(self, fav_or_str):
        if isinstance(fav_or_str, str):
            return
        fav = fav_or_str
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, fav["start"])
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, fav["end"])
        self.distance_entry.delete(0, tk.END)
        if fav.get("distance"):
            self.distance_entry.insert(0, str(fav["distance"]))
        if fav.get("vehicle") in ("Car", "Van", "Bike"):
            self.vehicle_var.set(fav["vehicle"])
        self._update_estimate()

    def _save_favorite(self):
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not start or not end:
            messagebox.showerror("Error", "Fill in start and end locations first.")
            return
        try:
            dist = float(self.distance_entry.get())
        except ValueError:
            dist = 0.0

        name_win = tk.Toplevel()
        name_win.title("Save Favorite Route")
        name_win.configure(bg=BG_APP)
        name_win.resizable(False, False)
        name_win.grab_set()

        tk.Label(name_win, text="Name this route:", font=("Helvetica", 11), bg=BG_APP, fg=GOLD).pack(padx=20, pady=(16, 4))
        name_entry = tk.Entry(
            name_win,
            font=("Helvetica", 11),
            bg=BG_FIELD,
            fg=TEXT_WHITE,
            insertbackground=GOLD,
            relief="flat",
            bd=5,
            width=28,
        )
        default_name = f"{start[:12]} to {end[:12]}"
        name_entry.insert(0, default_name)
        name_entry.pack(padx=20, pady=4)

        def do_save():
            name = name_entry.get().strip() or default_name
            route = {
                "name": name,
                "start": start,
                "end": end,
                "distance": dist,
                "vehicle": self.vehicle_var.get(),
            }
            saved = self.file_manager.save_favorite(self.account.username, route)
            name_win.destroy()
            if saved:
                messagebox.showinfo("Saved!", f"✅ '{name}' saved to favorites!")
            else:
                messagebox.showinfo("Already Saved", "This route is already in your favorites.")
            self._refresh_favorites_menu()

        tk.Button(
            name_win,
            text="Save",
            font=("Helvetica", 11, "bold"),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=do_save,
        ).pack(pady=12)

    def _delete_favorite(self, index):
        self.file_manager.delete_favorite(self.account.username, index)
        self._refresh_favorites_menu()
        messagebox.showinfo("Deleted", "Favorite route removed.")

    def book_ride(self):
        vehicle_type = self.vehicle_var.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        try:
            passengers = int(self.passengers_var.get())
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Passengers must be a valid number.")
            return

        caps = {"Car": 4, "Van": 10, "Bike": 1}
        if not start or not end:
            messagebox.showerror("Error", "Please fill in start and end locations.")
            return

        if passengers < 1:
            messagebox.showerror("Error", "Passengers must be at least 1.")
            return

        if passengers > caps.get(vehicle_type, 99):
            messagebox.showerror(
                "Over Capacity",
                f"{vehicle_type} holds max {caps.get(vehicle_type, '—')} passenger(s).\n"
                f"You selected {passengers}. Please choose a larger vehicle or fewer passengers.",
            )
            return

        try:
            raw_dist = self.distance_entry.get().strip()
            if raw_dist == "":
                raise ValueError("Distance is required")
            distance = float(raw_dist)
            if distance <= 0:
                raise ValueError("Distance must be greater than 0")
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Please enter a valid distance (greater than 0 km).")
            return

        scheduled_time = None
        if self.sched_enable.get():
            try:
                scheduled_time = self._parse_scheduled_time()
            except Exception as e:
                messagebox.showerror("Schedule Error", str(e) if str(e) else "Invalid schedule input.")
                return

        base = self._get_base_fare(vehicle_type, distance)
        surge = self._current_surge()
        try:
            gross = float(base) * float(surge)
        except Exception:
            messagebox.showerror("Error", "Could not compute fare. Please check your inputs.")
            return

        discount = self._discount
        try:
            discount = float(discount)
        except (TypeError, ValueError):
            discount = 0.0

        if discount < 0:
            messagebox.showerror("Error", "Invalid discount amount.")
            return

        promo_code = self._promo_applied
        try:
            est_cost = float(gross - discount)
        except Exception:
            est_cost = gross - discount
        if est_cost < 0:
            est_cost = 0.0

        try:
            wallet_balance = float(self.account.wallet_balance)
        except (TypeError, ValueError):
            wallet_balance = 0.0

        if wallet_balance < est_cost:
            messagebox.showerror(
                "Insufficient Balance",
                f"Wallet: P{wallet_balance:.2f}\n"
                f"Required: P{est_cost:.2f}\n"
                "Please top up your wallet first!",
            )
            return

        surge_txt = f"\n🚀 Surge x{surge}" if surge > 1.0 else ""
        promo_txt = f"\n🎟️ Promo {promo_code}: -P{discount:.2f}" if promo_code else ""
        pax_txt = f"\n👥 Passengers: {passengers}" if passengers > 1 else ""
        notes_txt = f"\n📝 Notes: {notes[:60]}" if notes else ""
        sched_txt = f"\n🗓️ Scheduled: {scheduled_time}" if scheduled_time else ""

        selected_payment_label = self.payment_var.get()
        if selected_payment_label != "Ride Wallet":
            messagebox.showinfo(
                "Payment Method",
                "Only Ride Wallet is currently supported. Your wallet will be charged.",
            )

        from models.driver import Driver as _Driver

        preview_driver = _Driver.get_random_driver()

        driver_txt = (
            f"\n\n🚗 Driver: {preview_driver.name}"
            f"\n   Plate: {preview_driver.plate}"
            f"\n   Rating: {preview_driver.rating} stars"
        )

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Vehicle: {vehicle_type}\n"
            f"From: {start} to {end}\n"
            f"Distance: {distance} km{pax_txt}{surge_txt}{promo_txt}\n"
            f"Total Cost: P{est_cost:.2f}{notes_txt}{sched_txt}"
            f"{driver_txt}\n\n"
            "Confirm booking?",
        )
        if not confirm:
            return

        self.account.wallet_balance -= est_cost
        self.account_manager.update_account(self.account)

        booking = self.service.book_ride(
            self.account.name,
            vehicle_type,
            start,
            end,
            distance,
            passengers=passengers,
            notes=notes,
            promo_code=promo_code,
            discount=discount,
            scheduled_time=scheduled_time,
        )
        self.service.save_bookings()

        import services.notification_service as notif_svc

        notif_svc.push(
            self.account.username,
            f"Booking #{booking.booking_id} confirmed! Driver: {booking.driver.name} ({booking.driver.plate}). Total: ₱{booking.total_cost:.2f}",
            category="ride",
            booking_id=booking.booking_id,
        )

        self.wallet_label.config(text=f"💳 Wallet Balance: P{self.account.wallet_balance:.2f}")

        status_word = "Scheduled" if scheduled_time else "Active"
        surge_msg = f"\n🚀 Surge x{booking.surge}" if booking.surge > 1.0 else ""
        promo_msg = f"\n🎟️ Discount: -P{discount:.2f}" if promo_code else ""
        sched_msg = f"\n🗓️ Pickup at: {scheduled_time}" if scheduled_time else ""

        messagebox.showinfo(
            f"Booking {status_word}! 🎉",
            f"Ride booked successfully!\n"
            f"Driver: {booking.driver.name}\n"
            f"Plate: {booking.driver.plate}\n"
            f"Total Cost: P{booking.total_cost:.2f}{surge_msg}{promo_msg}{sched_msg}\n"
            f"Remaining Balance: P{self.account.wallet_balance:.2f}",
        )

        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
        self.promo_entry.delete(0, tk.END)
        self.promo_label.config(text="")
        self.passengers_var.set(1)
        self._discount = 0.0
        self._promo_applied = None
        self.sched_enable.set(False)
        self.sched_status.config(text="")
        self.estimate_label.config(text="Enter distance to see estimate")
        self.surge_label.config(text="")
        self.fav_var.set("— select a favorite —")
        self.refresh_callback()