import smtplib
import csv
senders = "vivek.nalla362@gmail.com"
receivers = "mihirdeshpande1802@gmail.com"
password = "ehugrgrrfxqvqbwb"
subject = "IMPORTANT"
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(senders,password)
print("login success")
with open("mails.csv",'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        receiver = line["mail_id"]
        name = line["name"]
        message = f"Subject: {subject}\n\n{'This is a test message!'}"
        server.sendmail(senders,receiver,message)
        print(f"Email has been sent to {receiver}!")

print("sending done!")
















# # sending using the gui way

# from selenium import webdriver
# import time
# from config import EMAIL, PASSWORD
# browser  = webdriver.Edge("E:\Sendingmails\msedgedriver.exe")
# browser.get("https://www.gmail.com")


# email_input = browser.find_element_by_css_selector('input[type="email"]')
# email_input.send_keys(EMAIL)

# next_btn = browser.find_element_by_class_name('VfPpkd-LgbsSe')

# next_btn.click()