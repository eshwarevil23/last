# sending a simple mail to the college account
import smtplib # import smtp
sender_email = "maskprojectatvce@gmail.com"
receiver_email = "1602-19-735-087@vce.ac.in"
password = input("Enter your password: ")
message = '''Hey, Hope you are doing good,
This is just a test mail'''
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sender_email,password)
print("Login success")
server.sendmail(sender_email,receiver_email,message)
print("Email sent to {}".format(receiver_email))
