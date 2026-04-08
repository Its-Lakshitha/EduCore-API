from django.db import models


class SubmissionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    LATE = 'LATE', 'Late'
    SUBMITTED_ON_SPECIAL_EXTENSION = 'SUBMITTED_ON_SPECIAL_EXTENSION', 'Submitted on Special Extension',
    SUBMITTED_ON_EXTENSION = 'SUBMITTED_ON_EXTENSION', 'Submitted on Extension',
    GRADED = 'GRADED', 'Graded'