from django.urls import path

from .views import create_student, get_student, list_students

urlpatterns = [
    path('students/create', create_student),
    path('students/', list_students),
    path('students/<int:id>/', get_student),
    path('students/update/<int:id>', update_student),
    path('students/delete/<int:id>', delete_student),
    path('students/me', my_profile),
]