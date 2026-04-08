from django.db import models


class AssignmentExtension(models.Model):
    assignment = models.ForeignKey('assignment.Assignment', on_delete=models.CASCADE, related_name='extensions')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='assignment_extensions')
    extended_due_date = models.DateTimeField()
    reason = models.TextField()
    created_by = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE, related_name='created_extensions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"Extension for {self.assignment.title} by {self.student.name} (Teacher: {self.teacher.name})"