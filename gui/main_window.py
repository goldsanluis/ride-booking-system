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


class MainWindow:
    """
    Main passenger dashboard.
    Hosts the booking form on the left and the booking list on the right.
    """

    def __init__(self, account):
        self.account      = account
        self.root         = tk.Tk()
        self._notif_after_id = None

        self.root.title("Ride Booking System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1a1200")

        self.file_manager    = FileManager()
        self.account_manager = AccountManager()
        self.service         = BookingService(self.file_manager)

        self.setup_header()
        self.setup_tabs()

        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    # ── Header ────────────────────────────────────────────────────────────────

    def setup_header(self):
        header = tk.Frame(self.root, bg="#2d1f00", pady=10)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg="#2d1f00")
        title_frame.pack(fill="x", padx=20)

        tk.Label(
            title_frame, text="🚗 Ride Booking System",
            font=("Helvetica", 20, "bold"),
            bg="#2d1f00", fg="#FFD700",
        ).pack(side="left")

        # Right-side buttons (packed right-to-left)
        tk.Button(
            title_frame, text="Logout 🚪",
            font=("Helvetica", 10, "bold"),
            bg="#B8860B", fg="white", relief="flat",
            padx=10, pady=5, cursor="hand2",
            command=self.logout,
        ).pack(side="right")

        tk.Button(
            title_frame, text="🔄 Refresh",
            font=("Helvetica", 10, "bold"),
            bg="#FFA500", fg="white", relief="flat",
            padx=10, pady=5, cursor="hand2",
            command=self.refresh_bookings,
        ).pack(side="right", padx=5)

        self.notif_btn = tk.Button(
            title_frame, text="🔔 Notifications",
            font=("Helvetica", 10, "bold"),
            bg="#2d1f00", fg="#FFD700", relief="flat",
            padx=10, pady=5, cursor="hand2",
            command=self._open_notification_center,
        )
        self.notif_btn.pack(side="right", padx=5)

        tk.Button(
            title_frame, text="💳 Payment",
            font=("Helvetica", 10, "bold"),
            bg="#2d1f00", fg="#4ecca3", relief="flat",
            padx=10, pady=5, cursor="hand2",
            command=self._open_payment_methods,
        ).pack(side="right", padx=5)

        tk.Button(
            title_frame, text="ℹ️ About",
            font=("Helvetica", 10, "bold"),
            bg="#2d1f00", fg="#FFD700", relief="flat",
            padx=10, pady=5, cursor="hand2",
            command=self._open_about,
        ).pack(side="right", padx=5)

        tk.Label(
            header,
            text=f"Welcome, {self.account.name}! 👑",
            font=("Helvetica", 11),
            bg="#2d1f00", fg="#FFA500",
        ).pack()

        self._refresh_notif_badge()

    def _refresh_notif_badge(self):
        """Poll for unread notifications every 5 s and update the button label."""
        try:
            if not self.root.winfo_exists():
                return
            import services.notification_service as ns
            count = ns.get_unread_count(self.account.username)
            if count > 0:
                self.notif_btn.config(fg="#FF4444", text=f"🔔 ({count}) Notifications")
            else:
                self.notif_btn.config(fg="#FFD700", text="🔔 Notifications")
        except Exception:
            pass

        if self.root.winfo_exists():
            self._notif_after_id = self.root.after(5000, self._refresh_notif_badge)

    # ── Main layout ───────────────────────────────────────────────────────────

    def setup_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#1a1200")
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ── Left panel: booking form + wallet ─────────────────────────────────
        left_frame  = tk.Frame(tab_frame, bg="#1a1200")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        left_canvas = tk.Canvas(left_frame, bg="#1a1200", highlightthickness=0)
        left_scroll = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)

        left_inner = tk.Frame(left_canvas, bg="#1a1200")
        left_win   = left_canvas.create_window((0, 0), window=left_inner, anchor="nw")
        left_inner.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")),
        )
        left_canvas.bind(
            "<Configure>",
            lambda e: left_canvas.itemconfig(left_win, width=e.width),
        )

        self.booking_form = BookingForm(
            left_inner, self.service, self.file_manager,
            self.refresh, self.account, self.account_manager,
        )
        self.booking_form.frame.pack(fill="both", expand=True, pady=5)

        self.wallet_panel = WalletPanel(left_inner, self.account, self.account_manager)
        self.wallet_panel.frame.pack(fill="x", pady=5)

        # ── Right panel: booking list ─────────────────────────────────────────
        self.booking_list = BookingList(tab_frame, self.service, self.account)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=5)

    # ── Menu actions ──────────────────────────────────────────────────────────

    def _open_notification_center(self):
        from gui.notification_center import NotificationCenter
        import services.notification_service as ns
        ns.mark_all_seen(self.account.username)
        self.notif_btn.config(fg="#FFD700", text="🔔 Notifications")
        NotificationCenter(self.root, self.account.username)

    def _open_payment_methods(self):
        from gui.payment_methods_window import PaymentMethodsWindow
        PaymentMethodsWindow(self.root, self.account.username)

    def _open_about(self):
        from gui.about_window import AboutWindow
        AboutWindow(
            self.root,
            app_name="Ride Booking System",
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
        """Refresh the booking list panel."""
        self.booking_list.refresh()

    def refresh_bookings(self):
        """Reload bookings from disk and update all panels."""
        self.service = BookingService(self.file_manager)
        self.wallet_panel.refresh_balance()
        self.booking_list.service = self.service
        self.refresh()

    def logout(self):
        """Confirm logout, destroy window, and return to login screen."""
        if not messagebox.askyesno("Logout", "Are you sure you want to logout?"):
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

    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()