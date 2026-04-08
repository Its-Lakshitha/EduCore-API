from rest_framework.permissions import BasePermission

from student.models import StudentStatus


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects, but allow read-only access to everyone.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET']:
            return True

        # Write permissions are only allowed to the admin user.
        return request.user.is_staff

class IsActiveStudent(BasePermission):
    """
    Custom permission to only allow active students to access certain views.
    """

    def has_permission(self, request, view):
        try:
            return request.user.student_profile.status == StudentStatus.ACTIVE
        except AttributeError:
            return False