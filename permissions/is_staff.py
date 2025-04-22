from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """
    Custom permission to only allow staff users to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has staff role
        return request.user.is_authenticated and request.user.is_staff
