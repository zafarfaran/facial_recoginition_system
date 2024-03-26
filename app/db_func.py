from ..models import Student, User, Course

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