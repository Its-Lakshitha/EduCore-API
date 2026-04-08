
def get_effective_deadline(assignment, student):

    student_extension = assignment.extensions.filter(
        student=student,
        is_active=True,
    ).order_by('-created_at').first()

    if student_extension:
        return student_extension.extended_due_date, "Individual Extension"

    global_extension = assignment.global_extensions.filter(
        student_isnull=True,
        is_active=True,
    ).order_by('-created_at').first()

    if global_extension:
        return global_extension.extended_due_date, "Global Extension"

    return assignment.due_date, "Original Deadline"