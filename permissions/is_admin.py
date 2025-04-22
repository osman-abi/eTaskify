from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has admin role
        return request.user.is_authenticated and request.user.is_admin
