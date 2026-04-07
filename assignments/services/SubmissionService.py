from student.enums.StudentStatus import StudentStatus


def validate_student_active(student):
    if student.status != StudentStatus.ACTIVE:
        raise ValueError("Student is not active")