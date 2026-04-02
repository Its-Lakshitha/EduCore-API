from django.db import models


class StudentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    ENROLLED = 'ENROLLED', 'Enrolled'
    GRADUATED = 'GRADUATED', 'Graduated'
    DROPPED_OUT = 'DROPPED_OUT', 'Dropped Out'