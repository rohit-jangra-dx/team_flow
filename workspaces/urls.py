from .views import WorkspaceListCreateView
from django.urls import path, include

urlpatterns = [
    path('workspaces/', WorkspaceListCreateView.as_view(), name="workspace-list-create")
]