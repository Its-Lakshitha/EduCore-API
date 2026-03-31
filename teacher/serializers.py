from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authentication.models import User

from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        read_only_fields = ['user', 'employee_id', 'created_at']


class CreateTeacherSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    full_name = serializers.CharField(required=True)
    employee_id = serializers.CharField(required=True)
    specialization = serializers.CharField(required=False)
    department = serializers.CharField(required=False)

    # Required field validation
    def validate(self, data):
        if not data.get('username') or not data.get('email'):
            raise serializers.ValidationError("Username and Email are required")
        return data

    # Unique email validation
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    # Strong password validation
    def validate_password(self, value):
        validate_password(value)
        return value