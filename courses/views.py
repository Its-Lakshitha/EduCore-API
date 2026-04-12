from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from student.models import Student
from teacher.models import Teacher

from .models.course import Course
from .models.enrollment import Enrollment
from .permissions.DashboardPermissions import IsAdmin, IsTeacher
from .selectors.CourseSelector import get_all_courses
from .selectors.DashboardSelector import (
    get_courses_per_teacher,
)
from .selectors.EnrollmentSelector import (
    get_enrollments_by_student,
)
from .serializers import CourseSerializer, EnrollmentSerializer
from .services.CourseService import validate_teacher_for_course
from .services.EnrollmentService import enroll_student


@api_view(['POST'])
def create_course(request):
    data = request.data

    teacher_id = data.get("teacher")

    if teacher_id:
        teacher = Teacher.objects.get(id=teacher_id)

        try:
            validate_teacher_for_course(teacher)
        except ValueError:
            return Response({"error": "Teacher is not validated"}, status=400)

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        course = serializer.save()
        return Response(CourseSerializer(course).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_courses(request):
    courses = get_all_courses()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def enroll(request):
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    student = Student.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)

    try:
        enrollment = enroll_student(student, course)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

    return Response(EnrollmentSerializer(enrollment).data, status=201)

@api_view(['GET'])
def student_enrollments(request, student_id):
    user = request.user

    if user.role == 'student':
        student_id = user.student_profile.id
    else:
        student_id = request.GET.get('student_id')

    enrollments = get_enrollments_by_student(student_id=student_id)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdmin | IsTeacher])
def courses_per_teacher(request):
    user = request.user
    if user.role == 'teacher':
        data = get_courses_per_teacher(teacher_id=user.id)
    else:
        data = get_courses_per_teacher()

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAdmin | IsTeacher])
def students_per_course(request, course_id):
    enrollments = Enrollment.objects.filter(course_id=course_id).select_related('student')

    return Response([
        {"student": e.student.user.fullName}
        for e in enrollments
    ])

@api_view(['GET'])
def teachers_per_course(request):
    courses = Course.objects.select_related('teacher')

    return Response([
        {"course": c.name, "teacher": c.teacher.user.fullName if c.teacher else None}
        for c in courses
    ])