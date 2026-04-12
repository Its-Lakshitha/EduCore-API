from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff

class IsTeacher(BasePermission):
    """
    Allows access only to teacher users.
    """

    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsStudent(BasePermission):
    """
    Allows access only to student users.
    """

    def has_permission(self, request, view):
        return request.user.role == 'student'