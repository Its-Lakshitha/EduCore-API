from courses.models.enrollment import Enrollment
from student.enums.StudentStatus import StudentStatus
from teacher.enums.TeacherStatus import TeacherStatus


def enroll_student(student, course):
    """
    Enroll a student in a course.

    Args:
        student: The student to enroll.
        course: The course to enroll the student in.

    Returns:
        The created Enrollment object.
    """
    if student.status != StudentStatus.ACTIVE:
        raise ValueError("Student must be active to enroll in a course.")

    if not course.teacher:
        raise ValueError("Course must have an assigned teacher to enroll students.")

    if course.teacher.status != TeacherStatus.ACTIVE:
        raise ValueError("Course's teacher must be active to enroll students.")
    
    if Enrollment.objects.filter(student=student, course=course).exists():
        raise ValueError("Student is already enrolled in this course.")

    return Enrollment.objects.create(student=student, course=course)