import cv2
import time
import face_recognition
# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 720)  # Height

if not cap.isOpened():
    print("Error loading the camera")
    exit()

# For FPS calculation
fps_start_time = time.time()
fps = 0
total_frames = 0

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    total_frames += 1

    # Your image processing code here
    faceCurFrame = face_recognition.face_locations(img)

    # Draw rectangles around detected faces
    for top, right, bottom, left in faceCurFrame:
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
    # Calculate FPS
    time_elapsed = time.time() - fps_start_time
    if time_elapsed >= 1.0:  # Every second
        fps = total_frames / time_elapsed
        total_frames = 0  # Reset for the next average
        fps_start_time = time.time()

    # Display FPS on the frame
    cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()