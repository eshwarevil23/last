# import the necessary packages
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import time
import cv2
from os import listdir
from os.path import isfile, join, dirname
import os, shutil
import glob
import sqlite3
from tensorflow.python.keras.backend import shape

print ("=========================================================================================PROCEDURE STARTED===========================================================================================")

sqlite_connection = sqlite3.connect("temp.db")
db = sqlite_connection.cursor()

# ALL REQUIRED PATHS
base_path = "/home/eshwar/Desktop/mihir/last/"

path= f"{base_path}captured_images/"
mask_path = f"{base_path}with_mask"
wmask_path = f"{base_path}without_mask"
prototxtPath = f"{base_path}face_detector/deploy.prototxt"
weightsPath = f"{base_path}face_detector/res10_300x300_ssd_iter_140000.caffemodel"
maskNet = load_model(f"{base_path}mask_detector.model")

Mask_count = 1
Wmask_count = 1

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)
	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)
k = True
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

file= [f for f in listdir(path) if isfile(join(path, f))]
images= np.empty(len(file), dtype= object)
for n in range(0, len(file)):
    images[n] = cv2.imread(join(path, file[n]))
i=0
while k:
    for i in range(0,len(file)):
        
        frame= images[i].copy()
        frame= imutils.resize(frame, width= 200)
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            label= "Mask" if mask > withoutMask  else "No Mask"
            # lobo = "Trash"
            lobo = "Mask" if mask > withoutMask  else "No Mask"
            color= (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label= "{}: {:.2f}%".format(label, max(mask, withoutMask)*100)
            #cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            #cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            # cv2.imshow("Frame", frame)
            if (lobo == 'Mask'):
                cv2.imwrite(os.path.join(mask_path, str(Mask_count) + ".jpg"), frame)
                Mask_count = Mask_count+1

            elif (lobo == 'No Mask'):
                cv2.imwrite(os.path.join(wmask_path,str(Wmask_count) + ".jpg"), frame)
                Wmask_count = Wmask_count+1
    k= False
    if i == len(file):
         break
    
    cv2.destroyAllWindows()
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))