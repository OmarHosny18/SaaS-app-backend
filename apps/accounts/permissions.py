from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission that only allows the owner of an object to access it.
    Used in JobApplicationDetailView to prevent IDOR attacks.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminRole(BasePermission):
    """
    Allows access only to users with role='admin' or superusers.
    Superusers are never locked out of admin actions.
    Used in LessonCreateView and LessonUpdateDeleteView.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser