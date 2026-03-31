from django.db.models.signals import post_save
from django.dispatch import receiver
from teachers.models import Teacher

from authentication.models import User


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):

    if created:
        if instance.role == 'teacher':
            Teacher.objects.get_or_create(
                user=instance,
                defaults={
                    "full_name": instance.username,
                    "email": instance.email,
                    "employee_id": f"EMP-{instance.id}"
                }
            )
