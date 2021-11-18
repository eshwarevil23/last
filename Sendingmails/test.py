import csv
with open("mails.csv",'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        print(line["email_id"]+"@vce.ac.in")
