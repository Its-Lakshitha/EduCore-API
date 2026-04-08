def notify_students_extension(extension):
    if extension.student:
        student = extension.student
        # Send notification to the student about the extension
        print(f"Notify {student.id}: Deadline extended")

    else:
        students = extension.assignment.course.enrollments.all()
        for enrollment in students:
            student = enrollment.student
            # Send notification to each student about the extension
            print(f"Notify {student.id}: Deadline extended.")