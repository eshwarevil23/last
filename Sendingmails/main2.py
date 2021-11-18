import smtplib
import email
from email.mime.multipart import MIMEMultipart
# from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import csv
msg =   email.MIMEMultipart()
password = "ehugrgrrfxqvqbwb"
msg['From']="vivek.nalla362@gmail.com"

msg['Subject']="IMPORTANT"
msg.attach(email.MIMEImage(email.file("test.jpg").read()))

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(msg['From'],password)
print("Login Successfull")

with open("mails.csv",'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        msg['To']=line['mail_id']
        server.sendmail(msg['From'],msg['To'],msg.as_string())
        print(f"Email sent to {msg['To']}")