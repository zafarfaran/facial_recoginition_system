from mtcnn import MTCNN
from deepface import DeepFace
import cv2


def detect_and_recognize(frame, detector):
    faces = detector.detect_faces(frame)
    for face in faces:
        x, y, width, height = face['box']
        face_region = frame[y:y + height, x:x + width]

        # Use DeepFace for recognizing the detected face
        try:
            # Assuming "db_path" is the path to your database of known faces
            db_path = 'D:/Projects/facial_recoginition_system/app/images'
            # Find the most similar face in the database to the detected face
            recognition = DeepFace.find(face_region, db_path=db_path, enforce_detection=False)
            if recognition.shape[0] > 0:
                identity = recognition.iloc[0]['identity']
                print(f"Identity: {identity}")
                # Here, log the attendance based on 'identity'
        except Exception as e:
            print(f"Recognition failed: {str(e)}")


# Initialize the MTCNN detector
detector = MTCNN()

# Start video capture (0 for the default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (MTCNN expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect and recognize faces in the frame
    detect_and_recognize(frame_rgb, detector)

    # Display the resulting frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()