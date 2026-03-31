from teachers.models import Teacher

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
