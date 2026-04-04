from django.urls import path

from .views import create_course, enroll, list_courses, student_enrollments, courses_per_teacher, students_per_course

urlpatterns = [
    path('courses/', list_courses.as_view()),
    path('courses/create/', create_course.as_view()),
    path('enroll/', enroll.as_view()),
    path('student/<int:student_id>/enrollments/', student_enrollments.as_view()),

    path('dashboard/courses-per-teacher/', course_per_teacher.as_view()),
    path('dashboard/students-per-course/', students_per_course.as_view()),
]