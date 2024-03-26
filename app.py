# from flask import Flask, request, render_template, redirect, url_for, session, flash,jsonify
# from flask_sqlalchemy import SQLAlchemy
# import bcrypt
# from datetime import datetime
# from functools import wraps
# import json
# import base64
# import numpy as np
# import os

# # app = Flask(__name__)
# # app.secret_key = 'your_secret_key'
# # # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/litigat8'
# # # Database configuration
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/facial_recognition_db'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # db = SQLAlchemy(app)

# # class User(db.Model):
# #     __tablename__ = 'user'  # Explicitly set the table name if it's not the default
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(50), unique=True, nullable=False)
# #     password = db.Column(db.String(200), nullable=False)
# #     user_type = db.Column(db.String(20), nullable=False)
    
# # class Attendance(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# #     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# #     status = db.Column(db.String(50), nullable=False)

# #     user = db.relationship('User', backref=db.backref('attendances', lazy=True))
# # class Student(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# #     name = db.Column(db.String(100), nullable=False)
# #     email = db.Column(db.String(100), unique=True, nullable=False)
# #     year = db.Column(db.Integer, nullable=False)
# #     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
# #     # Relationships
# #     user = db.relationship('User', backref=db.backref('student', uselist=False))
# #     course = db.relationship('Course', back_populates='students')

# #     def __repr__(self):
# #         return f'<Student {self.name}>'


# # class Course(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# #     end_date = db.Column(db.DateTime, nullable=False)
# #     subjects = db.relationship('Subject', backref='course', lazy=True)  # One-to-many relationship
# #     students = db.relationship('Student', back_populates='course')  # Backreference to students

# #     def __repr__(self):
# #         return f'<Course {self.name}>'

# # class Subject(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# #     def __repr__(self):
# #         return f'<Subject {self.name}>'
   

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not 'user_type' in session or session['user_type'] != 'admin':
#             flash('This page is restricted to admin users.')
#             return redirect(url_for('login'))  # Redirect to login or another appropriate page
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in session:
#         flash('You are already logged in.')
#         return redirect(url_for('admin_dashboard'))  # Or wherever you want to redirect users
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password'].encode('utf-8')
        
#         user = User.query.filter_by(username=username).first()
#         if user and bcrypt.checkpw(password, user.password.encode('utf-8')):
#             session['username'] = user.username
#             session['user_type'] = user.user_type
#             return redirect(url_for('index'))
#         else:
#             flash('Login failed. Check your username and password.')
#             return redirect(url_for('login'))
#     return render_template('login.html')  # Ensure you have a login.html template

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
#         user_type = request.form['user_type']  # Ensure this comes from your registration form
        
#         new_user = User(username=username, password=password, user_type=user_type)
#         db.session.add(new_user)
#         db.session.commit()
        
#         flash('User registered successfully!')
#         return redirect(url_for('login'))
#     return render_template('register.html')  # Make sure to create a registration form

# @app.route('/adminDashboard', methods=['GET', 'POST'])
# @admin_required
# def admin_dashboard():
#     return render_template('admin-dashboard.html')

# @app.route('/facial_auth')
# def facial_auth():
#     return render_template('facial_auth.html')

# @app.route('/logout')
# def logout():
#     # Remove the username from the session if it's there
#     session.pop('username', None)
#     # Redirect to login page or home page after logout
#     return redirect(url_for('login'))  # Assuming you have a view function named 'login'


# @app.route('/')
# def index():
#     # if 'username' in session:
#     #     return f"Welcome {session['username']}, you are logged in as a {session['user_type']}."
#     return render_template('index.html')

# @app.route('/api/process-video', methods=['POST'])
# def process_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file provided'}), 400
    
#     video_file = request.files['video']
#     filepath = os.path.join('/tmp', video_file.filename)
#     video_file.save(filepath)

#     # Process the video file here. You can use your model to detect faces and return coordinates.
#     # Example: coordinates = your_model.detect_faces(filepath)

#     return jsonify({'message': 'Video processed', 'coordinates': '...'})

# if __name__ == '__main__':

#     app.run(debug=True)
