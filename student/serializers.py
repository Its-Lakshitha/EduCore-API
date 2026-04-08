from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id','registration_number']