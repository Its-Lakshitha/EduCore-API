from teacher.choices import TeacherStatus


def validate_teacher_for_course(teacher):
    if teacher.status != TeacherStatus.ACTIVE:
        raise ValueError(f"Teacher {teacher.full_name} is not active and cannot be assigned to a course.")