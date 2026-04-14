from django.utils.timezone import now

from exams.enums.ExamStatus import ExamStatus


class ExamService:

    @staticmethod
    def get_exam_status(exam, student):
        current_time = now()

        submission = exam.submissions.filter(student=student).first()

        if submission and submission.is_submitted:
            return ExamStatus.COMPLETED

        if current_time < exam.start_time:
            return ExamStatus.UPCOMING

        if exam.start_time <= current_time <= exam.end_time:
            return ExamStatus.ONGOING

        return ExamStatus.MISSED