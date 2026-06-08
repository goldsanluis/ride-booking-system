"""
main.py
-------
Application entry point.
Launches the main role-selection menu and starts the Tkinter event loop.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import sys
import tkinter as tk
from tkinter import messagebox


def main():
    """Entry point — create the role-selection menu and start the event loop."""
    from gui.main_menu import MainMenu
    menu = MainMenu()
    menu.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Show a friendly error dialog instead of a bare traceback on crash.
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Unexpected Error",
                f"The application encountered an error and needs to close.\n\n{e}"
            )
            root.destroy()
        except Exception:
            print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)