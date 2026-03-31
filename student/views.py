import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsStudent


def validate_student(data):
    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required"

    if not data.get("email"):
        errors["email"] = "Email is required"

    return errors


# Create a new student
@csrf_exempt
def create_student(request):
    user = request.user

    if request.method == "POST":
        try:
            if user.role != 'admin':
                return JsonResponse({
                    "status": "error",
                    "message": "Unauthorized user. Only admins can create students."
                }, status=403)

            data = json.loads(request.body)

            errors = validate_student(data)
            if errors:
                return JsonResponse({
                    "status": "error",
                    "errors": errors
                }, status=400)


            student = Student.objects.create(
                name=data["name"],
                email=data["email"],
                registration_number=data.get["registration_number"],
                created_at=data.get["created_at"]
            )

            return JsonResponse({
                "status": "success",
                "message": "Student created",
                "registration_number": student.registration_number,
            }, status=201)

        except IntegrityError:
            return JsonResponse({
                "status": "error",
                "message": "Email already exists"
            }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON"
            }, status=400)

# List all students
def list_students(request):
    query = request.GET.get('search')

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "registration_number": student.registration_number,
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })

# Get a student by ID
def get_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)

    if rquest.user.role == 'student' and request.user != student.user:
        return JsonResponse({
            "status": "error",
            "message": "Unauthorized"
        }, status=403)
    return JsonResponse({
        "status": "success",
        "data": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "registration_number": student.registration_number,
        }
    })

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
# Create your views here.
