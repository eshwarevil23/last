# this should start after the automation part.
import sqlite3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
import os

# PATHS REQUIRED
base_path = "/home/eshwar/Desktop/mihir/last/Sendingmails/"
without_mask_path = "/home/eshwar/Desktop/mihir/last/without_mask/"
faces_db_path = "/home/eshwar/Desktop/mihir/last/Faces.db"

html_path = f"{base_path}email2.html"
admin_mail = "miniproject7480@gmail.com"
emails_db_path = f"{base_path}email.db"
email_pics_path = f"{base_path}emailprocesspics/"
password="coronavyas"
sender_email = "maskprojectatvce@gmail.com"
email_html = open(f'{html_path}')
email_body = email_html.read()
context = ssl.create_default_context()
server = smtplib.SMTP('smtp.gmail.com',25)
server.starttls(context=context)
server.login(sender_email,password)
# send_mail function
def send_mail(email_address,attachment_picture):
    print(f"Sending mail to {email_address}")
    msg = MIMEMultipart()
    msg['To'] = formataddr(("Student",email_address))
    msg['From'] = formataddr(("Admin",sender_email))
    msg['Subject'] = "Important"
    msg.attach(MIMEText(email_body,'html'))

    # opening the image file
    if os.path.isfile(attachment_picture)==True:
        with open(attachment_picture,'rb') as attachment:
            part = MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment_picture}",
        )
        msg.attach(part)

    # connecting to the smtp server
    server.sendmail(sender_email,email_address,msg.as_string())
    print("Email sent")
    # server.quit()


def sending_mail_admin(path_to_folder,receiver_address=f"{admin_mail}"):
    print("Sending the remaining mails to admin mail id")
    # mail part
    msg = MIMEMultipart()
    msg['To'] = formataddr(("Admin",receiver_address))
    msg['From'] = formataddr(("Admin",sender_email))
    msg['Subject'] = "Important"
    msg.attach(MIMEText(email_body,'html'))
    for each_file in os.listdir(path_to_folder):
        try:
            file_name=os.path.join(path_to_folder,each_file)
            part = MIMEBase('application',"octet-stream")
            part.set_payload(open(file_name,"rb").read())    

            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment',filename=file_name)
            msg.attach(part)
        except:
            print("Could not attach file")
    server.sendmail(sender_email,receiver_address,msg.as_string())


# go through the db that was created by storing images that did not have mask on
# connect to the first db
sqlite_connection_1 = sqlite3.connect(f"{faces_db_path}")
db1 = sqlite_connection_1.cursor()
# connect to the second db
sqlite_connection_2 = sqlite3.connect(f"{emails_db_path}")
db2 = sqlite_connection_2.cursor()

# iterate through the data present in the first db
# then fetch the data present in the emails db
# get all the names
db1.execute("SELECT DISTINCT Roll FROM face_table;")

if db1.rowcount==0:
    print("No data in the database")
else:
    roll_list = db1.fetchall()
    ccounter = 1
    for i,each_roll in enumerate(roll_list):
        x = str(each_roll[0]).strip()
        # print(x)
        # read the image from the db
        db1.execute("SELECT Image FROM face_table WHERE Roll LIKE ?",(x,))
        photo_binary = db1.fetchone()[0]
        # save the file into the folder
           
        with open(f"{email_pics_path}{x}.jpg",'wb') as file:
            file.write(photo_binary)
        # find the email of the person in the second database
        db2.execute("SELECT EMAIL_ID FROM details_basic WHERE ROLL LIKE ?",(x,))  
        result = db2.fetchone()
        if(result==None):
            print("Email ID not found")
            continue
        if(result!=None):
            # send the email to the person
            send_mail(result[0],f"{email_pics_path}{x}.jpg")
        
print('Sending unknown images')
sending_mail_admin(f'{without_mask_path}')
# sending the unknown
print('Closing the server')
server.quit()    



