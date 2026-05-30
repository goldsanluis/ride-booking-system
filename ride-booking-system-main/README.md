# 🚗 Ride Booking System

A desktop ride-booking application built with Python and Tkinter. It supports two user roles — **Passenger** and **Driver** — with a gold-themed GUI, fare calculation, surge pricing, and persistent JSON-based storage.

---

## Features

- **Dual-role login** — separate flows for Passengers and Drivers
- **Vehicle selection** — choose between Bike, Car, or Van, each with its own base fare and per-km rate
- **Surge pricing** — fares are automatically multiplied during peak hours (7–9 AM and 5–8 PM)
- **Random driver assignment** — a driver is assigned automatically when a booking is created
- **Booking management** — view, cancel, complete, and rate your bookings
- **Driver dashboard** — drivers can view active bookings and accept rides
- **Persistent storage** — bookings and accounts are saved locally as JSON files

---

## Project Structure

```
ride-booking-system-main/
├── main.py                        # Entry point
├── data/
│   ├── accounts.json              # Passenger accounts
│   ├── bookings.json              # All bookings
│   └── drivers.json               # Driver accounts
├── models/
│   ├── account.py                 # Passenger account model
│   ├── driver.py                  # Driver model with random assignment pool
│   ├── booking.py                 # Booking model (cost, surge, status, rating)
│   ├── vehicle.py                 # Base vehicle class
│   ├── car.py                     # Car — ₱40 base + ₱14/km, capacity 4
│   ├── van.py                     # Van — ₱80 base + ₱20/km, capacity 10
│   └── bike.py                    # Bike — ₱20 base + ₱8/km, capacity 1
├── services/
│   └── booking_service.py         # Business logic for booking operations
├── file_handler/
│   ├── file_manager.py            # Load/save bookings to JSON
│   ├── account_manager.py         # Load/save passenger accounts
│   └── driver_manager.py          # Load/save driver accounts
└── gui/
    ├── main_menu.py               # Role selection screen (Passenger / Driver)
    ├── login_window.py            # Passenger login & registration
    ├── driver_login.py            # Driver login screen
    ├── main_window.py             # Passenger main screen
    ├── booking_form.py            # New booking form
    ├── booking_list.py            # Booking history & actions
    └── driver_dashboard.py        # Driver's active bookings view
```

---

## Getting Started

### Requirements

- Python 3.8+
- Tkinter (included with most Python installations)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ride-booking-system.git
cd ride-booking-system

# No external dependencies required — run directly
python main.py
```

---

## Usage

### Passenger

1. Select **Passenger** on the main menu.
2. Log in with an existing account or register a new one.
3. Fill in the booking form: pick-up location, destination, distance, and vehicle type.
4. View your bookings in the list on the right — cancel, complete, or rate them.

**Default test account**

| Username | Password |
|----------|----------|
| `gold`   | `gold`   |

### Driver

1. Select **Driver** on the main menu.
2. Log in with a driver account.
3. View active bookings from the dashboard and accept rides.

**Default driver accounts**

| Username | Password      |
|----------|---------------|
| `driver` | `password123` |
| `Drixx`  | `drixx`       |

---

## Pricing

| Vehicle | Base Fare | Per km  | Capacity |
|---------|-----------|---------|----------|
| Bike    | ₱20       | ₱8/km   | 1        |
| Car     | ₱40       | ₱14/km  | 4        |
| Van     | ₱80       | ₱20/km  | 10       |

**Surge pricing** applies a **1.5× multiplier** during peak hours:
- Morning: 7:00 AM – 9:00 AM
- Evening: 5:00 PM – 8:00 PM

---

## Data Storage

All data is stored locally under the `data/` directory as JSON files. The folder and files are created automatically on first run.

| File               | Contents                  |
|--------------------|---------------------------|
| `accounts.json`    | Passenger user accounts   |
| `drivers.json`     | Driver accounts           |
| `bookings.json`    | All booking records       |

---

## License

This project is licensed under the terms found in [LICENSE](LICENSE).
