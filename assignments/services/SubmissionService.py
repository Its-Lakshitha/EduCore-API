from django.utils import timezone
from rest_framework.exceptions import ValidationError

from student.enums.StudentStatus import StudentStatus

from .enums.SubmissionStatus import SubmissionStatus
from .models.submission import Submission
from .DeadlineService import determine_submission_status


def handle_submission(student, assignment, file):
    if student.status != StudentStatus.ACTIVE:
        raise ValueError("Student is not active")

    if not student.enrollments.filter(course=assignment.course).exists():
        raise ValidationError("Student is not enrolled in the course for this assignment")

    is_late = assignment.due_date < timezone.now()

    existing_submission = Submission.objects.filter(
        student=student,
        assignment=assignment
    ).first()

    status = determine_submission_status(assignment, student)

    if existing_submission:
        existing_submission.file = file
        existing_submission.version +=1
        existing_submission.status = status
        existing_submission.save()

        return existing_submission, 'updated'

    submission = Submission.objects.create(
        student=student,
        assignment=assignment,
        file=file,
        submitted_at=timezone.now()
    )

    return submission, 'created'