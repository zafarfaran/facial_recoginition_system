# Import necessary libraries
from mtcnn import MTCNN
import cv2
from matplotlib import pyplot as plt

# Initialize the MTCNN detector
detector = MTCNN()

# Load an image using OpenCV
image_path = '/app/images/1643421016946.jpeg'
image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

# Detect faces in the image
faces = detector.detect_faces(image)

# Draw rectangles around detected faces
for face in faces:
    x, y, width, height = face['box']
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 155, 255), 2)

# Display the image with detected faces
plt.imshow(image)
plt.axis('off')
plt.show()