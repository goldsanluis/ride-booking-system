content = open('gui/booking_form.py', encoding='utf-8').read()
idx = content.find('Confirm Booking')
print(repr(content[idx-20:idx+300]))
