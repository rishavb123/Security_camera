__author__ = 'Bhagat'
import smtplib
import encoder
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email(message,subject,files=['none'],email_user = 'pythonemailsender1@gmail.com',email_password_encoded = '<sm~7tyu',email_send = 'rishavb123@gmail.com'):

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body,'plain'))

    for filename in files:
        if filename is not 'none':
            attachment = open(filename,'rb')

            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename= '+filename)

            msg.attach(part)

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,encoder.decode(email_password_encoded))

    server.sendmail(email_user,email_send,text)
    server.quit()
#email('school email: 10013225@sbstudents.org\nemail: rishavb123@gmail.com\nStudent ID: 10013225','Info',email_user='rishavb123@gmail.com',email_password_encoded='9ift;w|y',email_send='ajaybhagat99@gmail.com')
