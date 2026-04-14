from django.db import models

from courses.models.course import Course
from exams.enums.ExamStatus import ExamStatus
from teacher.models.Teacher import Teacher


class Exam(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='exams')
    date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    total_marks = models.IntegerField()
    status = models.CharField(max_length=20, choices=ExamStatus.choices, default=ExamStatus.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title