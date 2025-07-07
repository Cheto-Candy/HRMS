from rest_framework import permissions

class IsAdminOrHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.userprofile.role in ['Admin', 'HR']
        )

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.userprofile.role == 'Employee'
        )
