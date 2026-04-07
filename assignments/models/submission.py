from django.db import models

from student.models import Student

from . import assignment
from assignments.enums.SubmissionStatus import SubmissionStatus


class Submission(models.Model):
    assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='assignments/')
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=SubmissionStatus.choices, default=SubmissionStatus.PENDING)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Submission by {self.student} for {self.assignment}'

    class Meta:
        unique_together = ('assignment', 'student')