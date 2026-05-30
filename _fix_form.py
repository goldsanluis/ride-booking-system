content = open('gui/booking_form.py', encoding='utf-8').read()
arrow = '\u00e2\u0086\u0092'
peso  = '\u00e2\u0082\u00b1'
old = ('        confirm = messagebox.askyesno(\n'
       '            "Confirm Booking",\n'
       '            f"Vehicle: {vehicle_type}\\n"\n'
       '            f"From: {start} ' + arrow + ' To: {end}\\n"\n'
       '            f"Distance: {distance} km{pax_txt}{surge_txt}{promo_txt}\\n"\n'
       '            f"Total Cost: ' + peso + '{est_cost:.2f}{notes_txt}{sched_txt}\\n\\n"\n'
       '            "Confirm booking?"\n'
       '        )')
new = ('        from models.driver import Driver as _Driver\n'
       '        preview_driver = _Driver.get_random_driver()\n'
       '        driver_preview_txt = (\n'
       '            f"\\n\\nDriver: {preview_driver.name}"\n'
       '            f"\\nPlate: {preview_driver.plate}"\n'
       '            f"\\nRating: {preview_driver.rating} stars")\n'
       '        confirm = messagebox.askyesno(\n'
       '            "Confirm Booking",\n'
       '            f"Vehicle: {vehicle_type}\\n"\n'
       '            f"From: {start} ' + arrow + ' To: {end}\\n"\n'
       '            f"Distance: {distance} km{pax_txt}{surge_txt}{promo_txt}\\n"\n'
       '            f"Total Cost: ' + peso + '{est_cost:.2f}{notes_txt}{sched_txt}"\n'
       '            f"{driver_preview_txt}\\n\\n"\n'
       '            "Confirm booking?"\n'
       '        )')
if old in content:
    open('gui/booking_form.py', 'w', encoding='utf-8').write(content.replace(old, new))
    print('SUCCESS')
else:
    print('NOT FOUND')
