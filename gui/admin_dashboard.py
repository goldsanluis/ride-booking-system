"""
Admin Dashboard — accessible from login with special admin credentials.
Manages: users, promos, drivers, bookings stats, broadcast notifications.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from file_handler.file_manager import FileManager
from file_handler.account_manager import AccountManager
from file_handler.driver_manager import DriverManager
from services.booking_service import BookingService
import services.promo_service as promos_svc
import services.notification_service as notif_svc

# ── PUP Maroon, Gold & White Design System ────────────────────────────────────
BG_DARK  = "#1a0000"   # Deep dark maroon background
BG_CARD  = "#800000"   # Maroon card surface
BG_FIELD = "#6b0000"   # Input field background
GOLD     = "#FFD700"   # PUP Gold
WHITE    = "#FFFFFF"   # White text
GRAY     = "#ffcccc"   # Muted light for subtitles
RED      = "#FF6B6B"   # Error/cancel red
GREEN    = "#90EE90"   # Light green for completed
TEAL     = "#87CEEB"   # Light blue for scheduled
ORANGE   = "#FFD700"   # Reuse gold for highlights
PURPLE   = "#FFD700"   # Reuse gold for drivers stat

# ── Admin credentials (hardcoded for simplicity) ─────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def is_admin(username: str, password: str) -> bool:
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


class AdminDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚙️  Admin Dashboard — PUP Rides")
        self.root.geometry("1050x680")
        self.root.configure(bg=BG_DARK)

        self.fm  = FileManager()
        self.am  = AccountManager()
        self.dm  = DriverManager()
        self.svc = BookingService(self.fm)

        self._active_tab = "overview"
        self._build_header()
        self._build_tabs()
        self._show_overview()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG_CARD, pady=10)
        hdr.pack(fill="x")

        tk.Frame(hdr, bg=BG_DARK, height=6).pack(fill="x", pady=(0, 8))

        title_row = tk.Frame(hdr, bg=BG_CARD)
        title_row.pack(fill="x", padx=16)

        tk.Label(title_row, text="🎓", font=("Helvetica", 24),
                 bg=BG_CARD, fg=GOLD).pack(side="left")

        txt = tk.Frame(title_row, bg=BG_CARD)
        txt.pack(side="left", padx=(10, 0))
        tk.Label(txt, text="PUP Rides — Admin Dashboard",
                 font=("Helvetica", 16, "bold"), bg=BG_CARD, fg=GOLD,
                 justify="left").pack(anchor="w")
        tk.Label(txt, text="Polytechnic University of the Philippines",
                 font=("Helvetica", 8), bg=BG_CARD, fg=WHITE).pack(anchor="w")

        tk.Button(title_row, text="🚪 Exit",
                  font=("Helvetica", 10), bg=RED, fg=WHITE, relief="flat",
                  padx=10, pady=4, cursor="hand2",
                  command=self.root.destroy).pack(side="right")

        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x")

    # ── Tab bar ───────────────────────────────────────────────────────────────
    def _build_tabs(self):
        self.tab_bar = tk.Frame(self.root, bg=BG_CARD)
        self.tab_bar.pack(fill="x")

        tabs = [("overview", "📊 Overview"), ("users", "👥 Users"),
                ("bookings", "📋 Bookings"), ("drivers", "🚕 Drivers"),
                ("promos", "🎟️ Promos"), ("notify", "🔔 Broadcast")]
        self.tab_btns = {}
        for key, label in tabs:
            btn = tk.Button(self.tab_bar, text=label,
                            font=("Helvetica", 10, "bold"), relief="flat",
                            padx=16, pady=8, cursor="hand2",
                            command=lambda k=key: self._switch(k))
            btn.pack(side="left")
            self.tab_btns[key] = btn

        self.content = tk.Frame(self.root, bg=BG_DARK)
        self.content.pack(fill="both", expand=True)

    def _switch(self, tab: str):
        self._active_tab = tab
        for k, btn in self.tab_btns.items():
            btn.config(bg=BG_DARK if k == tab else BG_CARD,
                       fg=GOLD if k == tab else GRAY)
        for w in self.content.winfo_children():
            w.destroy()
        {
            "overview": self._show_overview,
            "users":    self._show_users,
            "bookings": self._show_bookings,
            "drivers":  self._show_drivers,
            "promos":   self._show_promos,
            "notify":   self._show_notify,
        }[tab]()

    # ── Overview ──────────────────────────────────────────────────────────────
    def _show_overview(self):
        self._switch_style("overview")
        frame = self._scroll_frame()

        tk.Label(frame, text="System Overview",
                 font=("Helvetica", 14, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 12))

        bookings  = self.svc.get_all_bookings()
        accounts  = self.am.load_accounts()
        drivers   = self.dm.load_drivers()
        completed = [b for b in bookings if b.status == "Completed"]
        revenue   = sum(b.total_cost for b in completed)

        row1 = tk.Frame(frame, bg=BG_DARK); row1.pack(fill="x", padx=16, pady=4)
        row2 = tk.Frame(frame, bg=BG_DARK); row2.pack(fill="x", padx=16, pady=4)
        self._stat(row1, "👥", "Users",     str(len(accounts)),    TEAL)
        self._stat(row1, "🚕", "Drivers",   str(len(drivers)),     GOLD)
        self._stat(row1, "📋", "Bookings",  str(len(bookings)),    GOLD)
        self._stat(row2, "✅", "Completed", str(len(completed)),   GREEN)
        self._stat(row2, "❌", "Cancelled", str(len([b for b in bookings if b.status == "Cancelled"])), RED)
        self._stat(row2, "💰", "Revenue",   f"₱{revenue:,.2f}",   GREEN)

        tk.Label(frame, text="Recent Bookings (last 10)",
                 font=("Helvetica", 11, "bold"), bg=BG_DARK, fg=GOLD).pack(anchor="w", padx=16, pady=(16, 4))
        recent = sorted(bookings, key=lambda b: b.date, reverse=True)[:10]
        for b in recent:
            c = tk.Frame(frame, bg=BG_CARD, padx=10, pady=6)
            c.pack(fill="x", padx=16, pady=2)
            tk.Label(c, text=f"#{b.booking_id}  {b.user}  {b.start_location}→{b.end_location}",
                     font=("Helvetica", 10), bg=BG_CARD, fg=WHITE).pack(side="left")
            scol = {"Completed": GREEN, "Cancelled": RED, "Active": GOLD}.get(b.status, TEAL)
            tk.Label(c, text=f"{b.status}  ₱{b.total_cost:.2f}",
                     font=("Helvetica", 10), bg=BG_CARD, fg=scol).pack(side="right")

    # ── Users ─────────────────────────────────────────────────────────────────
    def _show_users(self):
        self._switch_style("users")
        frame = self._scroll_frame()
        tk.Label(frame, text="User Accounts",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 8))

        accounts = self.am.load_accounts()
        if not accounts:
            tk.Label(frame, text="No users found.", bg=BG_DARK, fg=GRAY).pack(pady=20)
            return

        for acc in accounts:
            c = tk.Frame(frame, bg=BG_CARD, padx=12, pady=8)
            c.pack(fill="x", padx=16, pady=3)
            tk.Label(c, text=f"👤 {acc['name']}  (@{acc['username']})",
                     font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=WHITE).pack(side="left")
            tk.Label(c, text=f"💳 ₱{acc.get('wallet_balance', 0):.2f}",
                     font=("Helvetica", 10), bg=BG_CARD, fg=GREEN).pack(side="right", padx=12)

            def _edit_wallet(a=acc):
                amt = simpledialog.askfloat("Edit Wallet",
                                            f"Set wallet balance for {a['username']}:",
                                            initialvalue=a.get("wallet_balance", 0.0),
                                            minvalue=0.0, maxvalue=999999.0,
                                            parent=self.root)
                if amt is not None:
                    accs = self.am.load_accounts()
                    for x in accs:
                        if x["username"] == a["username"]:
                            x["wallet_balance"] = amt
                    self.am.save_accounts(accs)
                    messagebox.showinfo("Updated", f"Balance set to ₱{amt:.2f}")
                    self._switch("users")

            tk.Button(c, text="✏️ Edit Wallet",
                      font=("Helvetica", 8), bg=GOLD, fg=BG_DARK,
                      relief="flat", padx=6, pady=2, cursor="hand2",
                      command=_edit_wallet).pack(side="right")

    # ── Bookings ──────────────────────────────────────────────────────────────
    def _show_bookings(self):
        self._switch_style("bookings")
        frame = self._scroll_frame()
        tk.Label(frame, text="All Bookings",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 8))

        bookings = sorted(self.svc.get_all_bookings(), key=lambda b: b.date, reverse=True)
        for b in bookings:
            scol = {"Completed": GREEN, "Cancelled": RED, "Active": GOLD, "Scheduled": TEAL}.get(b.status, WHITE)
            c = tk.Frame(frame, bg=BG_CARD, padx=10, pady=6)
            c.pack(fill="x", padx=16, pady=2)
            tk.Label(c, text=f"#{b.booking_id}  {b.user}",
                     font=("Helvetica", 10, "bold"), bg=BG_CARD, fg=WHITE).pack(side="left")
            tk.Label(c, text=f"{b.vehicle.name}  {b.start_location}→{b.end_location}  ₱{b.total_cost:.2f}",
                     font=("Helvetica", 9), bg=BG_CARD, fg=GRAY).pack(side="left", padx=10)
            tk.Label(c, text=b.status,
                     font=("Helvetica", 9, "bold"), bg=BG_CARD, fg=scol).pack(side="right")

    # ── Drivers ───────────────────────────────────────────────────────────────
    def _show_drivers(self):
        self._switch_style("drivers")
        frame = self._scroll_frame()
        tk.Label(frame, text="Registered Drivers",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 8))

        drivers = self.dm.load_drivers()
        if not drivers:
            tk.Label(frame, text="No registered drivers yet.",
                     bg=BG_DARK, fg=GRAY).pack(pady=20)
            return

        for d in drivers:
            c = tk.Frame(frame, bg=BG_CARD, padx=12, pady=8)
            c.pack(fill="x", padx=16, pady=3)
            tk.Label(c, text=f"🚕 {d['name']}  ({d.get('plate', '?')})",
                     font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=WHITE).pack(side="left")
            info = f"⭐{d.get('rating', 0):.1f}  💰₱{d.get('wallet_balance', 0):.2f}"
            tk.Label(c, text=info, font=("Helvetica", 10), bg=BG_CARD, fg=GREEN).pack(side="right")

    # ── Promos ────────────────────────────────────────────────────────────────
    def _show_promos(self):
        self._switch_style("promos")
        frame = self._scroll_frame()
        tk.Label(frame, text="Promo Code Manager",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 4))

        all_p = promos_svc.get_all_promos()
        extra = promos_svc._load_extra_promos()

        for code, info in all_p.items():
            is_custom = code in extra
            c = tk.Frame(frame, bg=BG_CARD, padx=12, pady=6)
            c.pack(fill="x", padx=16, pady=2)
            tk.Label(c, text=f"🎟️ {code}",
                     font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD).pack(side="left")
            detail = f"{info['desc']}  ({info['type']} {info['value']}{'%' if info['type'] == 'percent' else '₱'})"
            tk.Label(c, text=detail, font=("Helvetica", 9), bg=BG_CARD, fg=GRAY).pack(side="left", padx=8)
            if is_custom:
                tk.Button(c, text="🗑 Delete",
                          font=("Helvetica", 8), bg=RED, fg=WHITE, relief="flat",
                          padx=6, pady=2, cursor="hand2",
                          command=lambda cd=code: self._del_promo(cd)).pack(side="right")
            else:
                tk.Label(c, text="[built-in]", font=("Helvetica", 8),
                         bg=BG_CARD, fg=GRAY).pack(side="right")

        add = tk.Frame(frame, bg=BG_CARD, padx=14, pady=12)
        add.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(add, text="➕ Add New Promo",
                 font=("Helvetica", 11, "bold"), bg=BG_CARD, fg=GOLD).pack(anchor="w", pady=(0, 8))

        fields = {}
        for lbl, key, default in [("Code", "code", ""), ("Description", "desc", ""),
                                   ("Type (flat/percent)", "type", "flat"),
                                   ("Value", "value", "10"), ("Min Fare", "min_fare", "0")]:
            row = tk.Frame(add, bg=BG_CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=lbl + ":", font=("Helvetica", 9), bg=BG_CARD,
                     fg=GRAY, width=22, anchor="w").pack(side="left")
            e = tk.Entry(row, font=("Helvetica", 10), bg=BG_FIELD, fg=WHITE,
                         insertbackground=GOLD, relief="flat", bd=3)
            e.insert(0, default)
            e.pack(side="left", fill="x", expand=True)
            fields[key] = e

        def _add_promo():
            try:
                promos_svc.add_promo(
                    code=fields["code"].get().strip(),
                    ptype=fields["type"].get().strip(),
                    value=float(fields["value"].get()),
                    min_fare=float(fields["min_fare"].get()),
                    desc=fields["desc"].get().strip(),
                )
                messagebox.showinfo("Added!", f"Promo {fields['code'].get().upper()} created.")
                self._switch("promos")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

        tk.Button(add, text="➕ Create Promo",
                  font=("Helvetica", 10, "bold"), bg=GOLD, fg=BG_DARK,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  command=_add_promo).pack(pady=(8, 0))

    def _del_promo(self, code: str):
        if messagebox.askyesno("Delete", f"Delete promo {code}?", parent=self.root):
            promos_svc.delete_promo(code)
            self._switch("promos")

    # ── Broadcast notification ─────────────────────────────────────────────────
    def _show_notify(self):
        self._switch_style("notify")
        frame = self._scroll_frame()
        tk.Label(frame, text="📢 Broadcast Notification",
                 font=("Helvetica", 13, "bold"), bg=BG_DARK, fg=GOLD).pack(pady=(10, 8))

        tk.Label(frame, text="Send a message to ALL users:",
                 font=("Helvetica", 10), bg=BG_DARK, fg=GRAY).pack(anchor="w", padx=16)

        msg_box = tk.Text(frame, font=("Helvetica", 11), bg=BG_CARD, fg=WHITE,
                          insertbackground=GOLD, relief="flat", bd=4, height=5, wrap="word")
        msg_box.pack(fill="x", padx=16, pady=6)

        cat_var = tk.StringVar(value="system")
        cat_frame = tk.Frame(frame, bg=BG_DARK)
        cat_frame.pack(anchor="w", padx=16)
        tk.Label(cat_frame, text="Category:", font=("Helvetica", 9),
                 bg=BG_DARK, fg=GRAY).pack(side="left")
        for cat in ["system", "promo", "ride"]:
            icon = notif_svc.CATEGORIES.get(cat, "🔔")
            tk.Radiobutton(cat_frame, text=f"{icon} {cat}", variable=cat_var, value=cat,
                           bg=BG_DARK, fg=WHITE, selectcolor=BG_CARD,
                           activebackground=BG_DARK, font=("Helvetica", 9)).pack(side="left", padx=8)

        def _send():
            msg = msg_box.get("1.0", tk.END).strip()
            if not msg:
                messagebox.showerror("Error", "Message cannot be empty.", parent=self.root)
                return
            notif_svc.broadcast(msg, cat_var.get())
            messagebox.showinfo("Sent!", "Notification broadcast to all users.")
            msg_box.delete("1.0", tk.END)

        tk.Button(frame, text="📢 Send to All Users",
                  font=("Helvetica", 11, "bold"), bg=GOLD, fg=BG_DARK,
                  relief="flat", padx=16, pady=8, cursor="hand2",
                  command=_send).pack(pady=10)

        tk.Label(frame, text="Recent Broadcasts",
                 font=("Helvetica", 11, "bold"), bg=BG_DARK, fg=GOLD).pack(anchor="w", padx=16, pady=(12, 4))
        notifs = notif_svc._load()
        system_notifs = [n for n in notifs if n.get("category") in ("system", "promo")][-10:]
        for n in reversed(system_notifs):
            c = tk.Frame(frame, bg=BG_CARD, padx=10, pady=6)
            c.pack(fill="x", padx=16, pady=2)
            tk.Label(c, text=n.get("message", "")[:80],
                     font=("Helvetica", 9), bg=BG_CARD, fg=WHITE).pack(side="left")
            tk.Label(c, text=n.get("timestamp", "")[:16],
                     font=("Helvetica", 8), bg=BG_CARD, fg=GRAY).pack(side="right")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _stat(self, parent, icon, label, value, color=GOLD):
        f = tk.Frame(parent, bg=BG_CARD, padx=14, pady=12)
        f.pack(side="left", expand=True, fill="x", padx=5)
        tk.Label(f, text=icon, font=("Helvetica", 18), bg=BG_CARD).pack()
        tk.Label(f, text=value, font=("Helvetica", 15, "bold"), bg=BG_CARD, fg=color).pack()
        tk.Label(f, text=label, font=("Helvetica", 8), bg=BG_CARD, fg=GRAY).pack()

    def _scroll_frame(self):
        canvas = tk.Canvas(self.content, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        return inner

    def _switch_style(self, active: str):
        for k, btn in self.tab_btns.items():
            btn.config(bg=BG_DARK if k == active else BG_CARD,
                       fg=GOLD if k == active else GRAY)

    def run(self):
        self.root.mainloop()