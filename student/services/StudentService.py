from django.utils.timezone import now

from student.models import Student


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