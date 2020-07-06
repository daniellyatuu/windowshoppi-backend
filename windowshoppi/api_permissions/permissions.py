from rest_framework.permissions import BasePermission


class IsExcAdminOrAdmin(BasePermission):
    message = "you don't have permission"
    def has_permission(self, request, view):
        
        allowed_groups = ['exc_admin', 'admin']
        active_user_group = request.user.group.name
        
        if active_user_group in allowed_groups:
            return True
        
