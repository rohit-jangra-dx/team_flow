from .views import WorkspaceListCreateView, WorkspaceDetailsView
from django.urls import path, include

urlpatterns = [
    path('workspaces/', WorkspaceListCreateView.as_view(), name="workspace-list-create"),
    path('workspaces/<int:workspace_id>/', WorkspaceDetailsView.as_view(), name="workspace-details"),
]