from django.db import models


class SubmissionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    LATE = 'LATE', 'Late'
    GRADED = 'GRADED', 'Graded'