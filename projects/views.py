from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import Project
from .serializers import ProjectSerializer

from workspaces.models import Workspace

class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_workspace(self):
        workspace_id = self.kwargs["workspace_id"]
        workspace = Workspace.objects.filter(id=workspace_id, owner=self.request.user).first()
        if not workspace:
            raise NotFound("Workspace not found or you don't have permission.")
        return workspace

        
    def get_queryset(self):
        workspace = self.get_workspace()
        return Project.objects.filter(workspace=workspace).order_by('-created_at')

    def perform_create(self, serializer):
        workspace = self.get_workspace()
        serializer.save(workspace=workspace)
