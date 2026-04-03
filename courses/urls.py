from django.urls import path

from .views import create_course, enroll, list_courses, student_enrollments

urlpatterns = [
    path('courses/', list_courses.as_view()),
    path('courses/create/', create_course.as_view()),
    path('enroll/', enroll.as_view()),
    path('student/<int:student_id>/enrollments/', student_enrollments.as_view()),
]