from flask import Flask,session
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from .auth import auth
from .admin import admin
from flask import render_template
from .extensions import db, bcrypt
from threading import Thread, Event
import cv2
import face_recognition
import cvzone
from concurrent.futures import ThreadPoolExecutor
import time
import pickle
from .db_func import get_student_details,check_and_create_attendance
import numpy as np
from flask_bcrypt import Bcrypt
from flask import redirect, url_for

 # Load the encodings and IDs
file = open('D:/Projects/facial_recoginition_system/encodings/encodeFile.p', 'rb')
encodelistwithids = pickle.load(file)
file.close()
encodeKnownList, studentIds = encodelistwithids

# Initialize the stop flag
stop_thread = Event()

# Placeholder for the thread object
background_thread = None
  # Create the Bcrypt instance

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
   
       
    UPLOAD_FOLDER = 'static/Users/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/facial_recognition_db'
    # Additional configuration settings for your app
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    bcrypt.init_app(app)
    Session(app)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    # Import models here to ensure they are known to SQLAlchemy
    from .models import User, Attendance, Student, Course, Subject
    @app.route('/detect')
    def detection():
        session['face_detection'] = True
        global background_thread
        print(background_thread)
        if background_thread is None or not background_thread.is_alive():
            # Reset the stop flag in case it was previously set
            stop_thread.clear()
            # Start the background thread
            background_thread = Thread(target=start_face_detection, args=(app,stop_thread))
            background_thread.start()
        return redirect(url_for('admin.admin_dashboard'))
    @app.route('/stop-face-detection')
    def stop_face_detection():
        session['face_detection'] = False
        global stop_thread, background_thread
        stop_thread.set()  # Signal the thread to stop

        print(background_thread,stop_thread)
        # Signal the thread to stop
        stop_thread.set()
       
        return redirect(url_for('admin.admin_dashboard'))
    
    @app.route('/') 
    def index():
      
        return render_template('index.html')
    
    
    
    return app

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
        return studentIds[match_index],True, bbox, text
    return None,False, None, None

def start_face_detection(app,stop_event):
    with app.app_context():
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)  # Width
        cap.set(4, 720)   # Height

        last_db_query_time = 0  # Initialize last database query time
        query_interval = 10  # Interval for database queries in seconds

        while True:
            success, img = cap.read()
            img_scaled_down = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_scaled_down = cv2.cvtColor(img_scaled_down, cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(img_scaled_down)
            encodeCurrFrame = face_recognition.face_encodings(img_scaled_down, faceCurFrame)

            with ThreadPoolExecutor() as executor:
                results = executor.map(process_face, faceCurFrame, encodeCurrFrame)

            for id, detected, bbox,text_false in results:
                if detected and bbox and id is not None:
                    current_time = time.time()
                    if current_time - last_db_query_time > query_interval:
                        # Update last database query time
                        last_db_query_time = current_time
                        
                        student_details = get_student_details(id)
                        text,flag = check_and_create_attendance(id, db)
                        if flag:
                            face_img = img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            timestamp = f"{id}_{timestamp}"
                            filename = f"D:/Projects/facial_recoginition_system/static/temp/{timestamp}.jpg"
                            cv2.imwrite(filename, face_img)
                            print(f"Saved detected face to {filename}")
                        
                    
                    img = cvzone.cornerRect(img, bbox, rt=1)
                    cv2.putText(img, text, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    # Extract and save the detected face logic can be here if needed

            cv2.imshow("Facial Recognition", img)
            if cv2.waitKey(1) & 0xFF == ord('q') or stop_event.is_set():
                break

        cap.release()
        cv2.destroyAllWindows()

# Code to extract and save the detected face can be uncommented if needed
                        # face_img = img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                        # timestamp = time.strftime("%Y%m%d-%H%M%S")
                        # timestamp = f"{id}_{timestamp}"
                        # filename = f"D:/Projects/facial_recoginition_system/static/temp/{timestamp}.jpg"
                        # cv2.imwrite(filename, face_img)
                        # print(f"Saved detected face to {filename}")