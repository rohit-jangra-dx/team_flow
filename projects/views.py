from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission

from workspaces.models import Workspace

class WorkspaceMixin:
    def get_workspace(self):
        workspace_id = self.kwargs["workspace_id"]
        return get_object_or_404(Workspace, id=workspace_id)

class ProjectListCreateView(WorkspaceMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ProjectPermission]
    serializer_class = ProjectSerializer
        
    def get_queryset(self):
        return Project.objects.filter(workspace=self.get_workspace()).order_by('-created_at')

    def perform_create(self, serializer):
        workspace = self.get_workspace()
        serializer.save(workspace=workspace)


class ProjectDetailsView(WorkspaceMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]
    
    def get_object(self):
        return get_object_or_404(
            Project, workspace= self.get_workspace(), id= self.kwargs["project_id"]
        )
    
    
        