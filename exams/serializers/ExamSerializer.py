from rest_framework import serializers

from exams.models.exam import Exam
from exams.services.ExamService import ExamService


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

    def get_status(self, obj):
        student = self.context.get('student')
        return ExamService.get_exam_status(obj, student)