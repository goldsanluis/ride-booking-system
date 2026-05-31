"""gui/driver_dashboard.py
--------------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
from services.booking_service import BookingService

from file_handler.file_manager import FileManager
from file_handler.driver_manager import DriverManager
from models.driver import Driver

BG_DARK     = "#1a1200"
BG_CARD     = "#2d1f00"
GOLD        = "#FFD700"
GOLD_DARK   = "#B8860B"
GOLD_ACCENT = "#FFA500"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#9a8060"
GREEN       = "#4ecca3"


class DriverDashboard:
    def __init__(self, driver):
        self.driver         = driver
        self.root           = tk.Tk()
        self.root.title("Ride Booking System - Driver Dashboard")
        self.root.geometry("960x680")
        self.root.configure(bg=BG_DARK)

        self.file_manager   = FileManager()
        self.driver_manager = DriverManager()
        self.service        = BookingService(self.file_manager)

        self.header_frame   = None
        self.notebook_frame = None
        self._active_tab    = "rides"   # "rides" | "earnings" | "profile"

        self.setup_header()
        self.setup_tabs()

    # ─────────────────────────────── HEADER ───────────────────────────────────
    def setup_header(self):
        if self.header_frame:
            self.header_frame.destroy()

        self.header_frame = tk.Frame(self.root, bg=BG_CARD, pady=12)
        self.header_frame.pack(fill="x")

        row = tk.Frame(self.header_frame, bg=BG_CARD)
        row.pack(fill="x", padx=20)

        tk.Label(row, text=f"🚕 {self.driver['name']}",
                 font=("Helvetica", 15, "bold"), bg=BG_CARD, fg=GOLD).pack(side="left")
        tk.Label(row, text=f"Plate: {self.driver['plate']}",
                 font=("Helvetica", 11), bg=BG_CARD, fg=GOLD_ACCENT).pack(side="left", padx=16)
        tk.Label(row, text=f"⭐ {self.driver['rating']}",
                 font=("Helvetica", 11), bg=BG_CARD, fg=GOLD_ACCENT).pack(side="left")

        earnings = self.driver.get("wallet_balance", 0.0)
        self.earnings_label = tk.Label(row,
                                       text=f"💰 Total Earnings: ₱{earnings:.2f}",
                                       font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GREEN)
        self.earnings_label.pack(side="left", padx=18)

        tk.Button(row, text="🔄 Refresh",
                  font=("Helvetica", 10, "bold"), bg=GOLD_ACCENT, fg=BG_DARK,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.refresh_all).pack(side="right", padx=4)
        tk.Button(row, text="Logout 🚪",
                  font=("Helvetica", 10, "bold"), bg=GOLD, fg=BG_DARK,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.logout).pack(side="right")

    # ─────────────────────────────── TABS ─────────────────────────────────────
    def setup_tabs(self):
        if self.notebook_frame:
            self.notebook_frame.destroy()

        self.notebook_frame = tk.Frame(self.root, bg=BG_DARK)
        self.notebook_frame.pack(fill="both", expand=True)

        # Tab bar
        tab_bar = tk.Frame(self.notebook_frame, bg=BG_CARD)
        tab_bar.pack(fill="x")

        self.tab_rides_btn = tk.Button(
            tab_bar, text="🚦 Available Rides",
            font=("Helvetica", 11, "bold"), relief="flat", padx=20, pady=8,
            cursor="hand2", command=self._show_rides_tab)
        self.tab_rides_btn.pack(side="left")

        self.tab_earn_btn = tk.Button(
            tab_bar, text="💼 Earnings History",
            font=("Helvetica", 11, "bold"), relief="flat", padx=20, pady=8,
            cursor="hand2", command=self._show_earnings_tab)
        self.tab_earn_btn.pack(side="left")

        self.tab_profile_btn = tk.Button(
            tab_bar, text="👤 My Profile",
            font=("Helvetica", 11, "bold"), relief="flat", padx=20, pady=8,
            cursor="hand2", command=self._show_profile_tab)
        self.tab_profile_btn.pack(side="left")

        self.tab_content = tk.Frame(self.notebook_frame, bg=BG_DARK)
        self.tab_content.pack(fill="both", expand=True, padx=16, pady=12)

        self._show_rides_tab()

    def _set_tab_styles(self, active):
        for btn, name in [(self.tab_rides_btn, "rides"), (self.tab_earn_btn, "earnings"), (self.tab_profile_btn, "profile")]:
            if name == active:
                btn.config(bg=BG_DARK, fg=GOLD)
            else:
                btn.config(bg=BG_CARD, fg=TEXT_GRAY)

    def _clear_content(self):
        for w in self.tab_content.winfo_children():
            w.destroy()

    # ─────────────────────────────── RIDES TAB ────────────────────────────────
    def _show_rides_tab(self):
        self._active_tab = "rides"
        self._set_tab_styles("rides")
        self._clear_content()

        tk.Label(self.tab_content, text="Available Ride Requests 📍",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(0, 8))

        self.rides_canvas    = tk.Canvas(self.tab_content, bg=BG_DARK, highlightthickness=0)
        rides_sb             = tk.Scrollbar(self.tab_content, orient="vertical",
                                            command=self.rides_canvas.yview)
        self.rides_canvas.configure(yscrollcommand=rides_sb.set)
        rides_sb.pack(side="right", fill="y")
        self.rides_canvas.pack(side="left", fill="both", expand=True)

        self.rides_inner = tk.Frame(self.rides_canvas, bg=BG_DARK)
        self._rides_win  = self.rides_canvas.create_window((0, 0), window=self.rides_inner, anchor="nw")
        self.rides_inner.bind("<Configure>",  lambda e: self.rides_canvas.configure(
            scrollregion=self.rides_canvas.bbox("all")))
        self.rides_canvas.bind("<Configure>", lambda e: self.rides_canvas.itemconfig(
            self._rides_win, width=e.width))

        self._populate_rides()

    def _populate_rides(self):
        for w in self.rides_inner.winfo_children():
            w.destroy()

        active = [b for b in self.service.get_all_bookings()
                  if b.status == "Active" and b.driver.driver_id != self.driver["driver_id"]]

        if not active:
            tk.Label(self.rides_inner, text="No ride requests available right now 😴",
                     font=("Helvetica", 12), bg=BG_DARK, fg=TEXT_GRAY).pack(pady=20)
            return

        for booking in active:
            self._create_ride_card(booking)

    def _create_ride_card(self, booking):
        card = tk.Frame(self.rides_inner, bg=BG_CARD, padx=15, pady=12)
        card.pack(fill="x", padx=6, pady=6)

        tk.Label(card, text=f"👤 {booking.user}",
                 font=("Helvetica", 12, "bold"), bg=BG_CARD, fg=GOLD).pack(anchor="w")
        tk.Label(card, text=f"📍 {booking.start_location} → {booking.end_location}",
                 font=("Helvetica", 11), bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w", pady=3)

        pax = getattr(booking, "passengers", 1)
        pax_txt  = f"  👥 {pax} pax" if pax > 1 else ""
        notes    = getattr(booking, "notes", "")
        det = f"📏 {booking.distance} km  |  💰 ₱{booking.total_cost:.2f}  |  {booking.vehicle.name}{pax_txt}"
        tk.Label(card, text=det, font=("Helvetica", 10),
                 bg=BG_CARD, fg=GOLD_ACCENT).pack(anchor="w")

        if notes:
            tk.Label(card, text=f"📝 {notes[:80]}",
                     font=("Helvetica", 9, "italic"), bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=1)

        if booking.surge > 1.0:
            tk.Label(card, text=f"🚀 Surge ×{booking.surge}",
                     font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=GREEN).pack(anchor="w")

        tk.Button(card, text="✅ Accept Ride",
                  font=("Helvetica", 11, "bold"), bg=GREEN, fg=TEXT_WHITE,
                  relief="flat", padx=15, pady=7, cursor="hand2",
                  command=lambda b=booking: self.accept_ride(b)).pack(pady=8, anchor="w")

    def accept_ride(self, booking):
        if messagebox.askyesno(
                "Accept Ride?",
                f"Accept ride from {booking.user}?\n"
                f"{booking.start_location} → {booking.end_location}\n"
                f"You will earn: ₱{booking.total_cost:.2f}"):

            booking.driver = Driver(self.driver["name"], self.driver["plate"],
                                    self.driver["rating"], driver_id=self.driver["driver_id"])
            
            import os as _os, json as _json
            _nf = _os.path.join('data', 'notifications.json')
            _notifs = _json.load(open(_nf)) if _os.path.exists(_nf) else []
            _notifs.append({'user': booking.user, 'message': f"Driver {self.driver['name']} ({self.driver['plate']}) accepted your ride!", 'booking_id': booking.booking_id, 'seen': False})
            _json.dump(_notifs, open(_nf, 'w'), indent=2)
            self.driver_manager.update_driver_wallet(self.driver["driver_id"], booking.total_cost)
            self.driver["wallet_balance"] = self.driver.get("wallet_balance", 0.0) + booking.total_cost
            self.earnings_label.config(text=f"💰 Total Earnings: ₱{self.driver['wallet_balance']:.2f}")

            messagebox.showinfo("Ride Accepted! 🎉",
                                f"You accepted {booking.user}'s ride!\n"
                                f"Route: {booking.start_location} → {booking.end_location}\n"
                                f"You earned: ₱{booking.total_cost:.2f}\n"
                                f"Total Earnings: ₱{self.driver['wallet_balance']:.2f}")
            self._populate_rides()

    # ─────────────────────────────── EARNINGS TAB ─────────────────────────────
    def _show_earnings_tab(self):
        self._active_tab = "earnings"
        self._set_tab_styles("earnings")
        self._clear_content()
        self._build_earnings()

    def _build_earnings(self):
        # Reload fresh data
        self.service = BookingService(self.file_manager)
        drivers = self.driver_manager.load_drivers()
        for d in drivers:
            if d["driver_id"] == self.driver["driver_id"]:
                self.driver["wallet_balance"] = d.get("wallet_balance", 0.0)
                break

        # Find all bookings accepted by this driver (completed or still active)
        my_bookings = [
            b for b in self.service.get_all_bookings()
            if b.driver.driver_id == self.driver["driver_id"]
        ]
        completed   = [b for b in my_bookings if b.status == "Completed"]
        active      = [b for b in my_bookings if b.status == "Active"]

        total_earned = sum(b.total_cost for b in completed)
        pending      = sum(b.total_cost for b in active)
        ride_count   = len(completed)
        avg          = total_earned / ride_count if ride_count else 0.0

        # ── Summary cards ────────────────────────────────────────────────────
        summary_row = tk.Frame(self.tab_content, bg=BG_DARK)
        summary_row.pack(fill="x", pady=(0, 12))

        def stat(parent, label, value, color=GOLD):
            fr = tk.Frame(parent, bg=BG_CARD, padx=16, pady=12)
            fr.pack(side="left", expand=True, fill="x", padx=6)
            tk.Label(fr, text=label, font=("Helvetica", 9),
                     bg=BG_CARD, fg=TEXT_GRAY).pack()
            tk.Label(fr, text=value, font=("Helvetica", 14, "bold"),
                     bg=BG_CARD, fg=color).pack()

        stat(summary_row, "Total Earned",    f"₱{total_earned:.2f}", GREEN)
        stat(summary_row, "Rides Completed", str(ride_count),         GOLD)
        stat(summary_row, "Avg per Ride",    f"₱{avg:.2f}",           GOLD_ACCENT)
        stat(summary_row, "Pending (active)", f"₱{pending:.2f}",      GOLD_ACCENT)

        # ── Filter bar ───────────────────────────────────────────────────────
        fb = tk.Frame(self.tab_content, bg=BG_CARD, padx=8, pady=6)
        fb.pack(fill="x", pady=(0, 8))
        tk.Label(fb, text="Filter:", font=("Helvetica", 9, "bold"),
                 bg=BG_CARD, fg=GOLD_ACCENT).grid(row=0, column=0, padx=(0, 6))

        self.earn_status_var = tk.StringVar(value="All")
        tk.Label(fb, text="Status:", font=("Helvetica", 9),
                 bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=1)
        st_cb = tk.OptionMenu(fb, self.earn_status_var, "All", "Completed", "Active",
                               command=lambda _: self._refresh_earnings_list(my_bookings))
        st_cb.config(font=("Helvetica", 9), bg=BG_DARK, fg=TEXT_WHITE,
                     relief="flat", bd=0, highlightthickness=0)
        st_cb["menu"].config(bg=BG_DARK, fg=TEXT_WHITE, font=("Helvetica", 9))
        st_cb.grid(row=0, column=2, padx=(2, 12))

        self.earn_period_var = tk.StringVar(value="All time")
        tk.Label(fb, text="Period:", font=("Helvetica", 9),
                 bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=3)
        pe_cb = tk.OptionMenu(fb, self.earn_period_var,
                               "All time", "Today", "This week", "This month",
                               command=lambda _: self._refresh_earnings_list(my_bookings))
        pe_cb.config(font=("Helvetica", 9), bg=BG_DARK, fg=TEXT_WHITE,
                     relief="flat", bd=0, highlightthickness=0)
        pe_cb["menu"].config(bg=BG_DARK, fg=TEXT_WHITE, font=("Helvetica", 9))
        pe_cb.grid(row=0, column=4, padx=(2, 12))

        # ── Scrollable list ──────────────────────────────────────────────────
        self.earn_canvas = tk.Canvas(self.tab_content, bg=BG_DARK, highlightthickness=0)
        earn_sb          = tk.Scrollbar(self.tab_content, orient="vertical",
                                        command=self.earn_canvas.yview)
        self.earn_canvas.configure(yscrollcommand=earn_sb.set)
        earn_sb.pack(side="right", fill="y")
        self.earn_canvas.pack(side="left", fill="both", expand=True)

        self.earn_inner = tk.Frame(self.earn_canvas, bg=BG_DARK)
        self._earn_win  = self.earn_canvas.create_window((0, 0), window=self.earn_inner, anchor="nw")
        self.earn_inner.bind("<Configure>",  lambda e: self.earn_canvas.configure(
            scrollregion=self.earn_canvas.bbox("all")))
        self.earn_canvas.bind("<Configure>", lambda e: self.earn_canvas.itemconfig(
            self._earn_win, width=e.width))

        self._all_my_bookings = my_bookings
        self._refresh_earnings_list(my_bookings)

    def _refresh_earnings_list(self, my_bookings):
        from datetime import datetime
        for w in self.earn_inner.winfo_children():
            w.destroy()

        status = self.earn_status_var.get()
        period = self.earn_period_var.get()
        now    = datetime.now()

        filtered = []
        for b in my_bookings:
            if status != "All" and b.status != status:
                continue
            if period != "All time":
                try:
                    bd = datetime.strptime(b.date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
                if period == "Today" and bd.date() != now.date():
                    continue
                if period == "This week" and (now - bd).days > 7:
                    continue
                if period == "This month" and (bd.month != now.month or bd.year != now.year):
                    continue
            filtered.append(b)

        # Sort newest first
        filtered.sort(key=lambda b: b.date, reverse=True)

        if not filtered:
            tk.Label(self.earn_inner, text="No earnings match the current filter.",
                     font=("Helvetica", 11), bg=BG_DARK, fg=TEXT_GRAY).pack(pady=20)
            return

        for b in filtered:
            self._create_earnings_card(b)

    def _create_earnings_card(self, b):
        card = tk.Frame(self.earn_inner, bg=BG_CARD, padx=12, pady=8)
        card.pack(fill="x", padx=6, pady=4)

        hdr = tk.Frame(card, bg=BG_CARD); hdr.pack(fill="x")
        sc  = GREEN if b.status == "Completed" else GOLD_ACCENT
        tk.Label(hdr, text=f"#{b.booking_id} • {b.user}",
                 font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=GOLD).pack(side="left")
        tk.Label(hdr, text=f"● {b.status}",
                 font=("Helvetica", 9), bg=BG_CARD, fg=sc).pack(side="right")

        tk.Label(card, text=f"📍 {b.start_location} → {b.end_location}",
                 font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_WHITE).pack(anchor="w", pady=1)

        surge_txt = f"  🚀×{b.surge}" if b.surge > 1.0 else ""
        det = f"📏 {b.distance} km  |  {b.vehicle.name}{surge_txt}  |  📅 {b.date}"
        tk.Label(card, text=det, font=("Helvetica", 9),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")

        earn_color = GREEN if b.status == "Completed" else GOLD_ACCENT
        tk.Label(card, text=f"₱{b.total_cost:.2f}",
                 font=("Helvetica", 13, "bold"), bg=BG_CARD, fg=earn_color).pack(anchor="e")


    # ─────────────────────────────── PROFILE TAB ──────────────────────────────
    def _show_profile_tab(self):
        self._active_tab = "profile"
        self._set_tab_styles("profile")
        self._clear_content()
        self._build_profile()

    def _build_profile(self):
        # Reload fresh driver data
        drivers = self.driver_manager.load_drivers()
        d_data  = next((d for d in drivers if d["driver_id"] == self.driver["driver_id"]), self.driver)

        # All bookings for this driver
        self.service = BookingService(self.file_manager)
        my_bookings  = [b for b in self.service.get_all_bookings()
                        if b.driver.driver_id == self.driver["driver_id"]]
        completed    = [b for b in my_bookings if b.status == "Completed"]
        total_earned = sum(b.total_cost for b in completed)
        ride_count   = len(completed)
        avg          = total_earned / ride_count if ride_count else 0.0
        total_km     = sum(b.distance for b in completed)
        rating       = d_data.get("rating", self.driver.get("rating", 5.0))
        rating_count = d_data.get("rating_count", 0)

        inner = self.tab_content

        # Avatar + name
        avatar_frame = tk.Frame(inner, bg=BG_CARD, pady=20)
        avatar_frame.pack(fill="x", pady=(0, 12))
        tk.Label(avatar_frame, text="🧑‍✈️",
                 font=("Helvetica", 48), bg=BG_CARD).pack()
        tk.Label(avatar_frame, text=d_data.get("name", self.driver["name"]),
                 font=("Helvetica", 16, "bold"), bg=BG_CARD, fg=GOLD).pack()
        tk.Label(avatar_frame, text=f"🚗 {d_data.get('plate', self.driver['plate'])}",
                 font=("Helvetica", 12), bg=BG_CARD, fg=GOLD_ACCENT).pack()

        # Rating display
        stars = int(round(rating))
        tk.Label(avatar_frame, text=f"{'★' * stars}{'☆' * (5 - stars)}",
                 font=("Helvetica", 20), bg=BG_CARD, fg=GOLD).pack()
        tk.Label(avatar_frame, text=f"{rating:.2f} avg  ({rating_count} ratings)",
                 font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_GRAY).pack()

        # Stats row
        stats_row = tk.Frame(inner, bg=BG_DARK)
        stats_row.pack(fill="x", pady=4)

        def stat(parent, icon, label, value, color=GOLD):
            fr = tk.Frame(parent, bg=BG_CARD, padx=16, pady=12)
            fr.pack(side="left", expand=True, fill="x", padx=5)
            tk.Label(fr, text=icon,  font=("Helvetica", 18), bg=BG_CARD, fg=color).pack()
            tk.Label(fr, text=value, font=("Helvetica", 14, "bold"), bg=BG_CARD, fg=color).pack()
            tk.Label(fr, text=label, font=("Helvetica", 8),  bg=BG_CARD, fg=TEXT_GRAY).pack()

        stat(stats_row, "✅", "Rides Completed", str(ride_count),          GREEN)
        stat(stats_row, "💰", "Total Earned",    f"₱{total_earned:.2f}",  GREEN)
        stat(stats_row, "📏", "Total Distance",  f"{total_km:.1f} km",    GOLD_ACCENT)
        stat(stats_row, "💳", "Avg per Ride",    f"₱{avg:.2f}",           GOLD)

        # Vehicle type breakdown
        tk.Label(inner, text="Rides by Vehicle Type",
                 font=("Helvetica", 11, "bold"), bg=BG_DARK, fg=GOLD_ACCENT).pack(pady=(16, 4))

        by_v = {}
        for b in completed:
            vname = b.vehicle.name
            by_v[vname] = by_v.get(vname, 0) + 1

        if by_v:
            total_v = sum(by_v.values()) or 1
            bar_frame = tk.Frame(inner, bg=BG_CARD, padx=16, pady=12)
            bar_frame.pack(fill="x", padx=10)
            icons  = {"Car": "🚗", "Van": "🚐", "Bike": "🏍️"}
            colors = {"Car": GOLD, "Van": "#00bcd4", "Bike": GREEN}
            for vname, count in sorted(by_v.items(), key=lambda x: x[1], reverse=True):
                pct = count / total_v
                row = tk.Frame(bar_frame, bg=BG_CARD); row.pack(fill="x", pady=3)
                tk.Label(row, text=f"{icons.get(vname,'🚗')} {vname}",
                         font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_WHITE,
                         width=8, anchor="w").pack(side="left")
                bar_outer = tk.Frame(row, bg="#3d2a00", height=16)
                bar_outer.pack(side="left", fill="x", expand=True, padx=8)
                bar_outer.pack_propagate(False)
                bar_inner = tk.Frame(bar_outer, bg=colors.get(vname, GOLD), height=16)
                bar_inner.place(relwidth=pct, relheight=1.0)
                tk.Label(row, text=f"{count} ride{'s' if count != 1 else ''} ({pct*100:.0f}%)",
                         font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_GRAY,
                         width=18, anchor="e").pack(side="left")
        else:
            tk.Label(inner, text="Accept and complete rides to see your breakdown.",
                     font=("Helvetica", 10), bg=BG_DARK, fg=TEXT_GRAY).pack(pady=8)


    # ─────────────────────────────── MISC ─────────────────────────────────────
    def refresh_all(self):
        self.service = BookingService(self.file_manager)
        drivers = self.driver_manager.load_drivers()
        for d in drivers:
            if d["driver_id"] == self.driver["driver_id"]:
                self.driver["wallet_balance"] = d.get("wallet_balance", 0.0)
                break
        self.earnings_label.config(text=f"💰 Total Earnings: ₱{self.driver['wallet_balance']:.2f}")
        if self._active_tab == "rides":
            self._show_rides_tab()
        else:
            self._show_earnings_tab()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            from gui.main_menu import MainMenu
            MainMenu().run()

    def run(self):
        self.root.mainloop()
