from django.db.models import Count
from django.db.models.functions import TruncMonth

from courses.models.course import Course
from courses.models.enrollment import Enrollment


def get_courses_per_teacher():
    return Course.objects.values('teacher__id','teacher__user__email').annotate(total_courses=Count('id')).order_by('-total_courses')

def get_students_per_course():
    return Enrollment.objects.values('course__id','course__name').annotate(total_students=Count('student')).order_by('-total_students')

def filter_enrollments(queryset, start_date=None, end_date=None, department_id=None):
    if start_date and end_date:
        queryset = queryset.filter(enrollment_at__range=[start_date,end_date])
    if department_id:
        queryset = queryset.filter(course__teacher__department_id=department_id)

    return queryset

def get_monthly_enrollments(start_date=None, end_date=None, department_id=None):
    enrollments = Enrollment.objects.all()
    enrollments = filter_enrollments(enrollments, start_date, end_date, department_id)
    return enrollments.annotate(month=TruncMonth('enrollment_at')).values('month').annotate(total=Count('id')).order_by('month')

def get_course_popularity(department_id=None):
    courses = Enrollment.objects.all()
    courses = filter_enrollments(courses,department_id=department_id)

    return courses.values('course__id','course__name').annotate(total_students=Count('students')).order_by('-total_enrollments')

def get_top_teachers():
    return Course.objects.values('teacher__id','teacher__user__email').annotate(total_courses=Count("id"),total_students=Count('enrollments_students')).order_by('-total_students')

def get_top_courses():
    return Enrollment.objects.values('course__id','course__name').annotate(total_students=Count('student')).order_by('-total_students')