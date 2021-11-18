import smtplib,ssl
from email.mime.text import MIMEText
from email.utils import formataddr

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
# configuration
sender_email = "vivek.nalla362@gmail.com"
sender_name = "Admin"
password = "ehugrgrrfxqvqbwb"
# email_body = '''
#     <h1> Test test </h1>
# '''
email_html = open("mail.html")
email_body = email_html.read()
filename="test.jpg"
print("Sending email")
with open("mails.csv",'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        receiver_name = line['name']
        receiver_email = line['mail_id']
        msg = MIMEMultipart()
        msg['To'] = formataddr((receiver_name,receiver_email))
        msg['From'] = formataddr((sender_name,sender_email))
        msg['Subject'] = 'Hello, World'
        msg.attach(MIMEText(email_body,'html'))

        try:
            with open(filename,'r') as attachment:
                part = MIMEBase("application","octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}"
            )

            msg.attach(part)
        except Exception as e:
            print("an error has been found")


            
        try:
            # creating a smtp session
            server = smtplib.SMTP('smtp.gmail.com',587)
            # encrypt the email
            context = ssl.create_default_context()
            server.starttls(context=context)
            # logging into Gmail Account
            server.login(sender_email,password)
            server.sendmail(sender_email,receiver_email,msg.as_string())
            print("Mail sent")
        except Exception as e:
            print(e)
        finally:
            server.close()