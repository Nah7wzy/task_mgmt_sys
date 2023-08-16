from rest_framework import permissions

class IsTaskCreatorOrAssignedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if the user is the task creator or assigned user
        return obj.created_by == request.user or obj.assigned_to == request.user
