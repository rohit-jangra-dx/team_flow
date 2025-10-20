from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspaces.utils import get_workspace_from_view, get_workspace_member


class ProjectPermission(BasePermission):
    """
    Permission for project-level actions
    """
    
    def has_permission(self, request, view):
        workspace = get_workspace_from_view(view)
        if not workspace:
            return False
        
        member = get_workspace_member(request.user, workspace)
        if not member:
            return False
        
        if request.method in SAFE_METHODS:
            return member.can_view_project()
        
        return member.can_manage_project()