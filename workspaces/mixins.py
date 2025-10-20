from rest_framework.exceptions import PermissionDenied

from .models import WorkspaceMember
from .utils import get_workspace_from_view, get_workspace_member

class WorkspaceRoleCheckMixin:
    def get_inviter_and_target(self):
        workspace = get_workspace_from_view(self)
        if not workspace:
            raise PermissionDenied("Workspace does not exist")
        
        inviter = get_workspace_member(self.request.user, workspace)
        if not inviter:
            raise PermissionDenied("You are not part of this workspace")

        target_member = get_object_or_404(WorkspaceMember, id=self.kwargs["member_id"])
        return workspace, inviter, target_member

    def assert_can_manage(self, inviter, target_member):
        if not inviter.can_manage_member(target_member.role):
            raise PermissionDenied("You don't have enough authority to perform this operation")
