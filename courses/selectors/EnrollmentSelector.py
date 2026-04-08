from courses.models.enrollment import Enrollment


def get_enrollments_by_course(course_id):
    return Enrollment.objects.filter(course_id=course_id).select_related('student')

def get_enrollments_by_student(student_id):
    return Enrollment.objects.filter(student_id=student_id).select_related('course')

def get_student_courses(student, search=None):
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    if search:
        enrollments = enrollments.filter(course__name__icontains=search) | enrollments.filter(course__code__icontains=search)

    return enrollments.order_by('-created_at')