from courses.models.course import Course


def get_all_courses():
    return Course.objects.select_related('teacher').all()

def get_course_by_id(id):
    return Course.objects.filter(id=id).select_related('teacher').first()