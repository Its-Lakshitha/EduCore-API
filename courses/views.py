from selectors.course_selector import get_all_courses
from selectors.enrollment_selector import get_enrollments_by_student

from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.enrollment_service import enroll_student

from student.models import Student

from .models.course import Course
from .serializers import CourseSerializer, EnrollmentSerializer


@api_view(['POST'])
def create_course(request):
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
    enrollments = get_enrollments_by_student(student_id)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)