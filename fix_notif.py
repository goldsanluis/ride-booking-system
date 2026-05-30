with open('gui/driver_dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

notif_code = '''
            import os as _os, json as _json
            _nf = _os.path.join('data', 'notifications.json')
            _notifs = _json.load(open(_nf)) if _os.path.exists(_nf) else []
            _notifs.append({'user': booking.user, 'message': f'Driver {self.driver[chr(34)]name{chr(34)]} ({self.driver[chr(34)]plate{chr(34)]}) accepted your ride!', 'booking_id': booking.booking_id, 'seen': False})
            _json.dump(_notifs, open(_nf, 'w'), indent=2)
'''

code = code.replace('self.file_manager.save_bookings(self.service.get_all_bookings())\n            self.driver_manager', notif_code + '            self.driver_manager')

with open('gui/driver_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Done!')
