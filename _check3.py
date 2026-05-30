content = open('gui/booking_form.py', encoding='utf-8').read()
old = ('        confirm = messagebox.askyesno(\n'
       '            "Confirm Booking",\n'
       '            f"Vehicle: {vehicle_type}\\n"\n'
       '            f"From: {start} \u00e2\u0086\u0092 To: {end}\\n"\n'
       '            f"Distance: {distance} km{pax_txt}{surge_txt}{promo_txt}\\n"\n'
       '            f"Total Cost: \u00e2\u0082\u00b1{est_cost:.2f}{notes_txt}{sched_txt}\\n\\n"\n'
       '            "Confirm booking?"\n'
       '        )')
print('Found:', old in content)
print('Arrow repr:', repr('\u00e2\u0086\u0092'))
idx = content.find('â†')
print('Arrow in file:', repr(content[idx:idx+5]))
