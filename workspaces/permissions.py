from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from .utils import get_workspace_from_view, get_workspace_member


class WorkspacePermission(BasePermission):
    """
    Permission for workspace-level actions.
    """
    
    def has_permission(self, request, view):
        workspace = get_workspace_from_view(view)
        if not workspace:
            return False 

        member = get_workspace_member(request.user, workspace)
        if not member:
            return False 
        
        #safe method -> any member can view
        if request.method in SAFE_METHODS:
            return member.can_view_workspace()
        
        #rest stuff
        return member.can_manage_workspace()
    
class WorkspaceInvitePermission(BasePermission):
    
    def has_permission(self, request, view):
        workspace = get_workspace_from_view(view)
        if not workspace:
            return False 

        member = get_workspace_member(request.user, workspace)
        if not member:
            return False 

        if request.method in SAFE_METHODS:
            return member.can_view_members()
        
        #now the power to invite people
        return member.can_invite() 