from rest_framework import permissions

class IsAnswerAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class IsQuestionAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return True  # allow access to view; we check object-level below

    def has_object_permission(self, request, view, obj):
        return obj.question.author == request.user
