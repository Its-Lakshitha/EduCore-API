from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generated_registration_number(self):
        year = now().year

        last_student = Student.objects.filter(
            registration_number__startwith=f"STU-{year}"
        ).order_by('-registration_number').first()

        if last_student:
            last_number = int(last_student.registration_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"STU-{year}-{str(new_number).zfill(4)}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = self.generated_registration_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
