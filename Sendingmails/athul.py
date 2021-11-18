import smtplib as sl

def sendMail( rnum, temperature):
    # send mail to the management when invoked
    smtpobj = sl.SMTP('smtp.gmail.com', 587)
    # creating a smtp object and connecting to the domain server of mail.outlook.com over the port 587

    # you can remove the print statements from the code, its placed to know the status of code execution

    smtpobj.ehlo()  # this establishes the connection with the server
    smtpobj.starttls()  # this start the ttls encryption in the server
    pswd = 'put password'  # Taking the password as input is safer because if you save it in a script anyone who can access the script will be able to find the password
    smtpobj.login('covidCloudmp@gmail.com', pswd)  # login in to the smtp server

    SUBJECT = '{} temperature above 100'.format(rnum)  # subject line

    TEXT = '''Dear management,

    Student {} is having a temperature of {}
    please take an immediate attention on this issue.

    Thank you
    '''.format(rnum, temperature)  # body of the mail

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)  # concating the strings using string formatting

    smtpobj.sendmail('covidCloudmp@gmail.com', '1602-19-735-087@vce.ac.in', message)
    # sending the mail from us to the reciever; 071 = user; 091 = reciever; message = subject + body
    print("Mail sent to the management")
    smtpobj.quit()  # quiting the smtp server and deleting the object

sendMail("1602-19-735-071",99.9)