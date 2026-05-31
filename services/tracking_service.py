"""
Simulated real-time ride tracking service.
Since this is a local desktop app, tracking is simulated with timed status updates.

author = "Ghani Regina Gold San Luis"
group = "Group 6"
course = "CMPE 103 - Object Oriented Programming"
school = "Polytechnic University of the Philippines"
github = "https://github.com/your-username/ride-booking-system"
"""

import threading, time, random
from datetime import datetime

RIDE_STAGES = [
    ("🔍 Finding your driver...",       5),
    ("✅ Driver confirmed!",             3),
    ("🚗 Driver is on the way",          8),
    ("📍 Driver is nearby",              5),
    ("🎉 Driver has arrived!",           4),
    ("🚦 Ride in progress...",           10),
    ("✅ Almost at destination",         5),
]


class RideTracker:
    """
    Simulates live tracking for a single booking.
    Calls `on_update(stage_text, progress_pct)` on each stage change.
    Calls `on_complete()` when simulation ends.
    """
    def __init__(self, booking, on_update, on_complete):
        self.booking     = booking
        self.on_update   = on_update
        self.on_complete = on_complete
        self._thread     = None
        self._stop_evt   = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_evt.set()

    def _run(self):
        total_time = sum(s[1] for s in RIDE_STAGES)
        elapsed    = 0
        for i, (text, secs) in enumerate(RIDE_STAGES):
            if self._stop_evt.is_set():
                break
            pct = int((elapsed / total_time) * 100)
            self.on_update(text, pct)
            # Sleep in small increments so stop() is responsive
            for _ in range(secs * 4):
                if self._stop_evt.is_set():
                    return
                time.sleep(0.25)
            elapsed += secs
        if not self._stop_evt.is_set():
            self.on_update("✅ Ride complete! Please rate your driver.", 100)
            self.on_complete()


def get_eta_minutes(distance_km: float) -> int:
    """Rough ETA: assume 30 km/h average in city traffic."""
    return max(5, int((distance_km / 30) * 60))
