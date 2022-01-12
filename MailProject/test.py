from datetime import *
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
import pytz

with open('readme.txt', 'a') as f:
    f.write('readme' + "\n")

# start = (22/Apr/2022)[12:00]

messageContent = "A new lesson for Donijah Schoenenberger has been scheduled for Monday, February 7, 2022, 05:30 PM, Eastern Time (US and Canada) accessed via this link: https://idtech.zoom.us/j/93327197987.&nbsp;<br />"
start = messageContent.index("scheduled for")
end = messageContent.index('Eastern Time')

dateLine = messageContent[start+22:end-2]

dateParts = dateLine.split()
month = dateParts[0]
day = dateParts[1] = dateParts[1].replace(',','')
year = dateParts[2] = dateParts[2].replace(',','')
timeStr = dateParts[3]
AMPM = dateParts[4]

print(dateParts)
months = ["Null", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
monthIndex = months.index(month)

if(AMPM == "PM"):
    hour = int(timeStr[:2]) + 12
else:
    hour = int(timeStr[:2])
minute = int(timeStr[-2:])

tz_NY = pytz.timezone('US/Eastern') 
calendar = GoogleCalendar('EMAIL GOES HERE')              #<--- Put email here
start = datetime(int(year),monthIndex,int(day),hour,minute+4,0,0,tz_NY)
end = datetime(int(year),monthIndex,int(day),hour+1,minute+4,0,0,tz_NY)
event = Event('Meeting',
              start=start,
              end=end)

calendar.add_event(event)
