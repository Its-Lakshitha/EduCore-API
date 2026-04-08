from django.utils import timezone
from rest_framework.exceptions import ValidationError

from student.enums.StudentStatus import StudentStatus

from .DeadlineService import get_effective_deadline
from assignments.models.submission import Submission


def determine_submission_status(assignment, student):
    deadline, source = get_effective_deadline(assignment, student)

    now = timezone.now()

    if now <= deadline:
        if source == "ORIGINAL":
            return Submission.Status.SUBMITTED
        elif source == "GLOBAL_EXTENSION":
            return Submission.Status.SUBMITTED_ON_EXTENSION
        elif source == "INDIVIDUAL_EXTENSION":
            return Submission.Status.SUBMITTED_ON_SPECIAL_EXTENSION

    return Submission.Status.LATE

def handle_submission(student, assignment, file):
    if student.status != StudentStatus.ACTIVE:
        raise ValueError("Student is not active")

    if not student.enrollments.filter(course=assignment.course).exists():
        raise ValidationError("Student is not enrolled in the course for this assignment")


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

