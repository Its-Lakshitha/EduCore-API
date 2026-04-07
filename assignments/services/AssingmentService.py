from teacher.enums.TeacherStatus import TeacherStatus


def validate_teacher_active(teacher):
    if teacher.status != TeacherStatus.ACTIVE:
        raise ValueError("Teacher is not active")