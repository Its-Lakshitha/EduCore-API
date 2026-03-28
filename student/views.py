import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Student


def validate_student(data):
    errors = {}

    if not data.get("name"):
        errors["name"] = "Name is required"

    if not data.get("age"):
        errors["age"] = "Age is required"

    if not data.get("email"):
        errors["email"] = "Email is required"

    return errors


@csrf_exempt
def create_student(request):
    if request.method == "POST":
        try:
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
                "data": {
                    "id": student.id
                }
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

def list_students(request):
    students = Student.objects.all()

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

def get_student(request, id):
    try:
        student = Student.objects.get(id=id)

        return JsonResponse({
            "status": "success",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "registration_number": student.registration_number,
            }
        })

    except Student.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Student not found"
        }, status=404)



# Create your views here.
