from django.db import models


class EnrollmentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    ENROLLED = 'ENROLLED', 'Enrolled'
    COMPLETED = 'COMPLETED', 'Completed'
    DROPPED = 'DROPPED', 'Dropped'
    WAITLISTED = 'WAITLISTED', 'Waitlisted'
    CANCELLED = 'CANCELLED', 'Cancelled'