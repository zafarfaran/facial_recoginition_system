from flask import current_app,Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User,Attendance,Student,Course
from .extensions import db, bcrypt
import secrets
from functools import wraps
import json
from datetime import datetime, timedelta
import os
from threading import Thread

from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from .EncodingGenerator import main_encoding

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

admin = Blueprint('admin', __name__)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_type' in session or session['user_type'] != 'admin':
            flash('This page is restricted to admin users.')
            return redirect(url_for('index'))  # Redirect to login or another appropriate page
        return f(*args, **kwargs)
    return decorated_function

# Put your authentication routes here
@admin.route('/adminDashboard', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    return render_template('admin-dashboard.html')


@admin.route('/allAttendance', methods=['GET', 'POST'])
@admin_required
def all_attendance():

    attendance_records = Attendance.query.all()
    print("Attendance Records: ", attendance_records)
    return render_template('admin-dashboard-allAttendance.html', records=attendance_records)

@admin.route('/activeAttendance', methods=['GET', 'POST'])
@admin_required

def show_attendance():
    # Calculate the datetime for 24 hours ago
    twenty_four_hours_ago = datetime.utcnow() - timedelta(days=1)

    # Query attendance records from the last 24 hours
    recent_attendance_records = Attendance.query.filter(
        Attendance.timestamp >= twenty_four_hours_ago
    ).all()

    # Pass the records to the frontend
    return render_template('admin-dashboard-activeAttendance.html', records=recent_attendance_records)

@admin.route('/allUsers', methods=['GET', 'POST'])
@admin_required
def  show_all_Students():
    users = Student.query.all()
    return render_template('admin-dashboard-allUsers.html', users=users)

@admin.route('/addUser', methods=['GET', 'POST'])
@admin_required
def create_student():
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.form['name']
            email = request.form['email']
            year = request.form.get('year', type=int)
            course_id = request.form.get('course_id', type=int)

            # User details
            username = email  # Using email as username
            raw_password = secrets.token_hex(16)  # Generate a random password
            password = bcrypt.generate_password_hash(raw_password).decode('utf-8')  # Hash the password
            print(f'Generated password: {raw_password}')
            # Handle file upload
           

            # Create User entity
            new_user = User(username=username, password=password, user_type='student')
            db.session.add(new_user)
            db.session.flush()  # Assign an ID to new_user without committing
            file = request.files['image']
            if file and allowed_file(file.filename):
                _, file_extension = os.path.splitext(secure_filename(file.filename))
                filename = f"{new_user.id}{file_extension}"  # New filename with User ID
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

            # Create Student entity
            new_student = Student(user_id=new_user.id, name=name, email=email, year=year, course_id=course_id)
            db.session.add(new_student)
            
            db.session.commit()
            thread = Thread(target=main_encoding)
            thread.start()
            flash('Student and user created successfully! Encoding generation started.')
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction on error
            flash('Error creating user. It\'s possible the email is already in use. Please try again.', 'error')
        except Exception as e:
            db.session.rollback()  # Rollback the transaction on any other general error
            flash(f'An unexpected error occurred: {str(e)}', 'error')

        return redirect(url_for('admin.create_student'))

    return render_template('admin-dashboard-addUser.html') 
@admin.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('admin-dashboard-allCourses.html', courses=courses)
@admin.route('/add-course', methods=['POST'])
def add_course():
    name = request.form.get('name')
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    new_course = Course(name=name, start_date=start_date, end_date=end_date)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('admin.courses'))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# The form template