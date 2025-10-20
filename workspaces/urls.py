from django.urls import path

from .views import WorkspaceListCreateView, WorkspaceDetailsView, WorkspaceMemberListCreateView

urlpatterns = [
    path('workspaces/', WorkspaceListCreateView.as_view(), name="workspace-list-create"),
    path('workspaces/<int:workspace_id>/', WorkspaceDetailsView.as_view(), name="workspace-details"),
    
    # dealing with members invites and stuff
    path('workspaces/<int:workspace_id>/members', WorkspaceMemberListCreateView.as_view(), name="workspace-member-list-create"),
    path('workspaces/<int:workspace_id>/members/<int:member_id>/')
]