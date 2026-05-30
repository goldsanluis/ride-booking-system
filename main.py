"""
main.py
-------
Application entry point.
Launches the main role-selection menu and starts the Tkinter event loop.
"""

from gui.main_menu import MainMenu

if __name__ == "__main__":
    # Create and run the role-selection screen (Passenger / Driver)
    menu = MainMenu()
    menu.run()
