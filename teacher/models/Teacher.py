from django.conf import settings
from django.db import models

from teacher.enums.TeacherStatus import TeacherStatus

User = settings.AUTH_USER_MODEL

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('teacher.Department', on_delete=models.SET_NULL, null=True, blank=True,)
    status = models.CharField(max_length=10, choices=TeacherStatus.choices, default=TeacherStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


