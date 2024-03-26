from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime


from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

with open('D:/Projects/facial_recoginition_system/encodings/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('D:/Projects/facial_recoginition_system/encodings/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=3)
print("training")
knn.fit(FACES, LABELS)
print("training done")

confidence_threshold = 0.9  # You can adjust this threshold according to your needs



# COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        probabilities = knn.predict_proba(resized_img)[0]
        class_index = np.argmax(probabilities)
        confidence = probabilities[class_index]

        print(f"Probabilities: {probabilities}")  # Debug: Print out all probabilities
        print(f"Predicted Class Index: {class_index}, Confidence: {confidence}")  # Debug

        if confidence > confidence_threshold:
            label = knn.predict(resized_img)
            cv2.putText(frame, f"{label} ({confidence * 100:.2f}%)", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
        else:
            pass

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
