import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from smtplib import SMTPException


def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location = ''):

    success = False
    email_sender = 'jsmith@apteco.com'

    msg = MIMEMultipart()
    msg['From'] = email_sender

    if isinstance(email_recipient, str):
        email_recipient = [email_recipient]

    msg['To'] = ', '.join(email_recipient)
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('exchange.apteco.com', 587)
        server.ehlo()
        server.starttls()
        print('logging in')
        server.login('jsmith', 'IAgr33d2Th1s!')
        print('Logged in')
        text = msg.as_string()
        #text = 'dave'
        server.sendmail(email_sender, email_recipient, text)
        print('email sent')
        server.quit()
        success = True

    except SMTPException as e:
        success = False
        print(e)
        print("SMTP server connection error")

    except Exception as e:
        success = False
        print(e)
        print("Non-SMTP server connection error")

    return success
