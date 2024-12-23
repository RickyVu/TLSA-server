from rest_framework.permissions import BasePermission, IsAuthenticated


class IsStudent(BasePermission):
    """Allow access only to students."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsTeacher(BasePermission):
    """Allow access only to teachers."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsManager(BasePermission):
    """Allow access only to lab manager."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsTeachingAffairs(BasePermission):
    """Allow high clearance access to system."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teachingAffairs'
