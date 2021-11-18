import csv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line

# get the emails of the people from a csv file
with open("mails.csv",'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    names = []
    for line in csv_reader:
        names.append(line["EMAIL(PERSONAL)"])

sender_email = "maskprojectatvce@gmail.com"
sender_name = "Admin"
password = input("Enter the password for the account: ")
# Email body
email_html = open('email2.html')
email_body = email_html.read()

filename = 'testing.jpg'

for name in names:
    print(f"Sending mail to {name}")
    msg = MIMEMultipart()
    msg['To'] = formataddr((name, name))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['X-Priority']='2'
    msg['Subject'] = 'Test Mail'
    msg.attach(MIMEText(email_body,'html'))

    # opening the image file

    try:
        with open(filename,'rb') as attachment:
            part = MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
            )
        msg.attach(part)
    except Exception as e:
        print(f'AttachmentError{e}')
        break

    try:
        # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Encrypts the email
        context = ssl.create_default_context()
        server.starttls(context=context)
        # We log in into our Google account
        server.login(sender_email, password)
        # Sending email from sender, to receiver with the email body
        server.sendmail(sender_email, name, msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f'Could not send mail{e}')
        break
print('Closing the server...')
server.quit()