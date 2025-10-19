from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Workspace, WorkspaceMember
from .serializers import WorkspaceSerializer, WorkspaceMemberSerialzier
# Create your views here.

class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user).order_by('-created_at').prefetch_related('projects')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WorkspaceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        workspace_pk = self.kwargs["workspace_id"]
        return Workspace.objects.filter(owner=self.request.user, id=workspace_pk).prefetch_related('projects')
    
    def perform_update(self, serializer):
        serializer.save()
        
    def perform_destroy(self, instance):
        
        if instance.user != self.request.user:
            raise PermissionDenied("Only the owner can delete this permission")

        instance.delete()

class WorkspaceMemberListCreate(generics.ListCreateAPIView):
    serializer_class = WorkspaceMemberSerialzier
    permission_classes = [IsAuthenticated]
    
    
    
    
        
