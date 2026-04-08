from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User
from student.models import Student
from teacher.models.Teacher import Teacher


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        Student.objects.get_or_create(
            user=instance,
            name=instance.username,
            email=instance.email,
            registration_number=f"REG{instance.id}"
        )


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):

    if created and instance.role == 'teacher':
            Teacher.objects.get_or_create(
                user=instance,
                full_name=instance.username,
                email=instance.email,
                employee_id=f"EMP-{instance.id}"
            )
