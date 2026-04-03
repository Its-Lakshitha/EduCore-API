from django.db import models

from courses.enums.EnrollmentStatus import EnrollmentStatus


class Enrollment(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    enrollmentDate = models.DateTimeField(auto_now_add=True, verbose_name='Enrollment Date')
    status = models.CharField(
        max_length=20, choices=EnrollmentStatus.choices, default=EnrollmentStatus.ACTIVE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} enrolled in {self.course} - Status: {self.status}'