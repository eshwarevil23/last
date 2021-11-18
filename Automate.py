import os
from datetime import datetime
import time
import sqlite3

time.sleep(5)

# CHANGE THESE PATHS & VALUE
threshold_image_value = 5
python_interpreter_path = "/home/eshwar/Desktop/mihir/face/bin/python3"
base_path = "/home/eshwar/Desktop/mihir/last/"


# Required Paths
path_to_captured_images = f"{base_path}captured_images/"
path_to_without_mask_images = f"{base_path}without_mask/"
mask_detection_prog = f"{base_path}detection.py"
automate_prog = f"{base_path}Automate.py"
face_recognition_prog = f"{base_path}FaceDetection.py"
db_path = f"{base_path}Faces.db"
sending_mails_prog = f"{base_path}Sendingmails/sendingemail.py"


# check for every 60 seconds 
while len(os.listdir(path_to_captured_images)) < threshold_image_value:
    time.sleep(10)

# Start
print("[INFO]: Hello Admin!")
print("[INFO]: Today is {}".format(datetime.now().strftime("%D %H:%M:%S")))
print("[INFO]: The path to the captured images is set as {}!".format(path_to_captured_images),end="")
print("[INFO]: The total number of images captured today are {}.".format(len(os.listdir(path_to_captured_images))))

# face mask detection Procedure
os.system(f"{python_interpreter_path} {mask_detection_prog}")
print("[INFO]: Face Mask Detection Completed!")
print("[INFO]: The total number of images where mask was not found is {}.".format(len(os.listdir(path_to_without_mask_images))))

# Face Recognition Procedure
os.system(f"{python_interpreter_path} {face_recognition_prog} {path_to_without_mask_images}")
print("[INFO]: Face Recognition Completed!")

#Sendig mails to people not wearing a Mask
print("Sending mails")
os.system(f"{python_interpreter_path} {sending_mails_prog}")

# REFRESHING DB
sqlite_connection = sqlite3.connect(f"{db_path}")
db = sqlite_connection.cursor()
db.execute('DELETE FROM face_table;')
#CLOSING DB
sqlite_connection.commit()
db.close()
sqlite_connection.close()

#LOOPING
os.system(f"{python_interpreter_path} {automate_prog}")