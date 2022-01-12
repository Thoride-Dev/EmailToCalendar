from datetime import *
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA

from beautiful_date import Jan, Apr, hours
import pytz

tz_NY = pytz.timezone('America/New_York') 
calendar = GoogleCalendar('EMAIL GOES HERE')   #<--- Put email here
start = datetime(2022,1,11,12,0+4,0,0,tz_NY)
end = datetime(2022,1,11,14,0+4,0,0,tz_NY)
event = Event('Meeting',
              start=start,
              end=end)

calendar.add_event(event)

for event in calendar:
    print(event)