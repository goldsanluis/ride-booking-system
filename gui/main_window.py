"""gui/main_window.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
import json, os

from gui.booking_form  import BookingForm
from gui.booking_list  import BookingList
from gui.wallet_panel  import WalletPanel
from services.booking_service  import BookingService
from file_handler.file_manager import FileManager
from file_handler.account_manager import AccountManager

# ── PUP Design System ─────────────────────────────────────────────────────────
BG_APP      = "#1C0A0A"
BG_HEADER   = "#2A1010"
BG_NAV      = "#220D0D"
MAROON      = "#800000"
MAROON_LT   = "#A01515"
GOLD        = "#C8A951"
GOLD_BRIGHT = "#E8C96B"
GOLD_DIM    = "#8B7535"
TEXT_WHITE  = "#F5F0E8"
TEXT_MUTED  = "#7A6060"
TEAL        = "#4ECDC4"   # accent for payment/info
RED_NOTIF   = "#FF5555"


class MainWindow:
    """Main passenger dashboard — PUP Rides redesign."""

    def __init__(self, account):
        self.account         = account
        self.root            = tk.Tk()
        self._notif_after_id = None

        self.root.title("PUP Rides")
        self.root.geometry("1150x720")
        self.root.configure(bg=BG_APP)

        self.file_manager    = FileManager()
        self.account_manager = AccountManager()
        self.service         = BookingService(self.file_manager)

        self._build_header()
        self._build_body()

        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_HEADER)
        header.pack(fill="x")

        # Gold top accent line
        tk.Frame(header, bg=GOLD, height=3).pack(fill="x")

        nav = tk.Frame(header, bg=BG_HEADER, padx=24, pady=12)
        nav.pack(fill="x")

        # Left: brand
        brand_frame = tk.Frame(nav, bg=BG_HEADER)
        brand_frame.pack(side="left")
        tk.Label(brand_frame, text="🎓 PUP Rides",
                 font=("Helvetica", 18, "bold"), bg=BG_HEADER, fg=GOLD_BRIGHT).pack(side="left")
        tk.Label(brand_frame, text="  Polytechnic University of the Philippines",
                 font=("Helvetica", 9), bg=BG_HEADER, fg=GOLD_DIM).pack(side="left", pady=(4, 0))

        # Right: action buttons
        btn_cfg = dict(font=("Helvetica", 9, "bold"), relief="flat",
                       padx=12, pady=6, cursor="hand2")

        tk.Button(nav, text="Logout", bg=MAROON, fg=GOLD_BRIGHT,
                  activebackground=MAROON_LT, activeforeground=GOLD_BRIGHT,
                  command=self.logout, **btn_cfg).pack(side="right", padx=(4, 0))

        tk.Button(nav, text="↺ Refresh", bg=BG_HEADER, fg=TEXT_WHITE,
                  activebackground=BG_NAV, command=self.refresh_bookings,
                  **btn_cfg).pack(side="right", padx=4)

        self.notif_btn = tk.Button(
            nav, text="🔔 Notifications", bg=BG_HEADER, fg=GOLD,
            activebackground=BG_NAV, command=self._open_notification_center,
            **btn_cfg)
        self.notif_btn.pack(side="right", padx=4)

        tk.Button(nav, text="💳 Payment", bg=BG_HEADER, fg=TEAL,
                  activebackground=BG_NAV, command=self._open_payment_methods,
                  **btn_cfg).pack(side="right", padx=4)

        tk.Button(nav, text="ℹ About", bg=BG_HEADER, fg=TEXT_MUTED,
                  activebackground=BG_NAV, command=self._open_about,
                  **btn_cfg).pack(side="right", padx=4)

        # Welcome bar below nav
        sub = tk.Frame(self.root, bg=MAROON, padx=24, pady=8)
        sub.pack(fill="x")
        tk.Label(sub, text=f"Good day, {self.account.name}!  🎓",
                 font=("Helvetica", 11), bg=MAROON, fg=GOLD_BRIGHT).pack(side="left")
        tk.Label(sub, text="PUP — Ang Paaralan ng Bayan",
                 font=("Helvetica", 9, "italic"), bg=MAROON, fg=GOLD_DIM).pack(side="right")

        self._refresh_notif_badge()

    def _refresh_notif_badge(self):
        try:
            if not self.root.winfo_exists():
                return
            import services.notification_service as ns
            count = ns.get_unread_count(self.account.username)
            if count > 0:
                self.notif_btn.config(fg=RED_NOTIF, text=f"🔔 ({count}) Notifications")
            else:
                self.notif_btn.config(fg=GOLD, text="🔔 Notifications")
        except Exception:
            pass
        if self.root.winfo_exists():
            self._notif_after_id = self.root.after(5000, self._refresh_notif_badge)

    # ── Body ─────────────────────────────────────────────────────────────────

    def _build_body(self):
        body = tk.Frame(self.root, bg=BG_APP)
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # ── Left column: booking form + wallet ────────────────────────────────
        left = tk.Frame(body, bg=BG_APP)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        left_canvas = tk.Canvas(left, bg=BG_APP, highlightthickness=0)
        left_scroll = tk.Scrollbar(left, orient="vertical", command=left_canvas.yview)
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)

        left_inner = tk.Frame(left_canvas, bg=BG_APP)
        left_win = left_canvas.create_window((0, 0), window=left_inner, anchor="nw")
        left_inner.bind("<Configure>",
                        lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.bind("<Configure>",
                         lambda e: left_canvas.itemconfig(left_win, width=e.width))

        self.booking_form = BookingForm(
            left_inner, self.service, self.file_manager,
            self.refresh, self.account, self.account_manager,
        )
        self.booking_form.frame.pack(fill="both", expand=True, pady=(0, 8))

        self.wallet_panel = WalletPanel(left_inner, self.account, self.account_manager)
        self.wallet_panel.frame.pack(fill="x")

        # ── Right column: booking list ────────────────────────────────────────
        self.booking_list = BookingList(body, self.service, self.account)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

    # ── Menu actions ──────────────────────────────────────────────────────────

    def _open_notification_center(self):
        from gui.notification_center import NotificationCenter
        import services.notification_service as ns
        ns.mark_all_seen(self.account.username)
        self.notif_btn.config(fg=GOLD, text="🔔 Notifications")
        NotificationCenter(self.root, self.account.username)

    def _open_payment_methods(self):
        from gui.payment_methods_window import PaymentMethodsWindow
        PaymentMethodsWindow(self.root, self.account.username)

    def _open_about(self):
        from gui.about_window import AboutWindow
        AboutWindow(
            self.root,
            app_name="PUP Rides",
            app_version="1.0",
            group_members=[
                "Domingo, Franco Luis",
                "Gacu, Laiza May M.",
                "Luna, Sybella Llorin B.",
                "Mamaril, Jayson Cris L.",
                "Mejia, Aayel",
                "Mesias, Lewell",
                "Pangandaman, Najer D.",
                "Sabida, Ghale Anne",
                "San Luis, Ghani Regina Gold B.",
                "Tatlonghari, Jan Druelle",
            ],
            section="BSCPE 1-5",
        )

    # ── Refresh / Logout ──────────────────────────────────────────────────────

    def refresh(self):
        self.booking_list.refresh()

    def refresh_bookings(self):
        self.service = BookingService(self.file_manager)
        self.wallet_panel.refresh_balance()
        self.booking_list.service = self.service
        self.refresh()

    def logout(self):
        if not messagebox.askyesno("Sign out", "Are you sure you want to sign out?"):
            return
        try:
            if self._notif_after_id is not None:
                self.root.after_cancel(self._notif_after_id)
        except Exception:
            pass
        self.root.destroy()
        from gui.login_window import LoginWindow
        login   = LoginWindow()
        account = login.run()
        if account:
            MainWindow(account).run()

    def setup_header(self):
        self._build_header()

    def setup_tabs(self):
        self._build_body()

    def run(self):
        self.root.mainloop()