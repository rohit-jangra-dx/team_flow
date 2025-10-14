from rest_framework import serializers
from .models import Workspace
from projects.serializers import ProjectSerializer

class WorkspaceSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = Workspace
        fields = ["id", "name", "created_at", "projects"]
        read_only_fields = ["id", "created_at"]
    
    
