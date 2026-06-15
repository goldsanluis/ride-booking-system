"""
Payment Methods management window.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import tkinter as tk
from tkinter import messagebox
import services.payment_service as ps

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
RED_ERR     = "#FF6B6B"   # Error / delete red

SUPPORTED = [
    ("wallet", "💳 Ride Wallet",   "Built-in"),
    ("gcash",  "📱 GCash",         "e-Wallet"),
    ("maya",   "💜 Maya",          "e-Wallet"),
    ("card",   "💳 Credit/Debit",  "Bank Card"),
    ("cash",   "💵 Cash on Ride",  "Pay driver directly"),
]


class PaymentMethodsWindow:
    def __init__(self, parent, username):
        self.username = username

        self.win = tk.Toplevel(parent)
        self.win.title("💳 Payment Methods")
        self.win.geometry("440x540")
        self.win.configure(bg=BG_APP)
        self.win.resizable(False, True)
        self.win.grab_set()

        self._build()
        self._load()

    def _build(self):
        # Header strip
        hdr = tk.Frame(self.win, bg=MAROON, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="💳  Payment Methods",
                 font=("Helvetica", 14, "bold"), bg=MAROON, fg=GOLD).pack()

        # Gold accent line
        tk.Frame(self.win, bg=GOLD, height=3).pack(fill="x")

        # Saved methods section
        tk.Label(self.win, text="Your Payment Methods",
                 font=("Helvetica", 11, "bold"), bg=BG_APP, fg=GOLD).pack(anchor="w", padx=14, pady=(10, 2))

        list_frame = tk.Frame(self.win, bg=BG_APP)
        list_frame.pack(fill="x", padx=14)
        self.methods_frame = list_frame

        # Divider
        tk.Frame(self.win, bg=MAROON_LT, height=1).pack(fill="x", padx=14, pady=(8, 0))

        # Add method section
        tk.Label(self.win, text="Add a Payment Method",
                 font=("Helvetica", 11, "bold"), bg=BG_APP, fg=GOLD).pack(anchor="w", padx=14, pady=(12, 4))

        add_frame = tk.Frame(self.win, bg=BG_SURFACE, padx=12, pady=10)
        add_frame.pack(fill="x", padx=14)

        # Gold top border on card
        tk.Frame(add_frame, bg=GOLD, height=2).pack(fill="x", pady=(0, 8))

        self.add_type_var = tk.StringVar(value="gcash")
        for mtype, label, hint in SUPPORTED[1:]:  # skip wallet
            row = tk.Frame(add_frame, bg=BG_SURFACE)
            row.pack(fill="x", pady=2)
            tk.Radiobutton(row, text=label, variable=self.add_type_var, value=mtype,
                           bg=BG_SURFACE, fg=TEXT_WHITE, selectcolor=BG_FIELD,
                           activebackground=BG_SURFACE, activeforeground=GOLD,
                           font=("Helvetica", 10)).pack(side="left")
            tk.Label(row, text=hint, font=("Helvetica", 8),
                     bg=BG_SURFACE, fg=TEXT_MUTED).pack(side="left", padx=8)

        tk.Label(add_frame, text="Nickname / Account label:",
                 font=("Helvetica", 9), bg=BG_SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(8, 2))
        self.label_entry = tk.Entry(add_frame, font=("Helvetica", 10),
                                    bg=BG_FIELD, fg=TEXT_WHITE, insertbackground=GOLD,
                                    relief="flat", bd=4)
        self.label_entry.pack(fill="x")

        tk.Button(add_frame, text="➕ Add Method",
                  font=("Helvetica", 10, "bold"), bg=GOLD, fg=BG_APP,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  activebackground=MAROON_LT, activeforeground=GOLD,
                  command=self._add).pack(pady=(10, 0))

    def _load(self):
        for w in self.methods_frame.winfo_children():
            w.destroy()

        methods = ps.get_methods(self.username)
        non_wallet = [m for m in methods if m["type"] != "wallet"]

        # Always show wallet first
        wallet = next((m for m in methods if m["type"] == "wallet"), None)
        if wallet:
            self._make_row(wallet, None, is_wallet=True)

        if not non_wallet:
            tk.Label(self.methods_frame, text="No extra methods added yet.",
                     font=("Helvetica", 9), bg=BG_APP, fg=TEXT_GRAY).pack(anchor="w", pady=4)
            return

        for i, m in enumerate(non_wallet):
            self._make_row(m, i)

    def _make_row(self, m: dict, idx, is_wallet=False):
        icon = ps.PAYMENT_ICONS.get(m["type"], "💳")
        card = tk.Frame(self.methods_frame, bg=BG_SURFACE, padx=10, pady=8)
        card.pack(fill="x", pady=2)

        # Left gold accent bar for default
        if m.get("default"):
            tk.Frame(card, bg=GOLD, width=4).pack(side="left", fill="y", padx=(0, 8))

        tk.Label(card, text=f"{icon}  {m['label']}",
                 font=("Helvetica", 11, "bold"), bg=BG_SURFACE, fg=TEXT_WHITE).pack(side="left")

        if m.get("default"):
            tk.Label(card, text="✅ Default",
                     font=("Helvetica", 9), bg=BG_SURFACE, fg=GOLD_DIM).pack(side="left", padx=8)

        if not is_wallet:
            btn_frame = tk.Frame(card, bg=BG_SURFACE)
            btn_frame.pack(side="right")
            if not m.get("default"):
                tk.Button(btn_frame, text="Set Default",
                          font=("Helvetica", 8), bg=GOLD, fg=BG_APP,
                          relief="flat", padx=6, pady=2, cursor="hand2",
                          activebackground=MAROON_LT, activeforeground=GOLD,
                          command=lambda i=idx: self._set_default(i)).pack(side="left", padx=4)
            tk.Button(btn_frame, text="🗑",
                      font=("Helvetica", 9), bg=RED_ERR, fg=TEXT_WHITE,
                      relief="flat", padx=6, pady=2, cursor="hand2",
                      activebackground=MAROON_LT,
                      command=lambda i=idx: self._remove(i)).pack(side="left")

    def _add(self):
        mtype = self.add_type_var.get()
        label = self.label_entry.get().strip()
        if not label:
            messagebox.showerror("Error", "Please enter a nickname for this method.", parent=self.win)
            return
        ok, msg = ps.add_method(self.username, mtype, label)
        if ok:
            self.label_entry.delete(0, tk.END)
            self._load()
            messagebox.showinfo("Added!", msg, parent=self.win)
        else:
            messagebox.showerror("Error", msg, parent=self.win)

    def _set_default(self, idx):
        methods = ps.get_methods(self.username)
        non_wallet = [m for m in methods if m["type"] != "wallet"]
        if 0 <= idx < len(non_wallet):
            global_idx = methods.index(non_wallet[idx])
            ps.set_default(self.username, global_idx)
            self._load()

    def _remove(self, idx):
        if messagebox.askyesno("Remove", "Remove this payment method?", parent=self.win):
            methods = ps.get_methods(self.username)
            non_wallet = [m for m in methods if m["type"] != "wallet"]
            if 0 <= idx < len(non_wallet):
                global_idx = methods.index(non_wallet[idx])
                ps.remove_method(self.username, global_idx)
                self._load()