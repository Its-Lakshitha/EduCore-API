import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from common.pagination import StandardPagination
from courses.selectors.EnrollmentSelector import (
    get_student_courses as get_courses_for_student,
)
from courses.serializers import EnrollmentSerializer

from .enums.StudentStatus import StudentStatus
from .models import Student
from rest_framework.permissions import IsAuthenticated
from .permissions.StudentPermissions import IsActiveStudent, IsAdminOrReadOnly
from .serializers import StudentSerializer
from .services.StudentService import generated_registration_number


def validate_student(data):
    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required"

    if not data.get("email"):
        errors["email"] = "Email is required"

    return errors


# Create a new student
@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly])
@csrf_exempt
def create_student(request):

    data = request.data

    data['registration_number'] = generated_registration_number()

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all students
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_students(request):
    query = request.GET.get('search')

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# Get a student by ID
def get_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)

    if request.user.role == 'student' and request.user != student.user:
        return JsonResponse({
            "status": "error",
            "message": "Unauthorized"
        }, status=403)

    serializer = StudentSerializer(student)
    return Response(serializer.data)

# Get the profile of the currently authenticated student
@api_view(['GET'])
def my_profile(request):
    user = request.user

    if request.user.role != 'student':
        return JsonResponse({
            "status": "error",
            "message": "Unauthorized"
        }, status=403)

    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student profile not found"
        }, status=404)

    return JsonResponse({
        "status": "success",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "registration_number": student.registration_number,
        }
    })

# Update a student by ID
@api_view(['PUT'])
def update_student(request, id):
    user = request.user
    try:
        student = Student.objects.get(id=id)

        if request.method == "PUT":
            data = json.loads(request.body)

            student.name = data["name"]
            student.email = data["email"]
            if user.role == 'admin':
                student.registration_number = data.get(
                    "registration_number",
                    student.registration_number
                )
            student.created_at = data.get["created_at"]
            student.save()

            return JsonResponse({
                "status": "success",
                "message": "Student updated"
            })

    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)

# Delete a student by ID
@api_view(['DELETE'])
def delete_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)

    student.delete()

    return JsonResponse({
        "status": "success",
        "message": "Student deleted"
    })


@api_view(['PATCH'])
@permission_classes([IsAdminOrReadOnly])
def update_student_status(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)

    new_status = request.data.get("status")



    if new_status not in StudentStatus.values:
        return Response({"error": "Invalid status"}, status=400)

    student.status = new_status
    student.save()

    return JsonResponse({
        "status": "success",
        "message": "Student status updated"
    })

@api_view(['GET'])
@permission_classes([IsActiveStudent])
def my_courses(request):

    student = request.user.student

    queryset = get_courses_for_student(student.id).distinct()

    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(code__icontains=search))

    paginator = StandardPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = EnrollmentSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
