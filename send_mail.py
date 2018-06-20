#!/usr/bin/python3
import smtplib
from string import Template
from email.mime.base import MIMEBase
from email import encoders
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

MY_ADDRESS='<EMAIL ADDRESS>'
PASSWORD='<PASSWORD>'

def main():
    names, emails = get_contacts('<TXT FILE WITH CONTACT LIST IN FORMAT NAME EMAIL>') # read contacts
    print("\nLogging into SMTP server...            ",end='',flush=True)
    s = smtplib.SMTP('<SERVER ADDRESS>', <SERVER PORT>)
    try:
        # set up the SMTP server
        s.ehlo_or_helo_if_needed()
        s.starttls()
        s.ehlo()
        s.login(MY_ADDRESS, PASSWORD)
        print("Successful Login!")
    except:
        print("Something went wrong")
    # For each contact, send the email:

    print("Creating Message...                      ",end='',flush=True)
    #if sys.argv[1] == 'Sprints':
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = '<MESSAGE TO WRITE>'
    # Prints out the message body for our sake
    #print(message)

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=",".join(emails)
    msg['Subject']="<SUBJECT>"

    # add in the message body
    
    msg.attach(MIMEText(message, 'plain'))
    print("Message Created and Added!")

    #Add message attachment to excel created in previous script
    print("Creating Attachtment...                  ",end='',flush=True) 
    filename = "<FILENAME OF ATTACHMENT>"
    attachment = open("<ATTACHMENT TO ADD>", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)
    print('Attachment Created and Added!')
    
    # send the message via the server set up earlier.
    
    print('Sending Mail...                          ',end="",flush=True)
    s.send_message(msg)
    print('Mail Sent!')
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main()
