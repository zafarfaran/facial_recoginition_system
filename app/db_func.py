
from datetime import datetime, timedelta

from .models import Student, User, Course,Attendance
def check_and_create_attendance(user_id,db):
    # Get the current time
    now = datetime.utcnow()
    # Calculate 24 hours ago
    twenty_four_hours_ago = now - timedelta(days=1)

    # Check if an attendance record exists for the user in the last 24 hours
    attendance_record = Attendance.query.filter(
        Attendance.user_id == user_id,
        Attendance.timestamp >= twenty_four_hours_ago
    ).first()

    # If no record exists, create one
    if not attendance_record:
        new_attendance = Attendance(user_id=user_id, timestamp=now, status='Present')
        db.session.add(new_attendance)
        db.session.commit()
        return f"Marked Present",True
     
    else:
        # print(f"Attendance record already exists for user_id {user_id} in the last 24 hours.")
        return f"You have already been marked present in the last 24 hours.",False
def get_student_details(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if student:
        return {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'year': student.year,
            'course': student.course.name if student.course else 'No Course Assigned'
        }
    else:
        return None