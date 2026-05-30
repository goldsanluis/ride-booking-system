code = '''import tkinter as tk
from tkinter import messagebox
from gui.booking_form import BookingForm
from gui.booking_list import BookingList
from gui.wallet_panel import WalletPanel
from services.booking_service import BookingService
from file_handler.file_manager import FileManager
from file_handler.account_manager import AccountManager
import json, os

class MainWindow:
    def __init__(self, account):
        self.account = account
        self.root = tk.Tk()
        self.root.title("Ride Booking System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1a1200")

        self.file_manager = FileManager()
        self.account_manager = AccountManager()
        self.service = BookingService(self.file_manager)

        self.setup_header()
        self.setup_tabs()

    def setup_header(self):
        header = tk.Frame(self.root, bg="#2d1f00", pady=10)
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg="#2d1f00")
        title_frame.pack(fill="x", padx=20)

        tk.Label(
            title_frame,
            text="🚗 Ride Booking System",
            font=("Helvetica", 20, "bold"),
            bg="#2d1f00",
            fg="#FFD700"
        ).pack(side="left")

        tk.Button(
            title_frame,
            text="Logout 🚪",
            font=("Helvetica", 10, "bold"),
            bg="#B8860B",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.logout
        ).pack(side="right")

        tk.Button(
            title_frame,
            text="🔄 Refresh",
            font=("Helvetica", 10, "bold"),
            bg="#FFA500",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.refresh_bookings
        ).pack(side="right", padx=5)

        self.notif_btn = tk.Button(
            title_frame,
            text="🔔 Notifications",
            font=("Helvetica", 10, "bold"),
            bg="#2d1f00",
            fg="#FFD700",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.show_notifications
        )
        self.notif_btn.pack(side="right", padx=5)

        tk.Label(
            header,
            text=f"Welcome, {self.account.name}! 👑",
            font=("Helvetica", 11),
            bg="#2d1f00",
            fg="#FFA500"
        ).pack()

        self._refresh_notif_badge()

    def _refresh_notif_badge(self):
        nf = os.path.join("data", "notifications.json")
        if not os.path.exists(nf):
            return
        with open(nf) as f:
            notifs = json.load(f)
        unread = [n for n in notifs if n.get("user") == self.account.name and not n.get("seen")]
        if unread:
            self.notif_btn.config(fg="#FF4444", text=f"🔔 ({len(unread)}) Notifications")
        else:
            self.notif_btn.config(fg="#FFD700", text="🔔 Notifications")
        self.root.after(5000, self._refresh_notif_badge)

    def show_notifications(self):
        nf = os.path.join("data", "notifications.json")
        if not os.path.exists(nf):
            messagebox.showinfo("Notifications", "No notifications yet.")
            return
        with open(nf) as f:
            notifs = json.load(f)
        mine = [n for n in notifs if n.get("user") == self.account.name]
        if not mine:
            messagebox.showinfo("Notifications", "No notifications for you yet.")
            return
        unread = [n for n in mine if not n.get("seen")]
        msg = ""
        for n in mine[-5:][::-1]:
            status = "[NEW] " if not n.get("seen") else ""
            msg += f"{status}{n.get(chr(109)+chr(101)+chr(115)+chr(115)+chr(97)+chr(103)+chr(101), chr(78)+chr(111)+chr(32)+chr(109)+chr(101)+chr(115)+chr(115)+chr(97)+chr(103)+chr(101))}\\n\\n"
        for n in notifs:
            if n.get("user") == self.account.name:
                n["seen"] = True
        with open(nf, "w") as f:
            json.dump(notifs, f, indent=2)
        self.notif_btn.config(fg="#FFD700", text="🔔 Notifications")
        messagebox.showinfo(f"Notifications ({len(unread)} new)", msg.strip())

    def setup_tabs(self):
        tab_frame = tk.Frame(self.root, bg="#1a1200")
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(tab_frame, bg="#1a1200")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        left_canvas = tk.Canvas(left_frame, bg="#1a1200", highlightthickness=0)
        left_scroll = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)

        left_inner = tk.Frame(left_canvas, bg="#1a1200")
        left_win = left_canvas.create_window((0, 0), window=left_inner, anchor="nw")
        left_inner.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.bind("<Configure>", lambda e: left_canvas.itemconfig(left_win, width=e.width))

        self.booking_form = BookingForm(
            left_inner,
            self.service,
            self.file_manager,
            self.refresh,
            self.account,
            self.account_manager
        )
        self.booking_form.frame.pack(fill="both", expand=True, pady=5)

        self.wallet_panel = WalletPanel(left_inner, self.account, self.account_manager)
        self.wallet_panel.frame.pack(fill="x", pady=5)

        self.booking_list = BookingList(tab_frame, self.service, self.account)
        self.booking_list.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.booking_list.refresh()

    def refresh_bookings(self):
        self.service = BookingService(self.file_manager)
        self.wallet_panel.refresh_balance()
        self.booking_list.service = self.service
        self.refresh()

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            from gui.login_window import LoginWindow
            from gui.main_window import MainWindow
            login = LoginWindow()
            account = login.run()
            if account:
                app = MainWindow(account)
                app.run()

    def run(self):
        self.root.mainloop()
'''

with open("gui/main_window.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Done!")
