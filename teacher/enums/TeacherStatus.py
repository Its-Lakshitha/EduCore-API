from django.db import models


class TeacherStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    SUSPENDED = 'suspended', 'Suspended'