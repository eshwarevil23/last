import cv2
import os
import time
import datetime
path= '/home/eshwar/Desktop/last/raspberry_pi/pimages'
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0);

filename1 = time.strftime("%Y%m%d-%H%M")
date = datetime.datetime.now().strftime("%Y_%m_%d")
st= 0
while(cap.isOpened()):
    today_date = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dialated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dialated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(frame1, contours, -1, (150, 12, 255), 2)
    for c in contours:
        if cv2.contourArea(c) < 4000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        temp = frame1
        #cv2.rectangle(temp, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #print (faces, len(faces), type(faces))
        time.sleep(1)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if (len(faces) != 0):
        cv2.imwrite(os.path.join(path, today_date+".png"), frame1)
        st = st+1
        print (faces, len(faces), type(faces))
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('frame', frame1)
cap.release()
cv2.destroyAllWindows()
print("Number of images collected: {}".format(st))
