from core.pagination import StandardPagination
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models.assignment import Assignment
from .models.submission import Submission
from .serializers.AssignmentSerializer import AssignmentSerializer
from .serializers.SubmissionSerializer import SubmissionSerializer
from .service.AssignmentService import validate_teacher_active
from .service.SubmissionService import handle_submission


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_assignment(request):
    teacher = request.user.teacher

    validate_teacher_active(teacher)

    serializer = AssignmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_assignments(request):
    course_id = request.query_params.get('course')

    queryset = Assignment.objects.all()

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(title__icontains=search)

    paginator = StandardPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serilizer = AssignmentSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serilizer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assignment(request, assignment_id):
    student = request.user.student

    assignment = Assignment.objects.filter(id=assignment_id).first()

    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    submission, action = handle_submission(student, assignment, file)

    serializer = SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(student=student, assignment=assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def grade_submission(request, submission_id):
    teacher = request.user.teacher

    submission = Submission.objects.filter(id=submission_id).first()

    if submission.assignment.teacher != teacher:
        return Response({"error": "You are not authorized to grade this submission."}, status=status.HTTP_403_FORBIDDEN)

    submission.grade = request.data.get('grade')
    submission.feedback = request.data.get('feedback')
    submission.save()

    return Response({"message": "Submission graded successfully."}, status=status.HTTP_200_OK)




