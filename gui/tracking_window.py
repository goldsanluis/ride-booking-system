"""
Real-time ride tracking window.
Shows animated progress through ride stages with ETA countdown.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
from services.tracking_service import RideTracker, get_eta_minutes

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
RED_ERR     = "#FF6B6B"   # Error / cancel red
MAP_BG      = "#3a0000"   # Slightly lighter maroon for map area


class TrackingWindow:
    def __init__(self, parent, booking, on_complete_callback=None):
        self.booking  = booking
        self.callback = on_complete_callback
        self.tracker  = None

        self.win = tk.Toplevel(parent)
        self.win.title(f"Live Tracking — Booking #{booking.booking_id}")
        self.win.geometry("480x520")
        self.win.configure(bg=BG_APP)
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build()
        self._start_tracking()

    # ── UI ──────────────────────────────────────────────────────────────────
    def _build(self):
        # Header strip
        hdr = tk.Frame(self.win, bg=MAROON, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📍 Live Ride Tracking",
                 font=("Helvetica", 14, "bold"), bg=MAROON, fg=GOLD).pack()
        tk.Label(hdr, text=f"Booking #{self.booking.booking_id}",
                 font=("Helvetica", 10), bg=MAROON, fg=TEXT_MUTED).pack()

        # Gold accent line
        tk.Frame(self.win, bg=GOLD, height=3).pack(fill="x")

        # Map placeholder (animated)
        map_frame = tk.Frame(self.win, bg=MAP_BG, height=140)
        map_frame.pack(fill="x", padx=16, pady=(14, 0))
        map_frame.pack_propagate(False)
        self.map_canvas = tk.Canvas(map_frame, bg=MAP_BG, highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True)
        self._draw_route_map()

        # Stage label
        stage_frame = tk.Frame(self.win, bg=BG_APP, pady=8)
        stage_frame.pack(fill="x", padx=16)
        self.stage_label = tk.Label(stage_frame, text="🔍 Starting...",
                                    font=("Helvetica", 13, "bold"), bg=BG_APP, fg=TEXT_WHITE)
        self.stage_label.pack()

        # Progress bar
        pb_frame = tk.Frame(self.win, bg=BG_APP, padx=16)
        pb_frame.pack(fill="x")
        self.pb_outer = tk.Frame(pb_frame, bg=BG_FIELD, height=12)
        self.pb_outer.pack(fill="x")
        self.pb_outer.pack_propagate(False)
        self.pb_inner = tk.Frame(self.pb_outer, bg=GOLD, height=12)
        self.pb_inner.place(relwidth=0.0, relheight=1.0)

        # ETA row
        eta_frame = tk.Frame(self.win, bg=BG_APP, pady=4)
        eta_frame.pack(fill="x", padx=16)
        eta_mins = get_eta_minutes(self.booking.distance)
        self.eta_label = tk.Label(eta_frame, text=f"⏱ ETA: ~{eta_mins} min",
                                  font=("Helvetica", 10), bg=BG_APP, fg=GOLD_DIM)
        self.eta_label.pack(side="left")
        self.pct_label = tk.Label(eta_frame, text="0%",
                                  font=("Helvetica", 10), bg=BG_APP, fg=TEXT_GRAY)
        self.pct_label.pack(side="right")

        # Driver info card
        info = tk.Frame(self.win, bg=BG_SURFACE, padx=16, pady=12)
        info.pack(fill="x", padx=16, pady=12)

        # Gold top border on card
        tk.Frame(info, bg=GOLD, height=2).pack(fill="x", pady=(0, 8))

        tk.Label(info, text="🚗 Your Driver",
                 font=("Helvetica", 10, "bold"), bg=BG_SURFACE, fg=GOLD).pack(anchor="w")
        tk.Label(info, text=self.booking.driver.name,
                 font=("Helvetica", 12, "bold"), bg=BG_SURFACE, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(info, text=f"🔢 {self.booking.driver.plate}  ⭐ {self.booking.driver.rating}",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(info, text=f"📍 {self.booking.start_location} → {self.booking.end_location}",
                 font=("Helvetica", 10), bg=BG_SURFACE, fg=GOLD_DIM).pack(anchor="w", pady=(4, 0))

        # Buttons
        btn_row = tk.Frame(self.win, bg=BG_APP)
        btn_row.pack(fill="x", padx=16, pady=8)
        tk.Button(btn_row, text="📞 Call Driver (simulated)",
                  font=("Helvetica", 9), bg=BG_SURFACE, fg=GOLD,
                  relief="flat", padx=10, pady=6, cursor="hand2",
                  activebackground=MAROON_LT, activeforeground=GOLD,
                  command=self._call_driver).pack(side="left", padx=(0, 8))
        self.cancel_btn = tk.Button(btn_row, text="❌ Cancel Ride",
                                    font=("Helvetica", 9), bg=RED_ERR, fg=TEXT_WHITE,
                                    relief="flat", padx=10, pady=6, cursor="hand2",
                                    activebackground=MAROON_LT,
                                    command=self._cancel)
        self.cancel_btn.pack(side="left")

    def _draw_route_map(self):
        c = self.map_canvas
        c.update_idletasks()
        w, h = 448, 130
        # Road line
        c.create_line(40, h//2, w-40, h//2, fill=BG_FIELD, width=6)
        # Gold dashed center line
        for x in range(60, w-60, 20):
            c.create_line(x, h//2, x+10, h//2, fill=GOLD, width=2)
        # Start dot (gold)
        c.create_oval(32, h//2-10, 52, h//2+10, fill=GOLD, outline="")
        c.create_text(42, h//2+22, text="A", fill=GOLD, font=("Helvetica", 9, "bold"))
        # End dot (white)
        c.create_oval(w-52, h//2-10, w-32, h//2+10, fill=TEXT_WHITE, outline="")
        c.create_text(w-42, h//2+22, text="B", fill=TEXT_WHITE, font=("Helvetica", 9, "bold"))
        # Moving car
        self.car_x = 50
        self.car_obj = c.create_text(self.car_x, h//2-4, text="🚗",
                                      font=("Helvetica", 18))
        self._animate_car(w)

    def _animate_car(self, max_w):
        self.map_canvas.coords(self.car_obj, self.car_x, 61)
        if self.car_x < max_w - 55:
            self.car_x += 1.2
            try:
                self.win.after(60, lambda: self._animate_car(max_w))
            except tk.TclError:
                pass

    # ── Tracking callbacks ───────────────────────────────────────────────────
    def _start_tracking(self):
        self.tracker = RideTracker(
            self.booking,
            on_update=self._on_update,
            on_complete=self._on_tracking_done,
        )
        self.tracker.start()

    def _on_update(self, text: str, pct: int):
        try:
            self.win.after(0, lambda: self._apply_update(text, pct))
        except tk.TclError:
            pass

    def _apply_update(self, text: str, pct: int):
        self.stage_label.config(text=text)
        self.pb_inner.place(relwidth=pct / 100)
        self.pct_label.config(text=f"{pct}%")
        color = TEXT_WHITE if pct == 100 else GOLD
        self.pb_inner.config(bg=color)

    def _on_tracking_done(self):
        try:
            self.win.after(0, self._finish_ui)
        except tk.TclError:
            pass

    def _finish_ui(self):
        self.cancel_btn.config(state="disabled")
        if self.callback:
            self.callback()

    # ── Actions ─────────────────────────────────────────────────────────────
    def _call_driver(self):
        messagebox.showinfo("Calling Driver",
                            f"Calling {self.booking.driver.name}...\n"
                            f"(Simulated — no real call placed)",
                            parent=self.win)

    def _cancel(self):
        if messagebox.askyesno("Cancel", "Cancel and close tracking?", parent=self.win):
            self._on_close()

    def _on_close(self):
        if self.tracker:
            self.tracker.stop()
        self.win.destroy()