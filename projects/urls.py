from django.urls import path 
from .views import ProjectListCreateView

urlpatterns = [
    path("projects/<int:workspace_id>/", ProjectListCreateView.as_view(), name="project-list-create")
]