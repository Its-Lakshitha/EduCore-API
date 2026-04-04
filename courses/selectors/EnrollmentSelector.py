from courses.models.enrollment import Enrollment


def get_enrollments_by_course(course_id):
    return Enrollment.objects.filter(course_id=course_id).select_related('student')

def get_enrollments_by_student(student_id):
    return Enrollment.objects.filter(student_id=student_id).select_related('course')