with open('ride-booking-system-main/gui/driver_dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

bad = "_notifs.append({'user': booking.user, 'message': f'Driver {self.driver[chr(34)]name{chr(34)]} ({self.driver[chr(34)]plate{chr(34)]}) accepted your ride!', 'booking_id': booking.booking_id, 'seen': False})"

good = "_notifs.append({'user': booking.user, 'message': 'Driver ' + self.driver['name'] + ' (' + self.driver['plate'] + ') accepted your ride!', 'booking_id': booking.booking_id, 'seen': False})"

code = code.replace(bad, good)

with open('ride-booking-system-main/gui/driver_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Fixed!')
