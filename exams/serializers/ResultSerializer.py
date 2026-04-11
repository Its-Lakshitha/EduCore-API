from rest_framework import serializers

from exams.models.result import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['grade', 'is_passed', 'created_at', 'updated_at']