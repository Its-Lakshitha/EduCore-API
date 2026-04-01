import csv
from io import TextIOWrapper

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from authentication.models import User
from teacher.enums.TeacherStatus import TeacherStatus

from .models import Teacher
from .serializers import CreateTeacherSerializer, TeacherSerializer


# List all teachers
@api_view(['GET'])
def list_teachers(request):

    if request.user.role == 'student':
        return Response({"error": "Unauthorized user. Students cannot view teachers."}, status=403)

    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)


# Create a new teacher
@api_view(['POST'])
def create_teacher(request):

    if request.user.role != 'admin':
        return Response({"error": "Unauthorized user. Only admins can create teachers."}, status=403)

    serializer = CreateTeacherSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    # department is None
    # if data.get("department"):
    #     Department.objects.filter(name=data["department"]).first()

    # teacher = Teacher.objects.create(
    #     user=user,
    #     full_name=data['full_name'],
    #     email=data['email'],
    #     employee_id=data.get('employee_id', f"EMP-{user.id}"),
    #     specialization=data.get('specialization', ''),
    #     department=department
    # )
    #
    # return Response({
    #     "message": "Teacher created successfully",
    #     "teacher_id": teacher.id
    # })

    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Teacher created successfully", "data": data}, status=201)
    return Response(serializer.errors, status=400)

# Get a teacher by ID
@api_view(['GET'])
def get_teacher(request, id):

    if request.user.role == 'student':
        return Response({"error": "Unauthorized user. Students cannot view teachers."}, status=403)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)

    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)

# update teacher profile
@api_view(['PUT'])
def update_teacher(request, id):

    if request.user.role == 'student':
        return Response({"error": "Unauthorized user. Students cannot update teachers."}, status=403)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)

    if request.user != teacher.user:
        return Response({"error": "Unauthorized user. You can only update your own profile."}, status=403)

    serializer = TeacherSerializer(teacher, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Updated successfully", "data": serializer.data})
    return Response(serializer.errors, status=400)


# update teacher status
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_teacher_status(request, id):
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)

    new_status = request.data.get('status')

    if new_status not in TeacherStatus.values:
        return Response({"error": f"Invalid status. Valid options are: {', '.join(TeacherStatus.values)}"}, status=400)

    teacher.status = status
    teacher.save()
    return Response({"message": "Status updated successfully", "data": {"id": teacher.id, "status": teacher.status}})


#Delete a teacher by ID
@api_view(['DELETE'])
def delete_teacher(request, id):

    if request.user.role != 'admin':
        return Response({"error": "Unauthorized user. Only admin can delete teachers."}, status=403)

    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)

    teacher.delete()
    return Response({"message": "Deleted successfully"})


# Get the profile of the currently logged-in teacher
@api_view(['GET'])
def my_teacher_profile(request):

    if request.user.role != 'teacher':
        return Response({"error": "Unauthorized user. Only teachers can view their profile."}, status=403)

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher profile not found"}, status=404)

    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)



@api_view(['POST'])
def bulk_import_teachers(request):

    if request.user.role != 'admin':
        return Response({"error": "Only admin allowed"}, status=403)

    file = request.FILES.get('file')

    if not file:
        return Response({"error": "CSV file required"}, status=400)

    csv_file = TextIOWrapper(file.file, encoding='utf-8')
    reader = csv.DictReader(csv_file)

    created = []
    errors = []

    for row in reader:
        try:
            if User.objects.filter(email=row['email']).exists():
                errors.append(f"Email exists: {row['email']}")
                continue

            user = User.objects.create_user(
                username=row['username'],
                email=row['email'],
                password=row['password'],
                role='teacher'
            )

            teacher = Teacher.objects.create(
                user=user,
                full_name=row['full_name'],
                email=row['email'],
                specialization=row.get('specialization', ''),
                employee_id=f"TCH-{user.id}"
            )

            created.append(teacher.email)

        except Exception as e:
            errors.append(str(e))

    return Response({
        "created": created,
        "errors": errors
    })