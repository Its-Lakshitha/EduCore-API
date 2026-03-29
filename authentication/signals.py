from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from student.models import Student

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        Student.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
            registration_number=f"REG{instance.id}"
        )