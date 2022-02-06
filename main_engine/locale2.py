import locale
from datetime import date, datetime, time

d = date(2007, 3, 1)

time = d.strftime("%a, %d %B %Y")
# Sun, 23 Oct 2005 20:38:56
print(time)
locale.setlocale(category=locale.LC_ALL, locale="id_ID")  # swedish
# 'sv_SE'
time = d.strftime("%a, %d %B %Y")
# sön, 23 okt 2005 20:39:15
print(time)
