from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.pagination import StandardPagination
from teacher.enums.TeacherStatus import TeacherStatus

from .models.exam import Exam
from .models.result import Result
from .serializers.ExamSerializer import ExamSerializer
from .serializers.ResultSerializer import ResultSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam(request):
    teacher = request.user.teacher

    if teacher.status != TeacherStatus.ACTIVE:
        return Response({'error': 'Your account is not active. Please contact the administrator.'}, status=403)

    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_exams(request):
    queryset = Exam.objects.all()

    course = request.query_params.get("course")
    if course:
        queryset = queryset.filter(course__id=course)

    paginator = StandardPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = ExamSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_view(request, exam_id):
    student = request.user.student
    exam = get_object_or_404(Exam, id=exam_id)

    if not exam.course.enrollments.filter(student=student).exists():
        return Response({'error': 'You are not enrolled in the course for this exam.'}, status=403)

    serializer = ExamSerializer(exam, context={'student': student})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_result(request, exam_id):
    teacher = request.user.teacher
    exam = get_object_or_404(Exam, id=exam_id)

    if exam.teacher != teacher:
        return Response({'error': 'You do not have permission to add results to this exam.'}, status=403)

    serializer = ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(exam=exam)
        return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_results(request):
    student = request.user.student
    results = Result.objects.filter(student=student)
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)