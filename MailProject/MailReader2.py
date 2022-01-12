#modules
import imaplib
import email

#Calendar modules
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from beautiful_date import *
from datetime import *

import pytz

def createCalEvent(dateLine, name):
    dateParts = dateLine.split()
    month = dateParts[1]
    day = dateParts[2] = dateParts[2].replace(',','')
    year = dateParts[3] = dateParts[3].replace(',','')
    timeStr = dateParts[4]
    AMPM = dateParts[5]

    print(dateParts)
    months = ["Null", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthIndex = months.index(month)

    if(AMPM == "PM"):
        hour = int(timeStr[:2]) + 12
    else:
        hour = int(timeStr[:2])
    minute = int(timeStr[-2:])

    tz_NY = pytz.timezone('US/Eastern') 
    calendar = GoogleCalendar('EMAIL GOES HERE')
    start = datetime(int(year),monthIndex,int(day),hour,minute+4,0,0,tz_NY)
    end = datetime(int(year),monthIndex,int(day),hour+1,minute+4,0,0,tz_NY)
    event = Event("Lesson With: " + name,
                start=start,
                end=end)

    calendar.add_event(event)


with open('loggedLessons.txt', 'a') as f:
    f.write('\n//----------//\n')

#credentials
username ="EMAIL GOES HERE"

#generated app password
app_password= "Your email or app password here"

# https://www.systoolsgroup.com/imap/
gmail_host= 'imap.gmail.com'

#set connection
mail = imaplib.IMAP4_SSL(gmail_host)

#login
mail.login(username, app_password)

#select inbox
mail.select("INBOX")

#select specific mails
_, selected_mails = mail.search(None, '(FROM "do-not-reply@idtechnotifications.com")')

#total number of mails from specific user
print("Total Messages from do-not-reply@idtechnotifications.com:" , len(selected_mails[0].split()))

for num in selected_mails[0].split():
    _, data = mail.fetch(num , '(RFC822)')
    _, bytes_data = data[0]

    #convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)

    for part in email_message.walk():
        if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
            message = part.get_payload(decode=True)
            #print("Message: \n", message.decode())
            messageContent = message.decode()
            if("scheduled for" in messageContent):
                start = messageContent.index("scheduled for")
                end = messageContent.index('Eastern Time')                      #this could be an issue ?

                dateLine = messageContent[start+14:end-2]

                start = messageContent.index("lesson for")
                end = messageContent.index('has been')
                name = messageContent[start+11:end-1]
            break
    
    with open('loggedLessons.txt') as f:
        if (email_message["date"] not in f.read()):
            with open('loggedLessons.txt', 'a') as f2:
                f2.write(email_message["date"] + "\n")
                createCalEvent(dateLine, name)
        else:
            print("date exists")


