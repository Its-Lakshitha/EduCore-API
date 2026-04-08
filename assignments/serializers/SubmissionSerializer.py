from rest_framework import serializers

from assignments.models.submission import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'grade', 'feedback', 'version','status']