from django.db import models

class EnrollmentStatus(models.TextChoices):
    ENROLLED = 'ENROLLED', 'Enrolled'
    COMPLETED = 'COMPLETED', 'Completed'
    DROPPED = 'DROPPED', 'Dropped'
    WAITLISTED = 'WAITLISTED', 'Waitlisted'
    CANCELLED = 'CANCELLED', 'Cancelled'