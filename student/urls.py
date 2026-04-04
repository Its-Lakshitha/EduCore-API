from django.urls import path

from .views import (
    create_student,
    delete_student,
    get_student,
    list_students,
    my_profile,
    update_student,
    update_student_status,
    my_courses,
)

urlpatterns = [
    path('students/create', create_student),
    path('students/', list_students),
    path('students/<int:id>/', get_student),
    path('students/update/<int:id>', update_student),
    path('students/delete/<int:id>', delete_student),
    path('students/my-profile', my_profile),
    path('students/update/<int:id>/status', update_student_status),
    path('students/my-courses', my_courses),
]