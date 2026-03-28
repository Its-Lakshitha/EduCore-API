from django.urls import path
from .views import create_student, list_students, get_student

urlpatterns = [
    path('students/create', create_student),
    path('students/', list_students),
    path('students/<int:id>/', get_student),
]