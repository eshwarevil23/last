import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail='''sending an attachment'''
sender = "vivek.nalla362@gmail.com"
password = ""
receiver_address = "mihirdeshpande1802@gmail.com"
message = MIMEMultipart()
message['From'] = sender
message['To'] = receiver_address
message['Subject'] = "Important"
message.attach(MIMEText(mail,'plain'))
attach_file_name = "test.jpg"
attach_file = open(attach_file_name,'rb')
payload = MIMEBase('application','octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload)
payload.add_header('Content-Decomposition','attachment',filename=attach_file_name)
message.attach(payload)
session = smtplib.SMTP('smtp.gmail.com',587)
session.starttls()
session.login(sender,password)
text = message.as_string()
session.sendmail(sender,receiver_address,text)
session.quit()
print("Mail has been sent successfully")