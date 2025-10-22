from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Workspace, WorkspaceMember
from .serializers import WorkspaceSerializer, WorkspaceMemberSerialzier, WorkspaceMemberDetailSerializer
from .permissions import WorkspacePermission, WorkspaceInvitePermission
from .utils import get_workspace_from_view, get_workspace_member
from .mixins import WorkspaceRoleCheckMixin


class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Workspace.objects.filter(owner=self.request.user)
            .order_by("-created_at")
            .prefetch_related("projects")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkspaceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated, WorkspacePermission]
    lookup_url_kwarg = "workspace_id"

    def get_queryset(self):
        workspace_pk = self.kwargs["workspace_id"]
        return Workspace.objects.filter(
            id=workspace_pk
        ).prefetch_related("projects")


class WorkspaceMemberListCreateView(
    WorkspaceRoleCheckMixin, generics.ListCreateAPIView
):
    serializer_class = WorkspaceMemberSerialzier
    permission_classes = [IsAuthenticated, WorkspaceInvitePermission]

    def get_queryset(self):
        return WorkspaceMember.objects.filter(workspace=self.kwargs["workspace_id"])

    def perform_create(self, serializer):
        """
        Right now it's playing with taking in the inviter's workspace id and putting it
        also the user it refrence to might not exist. so deal with it
        """
        # DES -> Non need to check if workspace, inviter exist or not, if that wasn't the case,
        # this code wouldn't be executed due to permission returning false

        workspace = get_workspace_from_view(self)
        inviter = get_workspace_member(self.request.user, workspace)

        target_role = self.request.data.get("role")

        if target_role and not inviter.can_manage_member(target_role):
            raise PermissionDenied(
                "You can't invite members with equal or heigher role."
            )

        serializer.save(workspace=workspace)


class WorkspaceMemberDetailsView(WorkspaceRoleCheckMixin ,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceMemberDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "member_id"
        
    def get_queryset(self):
        return WorkspaceMember.objects.filter(id=self.kwargs["member_id"])

    def perform_update(self, serializer):
        """
        First check if the user is eligible to update it or not
        and then do the updation
        """
        workspace, inviter, target_member = self.get_inviter_and_target()
        self.assert_can_manage(inviter, target_member)
        serializer.save(workspace=workspace)

    def perform_destroy(self, instance):
        """
        same as above i need to manually check if the inviter who is trying to update has
        authority or not
        """
        workspace, inviter, target_member = self.get_inviter_and_target()
        self.assert_can_manage(inviter, target_member)
        instance.delete()
