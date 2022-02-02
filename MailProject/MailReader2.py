#modules
import imaplib
import email

#Calendar modules
from gcsa.event import Event as ev
from gcsa.google_calendar import GoogleCalendar
from beautiful_date import *
from datetime import *

import pytz
import tkinter as tk
from tkinter import Label, Entry, Button


m = tk.Tk()
emailLink = ""
password = ""


def createCalEvent(dateLine, name, emailToUse):
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
    calendar = GoogleCalendar(emailToUse)
    start = datetime(int(year),monthIndex,int(day),hour,minute+4,0,0,tz_NY)
    end = datetime(int(year),monthIndex,int(day),hour+1,minute+4,0,0,tz_NY)
    event = ev("Lesson With: " + name,
                start=start,
                end=end)

    calendar.add_event(event)



def checkMail():
    
    emailLink = em.get()
    password = pw.get()
    interval = iv.get()
    interval = int(interval)
    

    #credentials
    username = emailLink

    #generated app password
    app_password = password

    # https://www.systoolsgroup.com/imap/
    gmail_host= 'imap.gmail.com'

    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)

    #login
    
    try:
        mail.login(username, app_password)
    except:
        errorText = Label(m, text="Invalid Email or Password!", bg="red")
        errorText.grid(row=3)
        m.after(5000, lambda : errorText.grid_forget())
        return

    button.grid_forget()
    pw.grid_forget()
    #select inbox
    mail.select("INBOX")

    #select specific mails
    _, selected_mails = mail.search(None, '(FROM "do-not-reply@idtechnotifications.com")')

    #total number of mails from specific user
    print("Total Messages from do-not-reply@idtechnotifications.com:" , len(selected_mails[0].split()))

    counter = 0

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
                    counter+=1
                    createCalEvent(dateLine, name, emailLink)

            #else:
                #print("date exists")
    print("Done!--------------------------")
    completeText = "Done! Calendar Events Added: " + str(counter)
    status = Label(m, text=completeText, bg="green")
    status.grid(row=3)
    counter = 0
    progStat = Label(m, text="Program is running!", fg="green").grid(row=2)
    closeText = Label(m, text="Close App Window to Stop.", fg="red").grid(row=4)
    m.after(10000, lambda : status.grid_forget())
    m.after(interval, checkMail)



with open('loggedLessons.txt', 'a') as f:
    f.write('\n//----------//\n')


m.title("MailToCal v1.0")
Label(m, text='iD Tech Email:').grid(row=0)
Label(m, text='Password:').grid(row=1)
Label(m, text='Interval in ms:').grid(row=5)
em = Entry(m)
pw = Entry(m)
iv = Entry(m)
em.grid(row=0, column=1)
pw.grid(row=1, column=1)
iv.grid(row=5, column=1)

button = Button(m, text='Start', width=25, command=lambda : checkMail())
button.grid(row=2)


m.mainloop()