"""
Full-featured Notification Center window.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
import services.notification_service as ns

BG_DARK  = "#1a1200"
BG_CARD  = "#2d1f00"
GOLD     = "#FFD700"
GREEN    = "#4ecca3"
TEAL     = "#00bcd4"
ORANGE   = "#FFA500"
WHITE    = "#FFFFFF"
GRAY     = "#9a8060"
RED      = "#FF6B6B"
GOLD_DRK = "#B8860B"


class NotificationCenter:
    def __init__(self, parent, username):
        self.username = username

        self.win = tk.Toplevel(parent)
        self.win.title("🔔 Notification Center")
        self.win.geometry("480x560")
        self.win.configure(bg=BG_DARK)
        self.win.resizable(False, True)
        self.win.grab_set()

        self._build()
        self._load()

    def _build(self):
        # Header
        hdr = tk.Frame(self.win, bg=BG_CARD, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔔  Notification Center",
                 font=("Helvetica", 14, "bold"), bg=BG_CARD, fg=GOLD).pack(side="left", padx=14)

        btn_frame = tk.Frame(hdr, bg=BG_CARD)
        btn_frame.pack(side="right", padx=10)
        tk.Button(btn_frame, text="✅ Mark All Read",
                  font=("Helvetica", 9), bg=GOLD_DRK, fg=WHITE, relief="flat",
                  padx=8, pady=3, cursor="hand2",
                  command=self._mark_all).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑 Clear All",
                  font=("Helvetica", 9), bg=RED, fg=WHITE, relief="flat",
                  padx=8, pady=3, cursor="hand2",
                  command=self._clear_all).pack(side="left")

        # Filter row
        filt = tk.Frame(self.win, bg=BG_CARD, pady=6, padx=10)
        filt.pack(fill="x")
        tk.Label(filt, text="Filter:", font=("Helvetica", 9), bg=BG_CARD, fg=GRAY).pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        for cat in ["All", "ride", "payment", "promo", "driver", "refund", "system"]:
            icon = ns.CATEGORIES.get(cat, "📌")
            lbl  = f"{icon} {cat.title()}" if cat != "All" else "All"
            tk.Radiobutton(filt, text=lbl, variable=self.filter_var, value=cat,
                           bg=BG_CARD, fg=WHITE, selectcolor="#3d2a00",
                           activebackground=BG_CARD, activeforeground=GOLD,
                           font=("Helvetica", 8),
                           command=self._load).pack(side="left", padx=4)

        # Scrollable list
        outer = tk.Frame(self.win, bg=BG_DARK)
        outer.pack(fill="both", expand=True, padx=10, pady=6)
        self.canvas = tk.Canvas(outer, bg=BG_DARK, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=BG_DARK)
        win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(win_id, width=e.width))

    def _load(self):
        for w in self.inner.winfo_children():
            w.destroy()

        notifs = ns.get_for_user(self.username)
        notifs = list(reversed(notifs))  # newest first

        cat_filter = self.filter_var.get()
        if cat_filter != "All":
            notifs = [n for n in notifs if n.get("category") == cat_filter]

        if not notifs:
            tk.Label(self.inner, text="No notifications here! 🎉",
                     font=("Helvetica", 11), bg=BG_DARK, fg=GRAY).pack(pady=30)
            return

        for i, n in enumerate(notifs):
            self._make_card(n, i)

    def _make_card(self, n: dict, idx: int):
        seen    = n.get("seen", False)
        cat     = n.get("category", "system")
        icon    = ns.CATEGORIES.get(cat, "🔔")
        bg      = BG_CARD if not seen else "#221800"
        fg_main = WHITE if not seen else GRAY

        card = tk.Frame(self.inner, bg=bg, padx=10, pady=8)
        card.pack(fill="x", pady=2)

        row = tk.Frame(card, bg=bg); row.pack(fill="x")
        tk.Label(row, text=icon, font=("Helvetica", 16), bg=bg).pack(side="left", padx=(0, 8))
        msg_frame = tk.Frame(row, bg=bg)
        msg_frame.pack(side="left", fill="x", expand=True)
        tk.Label(msg_frame, text=n.get("message", ""),
                 font=("Helvetica", 10, "bold" if not seen else "normal"),
                 bg=bg, fg=fg_main, wraplength=330, justify="left").pack(anchor="w")
        ts = n.get("timestamp", "")
        tk.Label(msg_frame, text=ts, font=("Helvetica", 8),
                 bg=bg, fg=GRAY).pack(anchor="w")

        if not seen:
            tk.Label(row, text="●", font=("Helvetica", 12), bg=bg, fg=TEAL).pack(side="right")

    def _mark_all(self):
        ns.mark_all_seen(self.username)
        self._load()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all your notifications?", parent=self.win):
            ns.clear_all(self.username)
            self._load()
