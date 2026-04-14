from django.db import models


class ExamSubmission(models.Model):
    exam = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='exam_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('exam', 'student')