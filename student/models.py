from django.conf import settings
from django.db import models

from .enums.StudentStatus import StudentStatus

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=StudentStatus.choices, default=StudentStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
