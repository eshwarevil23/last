from io import StringIO
import smtplib
import email, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
subject="Important"
body="You have been found not wearing a mask"
sender_email = "maskprojectatvce@gmail.com"
receiver_email = "mihirdeshpande1802@gmail.com"
password = input("Please enter your password: ")


# create a multipart message and set headers
message=MIMEMultipart()
message['From']=sender_email
message['To']=receiver_email
message['Subject']=subject
message['Bcc']=receiver_email

message.attach(MIMEText(body,"plain"))

filename="test.jpg"

with open(filename,'rb') as attachment:
    # add file as an application
    part = MIMEBase("application","octet-stream")
    part.set_payload(attachment.read())

#Encode file in ASCII characters to send by email
encoders.encode_base64(part) 

#Add headers as keypair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename={filename}"
)

#Add atachment to message and convert message to String
message.attach(part)
text= message.as_string()

#Login to server using secure context and send mail
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)