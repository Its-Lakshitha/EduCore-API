from django.db import models
from teacher.models import Teacher

from courses.models.course import Course


class Assignment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title