from rest_framework.exceptions import ValidationError
from exams.models.result import Result
from .GradingService import calculate_grade

def create_or_update_result(student, exam, score):
    if not student.enrollments.filter(course=exam.course).exists():
        raise ValidationError("Student is not enrolled in the course for this exam.")

    grade, passed = calculate_grade(score, exam.total_marks)

    result, created = Result.objects.update_or_create(
        student=student,
        exam=exam,
        defaults={
            'score': score,
            'grade': grade,
            'is_passed': passed
        }
    )

    return result, created
