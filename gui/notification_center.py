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
BG_APP      = "#1a0000"
BG_SURFACE  = "#800000"
BG_FIELD    = "#6b0000"
MAROON      = "#800000"
MAROON_LT   = "#990000"
GOLD        = "#FFD700"
GOLD_DIM    = "#FFC200"
TEXT_WHITE  = "#FFFFFF"
TEXT_MUTED  = "#FFEECC"
TEXT_GRAY   = "#cc9966"
RED_ERR     = "#FF6B6B"


class NotificationCenter:
    def __init__(self, parent, username):
        self.username = username

        self.win = tk.Toplevel(parent)
        self.win.title("🔔 Notification Center")
        self.win.configure(bg=BG_APP)

        width = 550
        height = 650

        screen_w = self.win.winfo_screenwidth()
        screen_h = self.win.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        self.win.geometry(f"{width}x{height}+{x}+{y}")
        self.win.minsize(600, 500)
        self.win.resizable(True, True)

        self.win.grab_set()

        self._build()
        self._load()

    # ─────────────────────────────────────────────
    # UI BUILD
    # ─────────────────────────────────────────────
    def _build(self):
        hdr = tk.Frame(self.win, bg=MAROON, pady=12)
        hdr.pack(fill="x")

        tk.Label(
            hdr,
            text="🔔  Notification Center",
            font=("Helvetica", 14, "bold"),
            bg=MAROON,
            fg=GOLD
        ).pack(side="left", padx=14)

        btn_frame = tk.Frame(hdr, bg=MAROON)
        btn_frame.pack(side="right", padx=10)

        tk.Button(
            btn_frame,
            text="✅ Mark All Read",
            font=("Helvetica", 9),
            bg=GOLD,
            fg=BG_APP,
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=GOLD,
            command=self._mark_all
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame,
            text="🗑 Clear All",
            font=("Helvetica", 9),
            bg=RED_ERR,
            fg=TEXT_WHITE,
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2",
            activebackground=MAROON_LT,
            activeforeground=TEXT_WHITE,
            command=self._clear_all
        ).pack(side="left")

        tk.Frame(self.win, bg=GOLD, height=3).pack(fill="x")

        # ─────────────────────────────────────────────
        # FILTER ROW (UNCHANGED)
        # ─────────────────────────────────────────────
        filt = tk.Frame(self.win, bg=BG_SURFACE, pady=6, padx=10)
        filt.pack(fill="x")

        tk.Label(
            filt,
            text="Filter:",
            font=("Helvetica", 9, "bold"),
            bg=BG_SURFACE,
            fg=GOLD
        ).pack(side="left")

        self.filter_var = "All"
        self.filter_buttons = {}

        for cat in ["All", "ride", "payment", "promo", "driver", "refund", "system"]:
            lbl = cat.title() if cat != "All" else "All"

            btn = tk.Button(
                filt,
                text=lbl,
                bg=BG_SURFACE,
                fg=GOLD if cat == "All" else TEXT_WHITE,
                relief="flat",
                bd=0,
                highlightthickness=0,
                activebackground=BG_SURFACE,
                activeforeground=GOLD,
                font=("Helvetica", 10),
                cursor="hand2",
                command=lambda c=cat: self._set_filter(c)
            )

            btn.pack(side="left", padx=12)
            self.filter_buttons[cat] = btn

        # ─────────────────────────────────────────────
        # SCROLL AREA (ONLY PART CHANGED)
        # ─────────────────────────────────────────────
        outer = tk.Frame(self.win, bg=BG_APP)
        outer.pack(fill="both", expand=True, padx=10, pady=6)

        self.canvas = tk.Canvas(outer, bg=BG_APP, highlightthickness=0)

        self.scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self._on_scroll)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=BG_APP)

        self.win_id = self.canvas.create_window(
            (0, 0),
            window=self.inner,
            anchor="nw"
        )

        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    # ─────────────────────────────────────────────
    # SCROLL LOGIC (FIXED ONLY HERE)
    # ─────────────────────────────────────────────
    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._toggle_scrollbar()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.win_id, width=event.width)

    def _on_scroll(self, first, last):
        self.scrollbar.set(first, last)
        self._toggle_scrollbar()

    def _toggle_scrollbar(self):
        first, last = self.canvas.yview()

        # Show only if needed
        if first <= 0.0 and last >= 1.0:
            self.scrollbar.pack_forget()
        else:
            if not self.scrollbar.winfo_ismapped():
                self.scrollbar.pack(side="right", fill="y")

    # ─────────────────────────────────────────────
    # FILTER + LOAD (UNCHANGED)
    # ─────────────────────────────────────────────
    def _set_filter(self, category):
        self.filter_var = category

        for cat, btn in self.filter_buttons.items():
            btn.config(fg=GOLD if cat == category else TEXT_WHITE)

        self._load()

    def _load(self):
        for w in self.inner.winfo_children():
            w.destroy()

        notifs = ns.get_for_user(self.username)
        notifs = list(reversed(notifs))

        if self.filter_var != "All":
            notifs = [n for n in notifs if n.get("category") == self.filter_var]

        if not notifs:
            tk.Label(
                self.inner,
                text="No notifications here! 🎉",
                font=("Helvetica", 11),
                bg=BG_APP,
                fg=TEXT_MUTED
            ).pack(pady=30)
            return

        for i, n in enumerate(notifs):
            self._make_card(n, i)

    def _make_card(self, n: dict, idx: int):
        seen = n.get("seen", False)
        cat = n.get("category", "system")
        icon = ns.CATEGORIES.get(cat, "🔔")

        bg = BG_SURFACE if not seen else BG_FIELD
        fg_main = TEXT_WHITE if not seen else TEXT_MUTED

        card = tk.Frame(self.inner, bg=bg, padx=10, pady=8)
        card.pack(fill="x", pady=2)

        if not seen:
            tk.Frame(card, bg=GOLD, width=4).pack(side="left", fill="y", padx=(0, 8))

        row = tk.Frame(card, bg=bg)
        row.pack(fill="x")

        tk.Label(row, text=icon, font=("Helvetica", 16), bg=bg).pack(side="left", padx=(0, 8))

        msg_frame = tk.Frame(row, bg=bg)
        msg_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            msg_frame,
            text=n.get("message", ""),
            font=("Helvetica", 10, "bold" if not seen else "normal"),
            bg=bg,
            fg=fg_main,
            wraplength=330,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            msg_frame,
            text=n.get("timestamp", ""),
            font=("Helvetica", 8),
            bg=bg,
            fg=TEXT_GRAY
        ).pack(anchor="w")

        if not seen:
            tk.Label(row, text="●", font=("Helvetica", 12), bg=bg, fg=GOLD).pack(side="right")

    def _mark_all(self):
        ns.mark_all_seen(self.username)
        self._load()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all your notifications?", parent=self.win):
            ns.clear_all(self.username)
            self._load()