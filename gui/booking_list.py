"""gui/booking_list.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk

from file_handler.driver_manager import DriverManager

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_DARK     = "#1a0000"
BG_CARD     = "#800000"
BG_FIELD    = "#6b0000"
MAROON_LT   = "#990000"
GOLD        = "#FFD700"
GOLD_DIM    = "#FFC200"
TEXT_WHITE  = "#FFFFFF"
TEXT_GRAY   = "#ffcccc"
RED         = "#FF6B6B"
DIVIDER     = "#990000"


def _configure_slim_scrollbar():
    """Register a slim ttk scrollbar style (6 px, no arrows)."""
    style = ttk.Style()
    try:
        style.theme_use("default")
    except Exception:
        pass
    style.configure(
        "Slim.Vertical.TScrollbar",
        gripcount=0,
        background=MAROON_LT,
        darkcolor=BG_FIELD,
        lightcolor=BG_FIELD,
        troughcolor=BG_DARK,
        bordercolor=BG_DARK,
        arrowcolor=GOLD,
        width=6,
        arrowsize=0,
        relief="flat",
    )
    style.map(
        "Slim.Vertical.TScrollbar",
        background=[("active", GOLD), ("!active", MAROON_LT)],
    )


def _make_scrollable(parent):
    """Return (canvas, inner_frame) with slim scrollbar and mousewheel support."""
    _configure_slim_scrollbar()

    canvas = tk.Canvas(parent, bg=BG_DARK, highlightthickness=0)
    vbar   = ttk.Scrollbar(
        parent, orient="vertical",
        command=canvas.yview,
        style="Slim.Vertical.TScrollbar",
    )
    canvas.configure(yscrollcommand=vbar.set)
    vbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner  = tk.Frame(canvas, bg=BG_DARK)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(win_id, width=event.width)

    def on_mousewheel(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    inner.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>",   on_mousewheel)
    canvas.bind_all("<Button-5>",   on_mousewheel)

    return canvas, inner


class BookingList:

    def __init__(self, parent, service, account):
        self.service        = service
        self.account        = account
        self.driver_manager = DriverManager()
        self._active_tab    = "bookings"

        self.frame = tk.Frame(parent, bg=BG_DARK)

        # ── Tab bar ────────────────────────────────────────────────────────────
        tab_bar = tk.Frame(self.frame, bg=BG_CARD)
        tab_bar.pack(fill="x")

        self.tab_book_btn = tk.Button(
            tab_bar, text="📋  My Bookings",
            font=("Helvetica", 10, "bold"), relief="flat",
            padx=16, pady=7, cursor="hand2",
            command=self._show_bookings_tab,
        )
        self.tab_book_btn.pack(side="left")

        self.tab_stats_btn = tk.Button(
            tab_bar, text="📊  My Stats",
            font=("Helvetica", 10, "bold"), relief="flat",
            padx=16, pady=7, cursor="hand2",
            command=self._show_stats_tab,
        )
        self.tab_stats_btn.pack(side="left")

        self.content_frame = tk.Frame(self.frame, bg=BG_DARK)
        self.content_frame.pack(fill="both", expand=True)

        self._show_bookings_tab()

    def _set_tab_styles(self, active):
        for btn, name in [(self.tab_book_btn, "bookings"), (self.tab_stats_btn, "stats")]:
            if name == active:
                btn.config(bg=BG_DARK, fg=GOLD)
            else:
                btn.config(bg=BG_CARD, fg=TEXT_GRAY)

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    # ════════════════════════════════════════════════════════════════════════
    #  BOOKINGS TAB
    # ════════════════════════════════════════════════════════════════════════
    def _show_bookings_tab(self):
        self._active_tab = "bookings"
        self._set_tab_styles("bookings")
        self._clear_content()
        self._build_bookings_ui()

    def _build_bookings_ui(self):
        # ── Actions row ───────────────────────────────────────────────────────
        action_frame = tk.Frame(self.content_frame, bg=BG_DARK, padx=8, pady=6)
        action_frame.pack(fill="x", padx=4)
        tk.Button(
            action_frame, text="🧾  Export Bookings",
            font=("Helvetica", 10, "bold"), bg=GOLD, fg=BG_DARK,
            relief="flat", padx=12, pady=5, cursor="hand2",
            activebackground=MAROON_LT, activeforeground=GOLD,
            command=self._export_bookings,
        ).pack(side="right")

        # ── Search bar ────────────────────────────────────────────────────────
        search_frame = tk.Frame(self.content_frame, bg=BG_CARD, padx=8, pady=6)
        search_frame.pack(fill="x", padx=4, pady=(4, 0))
        tk.Label(search_frame, text="🔍", font=("Helvetica", 11),
                 bg=BG_CARD, fg=GOLD).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("Helvetica", 10), bg=BG_DARK, fg=TEXT_WHITE,
            insertbackground=GOLD, relief="flat", bd=4,
        ).pack(side="left", fill="x", expand=True, padx=6)
        tk.Button(
            search_frame, text="✖", font=("Helvetica", 9),
            bg=BG_CARD, fg=TEXT_GRAY, relief="flat", cursor="hand2",
            command=lambda: self.search_var.set(""),
        ).pack(side="left")

        # ── Filter bar ────────────────────────────────────────────────────────
        filter_frame = tk.Frame(self.content_frame, bg=BG_CARD, padx=8, pady=5)
        filter_frame.pack(fill="x", padx=4, pady=(0, 4))

        tk.Label(filter_frame, text="Filter:", font=("Helvetica", 9, "bold"),
                 bg=BG_CARD, fg=GOLD).grid(row=0, column=0, sticky="w", padx=(0, 6))

        def _dd(parent, var, options, col, label):
            tk.Label(parent, text=label, font=("Helvetica", 9),
                     bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=col, sticky="w")
            cb = tk.OptionMenu(parent, var, *options, command=lambda _: self.refresh())
            cb.config(font=("Helvetica", 9), bg=BG_DARK, fg=TEXT_WHITE,
                      activebackground=BG_CARD, relief="flat", bd=0, highlightthickness=0)
            cb["menu"].config(bg=BG_DARK, fg=TEXT_WHITE, font=("Helvetica", 9))
            cb.grid(row=0, column=col + 1, padx=(2, 10))

        self.status_var  = tk.StringVar(value="All")
        self.vehicle_var = tk.StringVar(value="All")
        self.date_var    = tk.StringVar(value="All time")

        _dd(filter_frame, self.status_var,
            ["All", "Active", "Scheduled", "Completed", "Cancelled"], 1, "Status:")
        _dd(filter_frame, self.vehicle_var,
            ["All", "Car", "Van", "Bike"], 3, "Vehicle:")
        _dd(filter_frame, self.date_var,
            ["All time", "Today", "This week", "This month"], 5, "Date:")

        tk.Button(
            filter_frame, text="✖ Clear", font=("Helvetica", 9),
            bg=BG_DARK, fg=TEXT_GRAY, relief="flat", padx=6, cursor="hand2",
            command=self._clear_filters,
        ).grid(row=0, column=7)

        self.count_label = tk.Label(filter_frame, text="",
                                    font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_GRAY)
        self.count_label.grid(row=0, column=8, padx=(10, 0))

        # ── Scrollable list ───────────────────────────────────────────────────
        self.canvas, self.inner_frame = _make_scrollable(self.content_frame)
        self.refresh()

    def _clear_filters(self):
        self.status_var.set("All")
        self.vehicle_var.set("All")
        self.date_var.set("All time")
        self.search_var.set("")
        self.refresh()

    def _filter_bookings(self, bookings):
        from datetime import datetime

        status  = self.status_var.get()
        vehicle = self.vehicle_var.get()
        period  = self.date_var.get()
        keyword = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        now     = datetime.now()

        result = []
        for b in bookings:
            if status != "All" and b.status != status:
                continue
            if vehicle != "All" and b.vehicle.name != vehicle:
                continue
            if keyword:
                haystack = (b.start_location + " " + b.end_location + " " + (b.notes or "")).lower()
                if keyword not in haystack:
                    continue
            if period != "All time":
                bdate = None
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                    try:
                        bdate = datetime.strptime(b.date, fmt)
                        break
                    except ValueError:
                        continue
                if bdate is None:
                    continue
                if period == "Today" and bdate.date() != now.date():
                    continue
                elif period == "This week" and (now - bdate).days > 7:
                    continue
                elif period == "This month" and (bdate.month != now.month or bdate.year != now.year):
                    continue
            result.append(b)
        return result

    def refresh(self):
        if self._active_tab != "bookings":
            return
        if not hasattr(self, "inner_frame"):
            return
        for w in self.inner_frame.winfo_children():
            w.destroy()

        all_bookings      = self.service.get_user_bookings(self.account.username)
        all_bookings      = sorted(all_bookings, key=lambda b: b.date, reverse=True)
        filtered_bookings = self._filter_bookings(all_bookings)

        total   = len(all_bookings)
        showing = len(filtered_bookings)
        self.count_label.config(
            text=(f"Showing {showing} of {total}" if showing != total else f"{total} bookings")
        )

        if not filtered_bookings:
            msg = "No bookings yet 😴" if total == 0 else "No bookings match current filters."
            tk.Label(self.inner_frame, text=msg,
                     font=("Helvetica", 11), bg=BG_DARK, fg=TEXT_GRAY,
                     ).pack(pady=24)
            return

        for booking in filtered_bookings:
            self._create_card(booking)

    def _create_card(self, booking):
        status_color = {
            "Active":    GOLD,
            "Completed": "#90EE90",
            "Cancelled": RED,
            "Scheduled": "#87CEEB",
        }.get(booking.status, GOLD)

        # Outer wrapper with left-accent border
        wrapper = tk.Frame(self.inner_frame, bg=status_color)
        wrapper.pack(fill="x", padx=6, pady=4)

        card = tk.Frame(wrapper, bg=BG_CARD, padx=12, pady=10)
        card.pack(fill="x", padx=(3, 0))

        # Header
        hdr = tk.Frame(card, bg=BG_CARD)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text=f"Booking #{booking.booking_id}",
                 font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD,
                 ).pack(side="left")
        tk.Label(hdr, text=f"● {booking.status}",
                 font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=status_color,
                 ).pack(side="right")

        tk.Frame(card, bg=DIVIDER, height=1).pack(fill="x", pady=(0, 6))

        tk.Label(card, text=f"🚗  {booking.driver.name}",
                 font=("Helvetica", 10), bg=BG_CARD, fg=GOLD,
                 ).pack(anchor="w", pady=1)
        tk.Label(card,
                 text=f"📍  {booking.start_location}  →  {booking.end_location}",
                 font=("Helvetica", 10), bg=BG_CARD, fg=TEXT_WHITE,
                 ).pack(anchor="w", pady=1)

        surge_txt = f"  🚀×{booking.surge}" if booking.surge > 1.0 else ""
        pax_txt   = f"  👥{getattr(booking, 'passengers', 1)}" if getattr(booking, 'passengers', 1) > 1 else ""
        promo_txt = f"  🎟️ −₱{booking.discount:.0f}" if getattr(booking, 'discount', 0) > 0 else ""
        det = (
            f"📏 {booking.distance} km  |  "
            f"💰 ₱{booking.total_cost:.2f}  |  "
            f"{booking.vehicle.name}{surge_txt}{pax_txt}{promo_txt}"
        )
        tk.Label(card, text=det, font=("Helvetica", 9),
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=1)

        sched = getattr(booking, "scheduled_time", None)
        if sched:
            tk.Label(card, text=f"🗓️  Scheduled:  {sched}",
                     font=("Helvetica", 9, "bold"), bg=BG_CARD, fg="#87CEEB",
                     ).pack(anchor="w", pady=1)

        notes = getattr(booking, "notes", "")
        if notes:
            tk.Label(card,
                     text=f"📝  {notes[:80]}{'…' if len(notes) > 80 else ''}",
                     font=("Helvetica", 9, "italic"), bg=BG_CARD, fg=TEXT_GRAY,
                     ).pack(anchor="w", pady=1)

        tk.Label(card, text=f"📅  {booking.date}",
                 font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_GRAY,
                 ).pack(anchor="w", pady=(1, 6))

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x")

        def _btn(parent, text, bg, fg, cmd, side="left"):
            tk.Button(
                parent, text=text,
                font=("Helvetica", 9, "bold"), bg=bg, fg=fg,
                relief="flat", padx=10, pady=4, cursor="hand2",
                activebackground=MAROON_LT, activeforeground=fg,
                command=cmd,
            ).pack(side=side, padx=2)

        if booking.status == "Scheduled":
            _btn(btn_row, "▶  Activate Now", "#87CEEB", BG_DARK, lambda b=booking: self._activate(b))
            _btn(btn_row, "❌  Cancel",       RED,       "white",  lambda b=booking: self._cancel(b))

        elif booking.status == "Active":
            _btn(btn_row, "✅  Complete", "#90EE90", BG_DARK, lambda b=booking: self._complete(b))
            _btn(btn_row, "📍  Track",    "#87CEEB", BG_DARK, lambda b=booking: self._track(b))
            _btn(btn_row, "❌  Cancel",   RED,       "white",  lambda b=booking: self._cancel(b))

        elif booking.status == "Completed":
            if not booking.rating:
                _btn(btn_row, "⭐  Rate", GOLD, BG_DARK, lambda b=booking: self._rate(b))
            else:
                tk.Label(btn_row, text=f"{'⭐' * booking.rating}  Your rating",
                         font=("Helvetica", 9), bg=BG_CARD, fg=GOLD).pack(side="left", padx=4)

        if booking.status == "Completed":
            _btn(btn_row, "🧾  Receipt", BG_DARK, GOLD,
                 lambda b=booking: self._show_receipt(b), side="right")

    # ── Actions ───────────────────────────────────────────────────────────────
    def _cancel(self, booking):
        refund_pct = 50 if booking.status == "Active" else 100
        confirm_msg = (
            f"Cancel booking #{booking.booking_id}?\n"
            f"Refund policy: {refund_pct}% of the booking total will be returned to your wallet."
        )
        if messagebox.askyesno("Cancel Booking", confirm_msg):
            msg, refund_amt = self.service.cancel_booking(
                booking.booking_id, self.account.username, refund_policy=refund_pct,
            )
            self.account.wallet_balance += refund_amt
            from file_handler.account_manager import AccountManager
            AccountManager().update_account(self.account)

            import services.notification_service as notif_svc
            notif_svc.push(
                self.account.username,
                f"Booking #{booking.booking_id} cancelled. ₱{refund_amt:.2f} refunded.",
                category="refund", booking_id=booking.booking_id,
            )
            self._save()
            messagebox.showinfo("Cancelled", msg)
            self.refresh()

    def _complete(self, booking):
        if messagebox.askyesno("Complete Booking",
                               f"Mark booking #{booking.booking_id} as completed?"):
            msg = self.service.complete_booking(booking.booking_id, self.account.username)
            if booking.driver.driver_id and booking.driver.driver_id != "unassigned":
                self.driver_manager.update_driver_wallet(booking.driver.driver_id, booking.total_cost)
            import services.notification_service as notif_svc
            notif_svc.push(
                self.account.username,
                f"Ride #{booking.booking_id} completed! "
                f"Please rate your driver {booking.driver.name}.",
                category="ride", booking_id=booking.booking_id,
            )
            self._save()
            messagebox.showinfo("Success", msg)
            self.refresh()

    def _activate(self, booking):
        if messagebox.askyesno("Activate Now",
                               f"Activate booking #{booking.booking_id} right now?"):
            msg = self.service.activate_booking(booking.booking_id, self.account.username)
            if msg.startswith("Booking #"):
                messagebox.showinfo("Activated", msg)
                self.refresh()
            else:
                messagebox.showerror("Activation Failed", msg)

    def _rate(self, booking):
        rate_win = tk.Toplevel()
        rate_win.title(f"Rate Ride #{booking.booking_id}")
        rate_win.configure(bg=BG_DARK)
        rate_win.resizable(False, False)
        rate_win.grab_set()

        tk.Label(rate_win, text="How was your ride?",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD,
                 ).pack(pady=(16, 4))
        tk.Label(rate_win, text=f"Driver: {booking.driver.name}",
                 font=("Helvetica", 10), bg=BG_DARK, fg=TEXT_GRAY).pack()

        star_var    = tk.IntVar(value=5)
        star_frame  = tk.Frame(rate_win, bg=BG_DARK)
        star_frame.pack(pady=12)
        star_labels = []

        def update_stars(selected):
            star_var.set(selected)
            for i, lbl in enumerate(star_labels):
                lbl.config(fg=GOLD if i < selected else TEXT_GRAY)

        for i in range(1, 6):
            lbl = tk.Label(star_frame, text="★", font=("Helvetica", 26),
                           bg=BG_DARK, fg=GOLD, cursor="hand2")
            lbl.pack(side="left", padx=2)
            lbl.bind("<Button-1>", lambda e, s=i: update_stars(s))
            lbl.bind("<Enter>",    lambda e, s=i: update_stars(s))
            star_labels.append(lbl)
        update_stars(5)

        tk.Label(rate_win, text="Leave a comment (optional):",
                 font=("Helvetica", 9), bg=BG_DARK, fg=TEXT_GRAY).pack()
        feedback_entry = tk.Entry(
            rate_win, font=("Helvetica", 10), width=32,
            bg=BG_CARD, fg=TEXT_WHITE, insertbackground=GOLD,
            relief="flat", bd=4,
        )
        feedback_entry.pack(padx=20, pady=(4, 8))

        def submit():
            rating  = star_var.get()
            msg     = self.service.rate_booking(booking.booking_id, self.account.username, rating)
            if booking.driver.driver_id and booking.driver.driver_id != "unassigned":
                self.driver_manager.update_driver_rating(booking.driver.driver_id, rating)
            comment = feedback_entry.get().strip()
            if comment:
                booking.notes = (booking.notes or "") + f" [Review: {comment}]"
            self._save()
            rate_win.destroy()
            messagebox.showinfo("Thank you!", msg)
            self.refresh()

        tk.Button(
            rate_win, text="Submit Rating",
            font=("Helvetica", 11, "bold"), bg=GOLD, fg=BG_DARK,
            relief="flat", padx=16, pady=8, cursor="hand2",
            activebackground=MAROON_LT, activeforeground=GOLD,
            command=submit,
        ).pack(pady=(4, 16))

    def _track(self, booking):
        from gui.tracking_window import TrackingWindow
        TrackingWindow(self.frame, booking, on_complete_callback=lambda: None)

    def _show_receipt(self, booking):
        surge_txt  = f"\n🚀  Surge ×{booking.surge} applied" if booking.surge > 1.0 else ""
        promo_txt  = f"\n🎟️  Promo {booking.promo_code}: −₱{booking.discount:.2f}" if getattr(booking, "promo_code", None) else ""
        rating_txt = f"{'⭐' * booking.rating}" if booking.rating else "Not rated"
        pax_txt    = f"\n👥  Passengers: {getattr(booking, 'passengers', 1)}"
        notes_txt  = f"\n📝  Notes: {booking.notes}" if getattr(booking, "notes", "") else ""

        receipt = (
            f"{'═'*36}\n"
            f"         RIDE RECEIPT\n"
            f"{'═'*36}\n"
            f"Booking ID : #{booking.booking_id}\n"
            f"Date       : {booking.date}\n"
            f"{'─'*36}\n"
            f"From       : {booking.start_location}\n"
            f"To         : {booking.end_location}\n"
            f"Distance   : {booking.distance} km\n"
            f"Vehicle    : {booking.vehicle.name}{pax_txt}\n"
            f"Driver     : {booking.driver.name}\n"
            f"{'─'*36}\n"
            f"Fare       : ₱{booking.total_cost:.2f}"
            f"{surge_txt}{promo_txt}{notes_txt}\n"
            f"Status     : {booking.status}\n"
            f"Rating     : {rating_txt}\n"
            f"{'═'*36}"
        )
        messagebox.showinfo(f"Receipt — Booking #{booking.booking_id}", receipt)

    def _save(self):
        self.service.save_bookings()

    def _export_bookings(self):
        all_bookings = self.service.get_user_bookings(self.account.username)
        filtered     = self._filter_bookings(all_bookings)

        if not filtered:
            messagebox.showinfo("Export", "No bookings to export.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Bookings Export",
        )
        if not path:
            return

        lines = [
            "PUP RIDES — BOOKING EXPORT",
            f"User: {self.account.username}",
            "=" * 40, "",
        ]
        for b in filtered:
            lines.append(f"Booking #{b.booking_id}")
            lines.append(f"  Date     : {b.date}")
            lines.append(f"  From     : {b.start_location}")
            lines.append(f"  To       : {b.end_location}")
            lines.append(f"  Vehicle  : {b.vehicle.name}")
            lines.append(f"  Driver   : {b.driver.name}")
            lines.append(f"  Distance : {b.distance} km")
            lines.append(f"  Fare     : ₱{b.total_cost:.2f}")
            lines.append(f"  Status   : {b.status}")
            if b.rating:
                lines.append(f"  Rating   : {'⭐' * b.rating}")
            lines.append("-" * 40)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Export Successful", f"Bookings exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    # ════════════════════════════════════════════════════════════════════════
    #  STATS TAB
    # ════════════════════════════════════════════════════════════════════════
    def _show_stats_tab(self):
        self._active_tab = "stats"
        self._set_tab_styles("stats")
        self._clear_content()
        self._build_stats_ui()

    def _build_stats_ui(self):
        stats = self.service.get_user_stats(self.account.username)

        canvas, inner = _make_scrollable(self.content_frame)

        tk.Label(inner, text="📊  My Ride Statistics",
                 font=("Helvetica", 14, "bold"), bg=BG_DARK, fg=GOLD,
                 ).pack(pady=(14, 8))

        # ── Summary cards ─────────────────────────────────────────────────────
        cards_frame = tk.Frame(inner, bg=BG_DARK)
        cards_frame.pack(fill="x", padx=10, pady=4)

        card_data = [
            ("Total Bookings", stats["total_bookings"], GOLD,      "🗂️"),
            ("Completed",      stats["completed"],      "#90EE90", "✅"),
            ("Cancelled",      stats["cancelled"],      RED,       "❌"),
            ("Active / Sched", stats["active"],         GOLD,      "🚗"),
        ]
        for col, (label, value, color, icon) in enumerate(card_data):
            cf = tk.Frame(cards_frame, bg=BG_CARD, padx=12, pady=10)
            cf.grid(row=0, column=col, padx=5, pady=4, sticky="nsew")
            cards_frame.columnconfigure(col, weight=1)
            tk.Label(cf, text=icon,    font=("Helvetica", 16), bg=BG_CARD, fg=color).pack()
            tk.Label(cf, text=str(value), font=("Helvetica", 20, "bold"), bg=BG_CARD, fg=color).pack()
            tk.Label(cf, text=label,   font=("Helvetica", 9),  bg=BG_CARD, fg=TEXT_GRAY).pack()

        # ── Spending summary ──────────────────────────────────────────────────
        tk.Frame(inner, bg=DIVIDER, height=1).pack(fill="x", padx=10, pady=6)
        spend_frame = tk.Frame(inner, bg=BG_CARD, padx=14, pady=12)
        spend_frame.pack(fill="x", padx=10, pady=(0, 4))
        tk.Label(spend_frame, text="💰  Spending Summary",
                 font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD,
                 ).pack(anchor="w", pady=(0, 6))

        avg_rating = stats.get("avg_rating_given")
        rating_txt = f"{'⭐' * round(avg_rating)} ({avg_rating:.1f})" if avg_rating else "N/A"

        for label, value in [
            ("Total Spent",      f"₱{stats['total_spent']:.2f}"),
            ("Average Fare",     f"₱{stats['avg_fare']:.2f}"),
            ("Total Distance",   f"{stats['total_distance']:.1f} km"),
            ("Avg Rating Given", rating_txt),
        ]:
            row = tk.Frame(spend_frame, bg=BG_CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, font=("Helvetica", 10),
                     bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10, "bold"),
                     bg=BG_CARD, fg=TEXT_WHITE).pack(side="right")

        # ── By vehicle breakdown ──────────────────────────────────────────────
        by_v = stats.get("by_vehicle", {})
        if by_v:
            tk.Frame(inner, bg=DIVIDER, height=1).pack(fill="x", padx=10, pady=6)
            veh_frame = tk.Frame(inner, bg=BG_CARD, padx=14, pady=12)
            veh_frame.pack(fill="x", padx=10, pady=(0, 14))
            tk.Label(veh_frame, text="🚗  Spending by Vehicle",
                     font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD,
                     ).pack(anchor="w", pady=(0, 6))

            total_v = sum(by_v.values()) or 1
            veh_colors = {"Car": GOLD, "Van": "#87CEEB", "Bike": "#90EE90"}
            for vname, amount in by_v.items():
                pct   = amount / total_v * 100
                color = veh_colors.get(vname, TEXT_WHITE)
                row   = tk.Frame(veh_frame, bg=BG_CARD)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=vname, font=("Helvetica", 10),
                         bg=BG_CARD, fg=color, width=6, anchor="w").pack(side="left")
                bar_bg = tk.Frame(row, bg=BG_DARK, height=10, width=190)
                bar_bg.pack(side="left", padx=8)
                bar_bg.pack_propagate(False)
                fill_w = max(4, int(pct / 100 * 190))
                tk.Frame(bar_bg, bg=color, height=10, width=fill_w).place(x=0, y=0)
                tk.Label(row, text=f"₱{amount:.2f}  ({pct:.0f}%)",
                         font=("Helvetica", 9), bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")