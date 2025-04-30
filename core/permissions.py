from rest_framework import permissions

class IsAnswerAuthorOrReadOnly(permissions.BasePermission):
    """Only answer author can modify; others can view"""
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class IsQuestionAuthor(permissions.BasePermission):
    """Special permission for question authors (e.g., accepting answers)"""
    def has_permission(self, request, view):
        return True  # Allow access to view (object-level checks below)
    
    def has_object_permission(self, request, view, obj):
        return obj.question.author == request.user  # Only question owner can accept answers