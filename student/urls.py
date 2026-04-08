from django.urls import path

from .views import (
    create_student,
    delete_student,
    get_student,
    list_students,
    my_courses,
    my_profile,
    update_student,
    update_student_status,
)

urlpatterns = [
    path('students/create', create_student, name='student-create'),
    path('students/', list_students, name='students-list'),
    path('students/<int:id>/', get_student, name='student-detail'),
    path('students/update/<int:id>', update_student, name='student-update'),
    path('students/delete/<int:id>', delete_student, name='student-delete'),
    path('students/my-profile', my_profile, name='student-profile'),
    path('students/update/<int:id>/status', update_student_status, name='student-update-status'),
    path('students/my-courses', my_courses, name='student-my-courses'),
]