import cv2
import face_recognition
import pickle
import numpy as np
import cvzone
from concurrent.futures import ThreadPoolExecutor
import dlib
import time

# Print the version of dlib being used
print("Dlib version:", dlib.__version__)

# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load the encodings and IDs
file = open('D:/Projects/facial_recoginition_system/encodings/encodeFile.p', 'rb')
encodelistwithids = pickle.load(file)
file.close()
encodeKnownList, studentIds = encodelistwithids

# Function to process each face detected
def process_face(faceLoc, encodeFace):
    matches = face_recognition.compare_faces(encodeKnownList, encodeFace)
    face_distance = face_recognition.face_distance(encodeKnownList, encodeFace)
    match_index = np.argmin(face_distance)
    
    if matches[match_index]:
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = x1, y1, x2 - x1, y2 - y1
        text = f"Face Detected = id:{studentIds[match_index]}"
        return True, bbox, text
    return False, None, None

# Frame processing settings
frame_skip = 300
frame_count = 0

# Main loop
while True:
    success, img = cap.read()
    frame_count += 1
    
    if frame_count % frame_skip != 0:
        img_scaled_down = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_scaled_down = cv2.cvtColor(img_scaled_down, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(img_scaled_down)
        encodeCurrFrame = face_recognition.face_encodings(img_scaled_down, faceCurFrame)

        with ThreadPoolExecutor() as executor:
            results = executor.map(process_face, faceCurFrame, encodeCurrFrame)

        for detected, bbox, text in results:
            if detected and bbox is not None:
                img = cvzone.cornerRect(img, bbox, rt=1)
                cv2.putText(img, text, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Extract and save the detected face
                face_img = img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"D:/Projects/facial_recoginition_system/detected_faces/{timestamp}.jpg"
                cv2.imwrite(filename, face_img)
                print(f"Saved detected face to {filename}")

        cv2.imshow("Facial Recognition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()