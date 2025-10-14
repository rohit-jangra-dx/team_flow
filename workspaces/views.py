from rest_framework import generics, permissions
from .models import Workspace
from .serializers import WorkspaceSerializer
# Create your views here.

class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user).order_by('-created_at').prefetch_related('projects')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        