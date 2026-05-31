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


from gui.main_menu import MainMenu

if __name__ == "__main__":
    # Create and run the role-selection screen (Passenger / Driver)
    menu = MainMenu()
    menu.run()
