# 🚗 Ride Booking System

A desktop ride-booking application built with Python and Tkinter, featuring separate interfaces for passengers, drivers, and administrators.

---

## Features

### Passenger
- **Book a ride** — choose between Car, Van, or Bike with real-time fare estimates
- **Scheduled rides** — book in advance for a future date and time
- **Surge pricing** — automatic 1.5× multiplier during peak hours (7–9 AM and 5–8 PM)
- **Promo codes** — apply discount codes at checkout (flat or percentage-based)
- **Favorite routes** — save and reuse frequently travelled routes
- **Live tracking** — animated ride progress window with ETA countdown
- **Wallet** — in-app balance for paying rides and topping up
- **Payment methods** — manage saved payment options
- **Notifications** — real-time notification center with unread badge
- **Booking history** — view, cancel, complete, and rate past rides

### Driver
- **Driver dashboard** — view and accept assigned bookings
- **Earnings tracker** — monitor ride income over time
- **Profile management** — update driver details and view rating
- **Separate login** — dedicated login flow for driver accounts

### Admin
- **User management** — view and manage registered passenger accounts
- **Driver management** — add or remove drivers
- **Booking statistics** — overview of all system bookings
- **Promo management** — create and delete custom promo codes
- **Broadcast notifications** — send messages to all users

---

## Project Structure

```
ride-booking-system/
├── main.py                     # Entry point
├── data/
│   ├── accounts.json           # Passenger accounts
│   ├── bookings.json           # All bookings
│   ├── drivers.json            # Driver accounts
│   ├── favorites.json          # Per-user saved routes
│   └── notifications.json      # Notification records
├── models/
│   ├── account.py              # Passenger account model
│   ├── booking.py              # Booking model (cost, surge, status)
│   ├── driver.py               # Driver model
│   ├── vehicle.py              # Base vehicle class
│   ├── car.py                  # Car: ₱40 base + ₱14/km, capacity 4
│   ├── van.py                  # Van: ₱80 base + ₱20/km, capacity 10
│   └── bike.py                 # Bike: ₱20 base + ₱8/km, capacity 1
├── services/
│   ├── booking_service.py      # Booking creation and retrieval logic
│   ├── promo_service.py        # Promo code validation and management
│   ├── notification_service.py # Notification read/write logic
│   ├── tracking_service.py     # Ride stage simulation and ETA
│   ├── wallet_service.py       # Wallet top-up and deductions
│   └── payment_service.py      # Payment method management
├── file_handler/
│   ├── file_manager.py         # Bookings and favorites persistence
│   ├── account_manager.py      # Account registration and login
│   └── driver_manager.py       # Driver persistence
└── gui/
    ├── main_menu.py            # App entry — routes to login
    ├── login_window.py         # Passenger login and registration
    ├── driver_login.py         # Driver login screen
    ├── main_window.py          # Main passenger dashboard
    ├── booking_form.py         # Ride booking form
    ├── booking_list.py         # Booking history and actions
    ├── driver_dashboard.py     # Driver rides, earnings, profile
    ├── admin_dashboard.py      # Admin control panel
    ├── tracking_window.py      # Live ride tracking UI
    ├── notification_center.py  # Notification inbox
    ├── payment_methods_window.py # Payment method management
    └── wallet_panel.py         # Wallet balance display
```

---

## Getting Started

### Requirements

- Python 3.8+
- Tkinter (included with most Python installations)

No third-party packages are required.

### Installation

```bash
git clone https://github.com/your-username/ride-booking-system.git
cd ride-booking-system
```

### Running the App

```bash
python main.py
```

---

## Default Credentials

### Passenger
Register a new account from the login screen, or use the pre-seeded account:

| Username | Password |
|----------|----------|
| `gold`   | `gold`   |

### Driver

| Username | Password      | Name           |
|----------|---------------|----------------|
| `driver` | `password123` | Juan dela Cruz |
| `maria`  | `password123` | Maria Santos   |
| `pedro`  | `password123` | Pedro Reyes    |

### Admin

| Username | Password   |
|----------|------------|
| `admin`  | `admin123` |

---

## Fare Structure

| Vehicle | Base Fare | Per km | Capacity |
|---------|-----------|--------|----------|
| Bike    | ₱20       | ₱8     | 1        |
| Car     | ₱40       | ₱14    | 4        |
| Van     | ₱80       | ₱20    | 10       |

> **Surge pricing:** fares are multiplied by **1.5×** during peak hours (7–9 AM and 5–8 PM). Scheduled rides are exempt from surge pricing.

---

## Built-in Promo Codes

| Code       | Discount                        | Minimum Fare |
|------------|---------------------------------|--------------|
| `RIDE10`   | ₱10 off                         | ₱50          |
| `RIDE50`   | ₱50 off                         | ₱200         |
| `SAVE20`   | 20% off                         | ₱100         |
| `NEWUSER`  | ₱80 welcome discount            | None         |
| `VANRIDE`  | ₱100 off Van rides              | ₱300         |
| `PEAKHOUR` | 10% surge relief                | None         |

Admins can add and remove custom promo codes from the Admin Dashboard.

---

## Data Storage

All data is stored locally as JSON files in the `data/` directory. No database or internet connection is required.

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.
