from rest_framework.permissions import BasePermission

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