from django.urls import path 
from .views import ProjectListCreateView, ProjectDetailsView

urlpatterns = [
    path("workspaces/<int:workspace_id>/projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("workspaces/<int:workspace_id>/projects/<int:project_id>", ProjectDetailsView.as_view(), name="project-details")
]