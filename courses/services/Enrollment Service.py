from courses.models.enrollment import Enrollment


def enroll_student(student, course):
    """
    Enroll a student in a course.

    Args:
        student: The student to enroll.
        course: The course to enroll the student in.

    Returns:
        The created Enrollment object.
    """
    if Enrollment.objects.filter(student=student, course=course).exists():
        raise ValueError("Student is already enrolled in this course.")

    return Enrollment.objects.create(student=student, course=course)