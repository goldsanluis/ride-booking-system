"""gui/wallet_panel.py
-----------------------

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"

NOTE: The wallet UI is now embedded directly inside BookingForm so that
      the booking form and wallet share a single scrollable panel with no
      dividing scrollbar.  This file is kept for backwards compatibility
      in case anything still imports WalletPanel; it simply provides a
      no-op frame that takes up no visible space.
"""

import tkinter as tk


class WalletPanel:
    """Stub — wallet UI lives inside BookingForm._build() as of the refactor."""

    def __init__(self, parent, account, account_manager):
        self.account         = account
        self.account_manager = account_manager
        # Invisible zero-height frame so existing layout code doesn't crash.
        self.frame = tk.Frame(parent, bg="#1a0000", height=0)

    def refresh_balance(self):
        """No-op: call BookingForm._refresh_balance() instead."""
        pass

    def add_money(self):
        """No-op: handled by BookingForm._add_money() instead."""
        pass