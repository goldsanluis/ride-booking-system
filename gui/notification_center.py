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
TEXT_GRAY   = "#cc9966"   # Muted brownish gray
RED_ERR     = "#FF6B6B"   # Error / clear red


class NotificationCenter:
    def __init__(self, parent, username):
        self.username = username

        self.win = tk.Toplevel(parent)
        self.win.title("🔔 Notification Center")
        self.win.geometry("480x560")
        self.win.configure(bg=BG_APP)
        self.win.resizable(False, True)
        self.win.grab_set()

        self._build()
        self._load()

    def _build(self):
        # Header strip
        hdr = tk.Frame(self.win, bg=MAROON, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔔  Notification Center",
                 font=("Helvetica", 14, "bold"), bg=MAROON, fg=GOLD).pack(side="left", padx=14)

        btn_frame = tk.Frame(hdr, bg=MAROON)
        btn_frame.pack(side="right", padx=10)
        tk.Button(btn_frame, text="✅ Mark All Read",
                  font=("Helvetica", 9), bg=GOLD, fg=BG_APP, relief="flat",
                  padx=8, pady=3, cursor="hand2",
                  activebackground=MAROON_LT, activeforeground=GOLD,
                  command=self._mark_all).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑 Clear All",
                  font=("Helvetica", 9), bg=RED_ERR, fg=TEXT_WHITE, relief="flat",
                  padx=8, pady=3, cursor="hand2",
                  activebackground=MAROON_LT, activeforeground=TEXT_WHITE,
                  command=self._clear_all).pack(side="left")

        # Gold accent line
        tk.Frame(self.win, bg=GOLD, height=3).pack(fill="x")

        # Filter row
        filt = tk.Frame(self.win, bg=BG_SURFACE, pady=6, padx=10)
        filt.pack(fill="x")
        tk.Label(filt, text="Filter:", font=("Helvetica", 9, "bold"),
                 bg=BG_SURFACE, fg=GOLD).pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        for cat in ["All", "ride", "payment", "promo", "driver", "refund", "system"]:
            icon = ns.CATEGORIES.get(cat, "📌")
            lbl  = f"{icon} {cat.title()}" if cat != "All" else "All"
            tk.Radiobutton(filt, text=lbl, variable=self.filter_var, value=cat,
                           bg=BG_SURFACE, fg=TEXT_WHITE, selectcolor=BG_FIELD,
                           activebackground=BG_SURFACE, activeforeground=GOLD,
                           font=("Helvetica", 8),
                           command=self._load).pack(side="left", padx=4)

        # Scrollable list
        outer = tk.Frame(self.win, bg=BG_APP)
        outer.pack(fill="both", expand=True, padx=10, pady=6)
        self.canvas = tk.Canvas(outer, bg=BG_APP, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=BG_APP)
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
                     font=("Helvetica", 11), bg=BG_APP, fg=TEXT_MUTED).pack(pady=30)
            return

        for i, n in enumerate(notifs):
            self._make_card(n, i)

    def _make_card(self, n: dict, idx: int):
        seen    = n.get("seen", False)
        cat     = n.get("category", "system")
        icon    = ns.CATEGORIES.get(cat, "🔔")
        bg      = BG_SURFACE if not seen else BG_FIELD
        fg_main = TEXT_WHITE if not seen else TEXT_MUTED

        card = tk.Frame(self.inner, bg=bg, padx=10, pady=8)
        card.pack(fill="x", pady=2)

        # Left gold accent bar for unread
        if not seen:
            tk.Frame(card, bg=GOLD, width=4).pack(side="left", fill="y", padx=(0, 8))

        row = tk.Frame(card, bg=bg)
        row.pack(fill="x")
        tk.Label(row, text=icon, font=("Helvetica", 16), bg=bg).pack(side="left", padx=(0, 8))
        msg_frame = tk.Frame(row, bg=bg)
        msg_frame.pack(side="left", fill="x", expand=True)
        tk.Label(msg_frame, text=n.get("message", ""),
                 font=("Helvetica", 10, "bold" if not seen else "normal"),
                 bg=bg, fg=fg_main, wraplength=330, justify="left").pack(anchor="w")
        ts = n.get("timestamp", "")
        tk.Label(msg_frame, text=ts, font=("Helvetica", 8),
                 bg=bg, fg=TEXT_GRAY).pack(anchor="w")

        if not seen:
            tk.Label(row, text="●", font=("Helvetica", 12), bg=bg, fg=GOLD).pack(side="right")

    def _mark_all(self):
        ns.mark_all_seen(self.username)
        self._load()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all your notifications?", parent=self.win):
            ns.clear_all(self.username)
            self._load()