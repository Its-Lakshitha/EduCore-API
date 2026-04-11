from django.urls import path

from .views import (
    courses_per_teacher,
    create_course,
    enroll,
    list_courses,
    student_enrollments,
    students_per_course,
)

urlpatterns = [
    path('courses/', list_courses),
    path('courses/create/', create_course),
    path('enroll/', enroll),
    path('student/<int:student_id>/enrollments/', student_enrollments),

    path('dashboard/courses-per-teacher/', courses_per_teacher),
    path('dashboard/students-per-course/', students_per_course),
]