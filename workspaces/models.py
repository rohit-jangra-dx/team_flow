from django.db import models
from accounts.models import CustomUser

    
# Create your models here.
class Workspace(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="workspaces", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.owner.email})"
    
    class Meta:
        unique_together = ("owner", "name")


class WorkspaceMember(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="workspace_memberships")
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    invited_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # becomes True once the invite is accepted

    class Meta:
        unique_together = ("user", "workspace")
