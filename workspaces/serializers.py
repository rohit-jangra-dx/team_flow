from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Workspace, WorkspaceMember
from projects.serializers import ProjectSerializer

class WorkspaceSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = Workspace
        fields = ["id", "name", "created_at", "projects"]
        read_only_fields = ["id", "created_at"]

class WorkspaceMemberSerialzier(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMember
        fields = '__all__'
        ready_only_fields = ["id", "invited_at", "workspace"]
        validators = [
            UniqueTogetherValidator(
                queryset=WorkspaceMember.objects.all(),
                fields=['user', 'workspace'],
                message="User is already a member of this workspace"
            )
        ]    

class WorkspaceMemberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMember
        fields = '__all__'
        read_only_fields = ["id", "invited_at", "user", "workspace"]