# TODO

- [x] Add BookingService.save_bookings() helper (wrap FileManager.save_bookings(self.bookings)).
- [x] Add BookingService.activate_booking(booking_id, username) with required validations, call booking.activate(), then self.save_bookings(), and return success/error string.

- [x] Update gui/booking_list.py BookingList._activate() to call service.activate_booking(...), show showerror on failure and showinfo on success, and refresh UI.

- [x] Ensure only updated methods are changed/returned per request.



