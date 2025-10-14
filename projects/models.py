from django.db import models
from workspaces.models import Workspace


# Create your models here.
class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.workspace.name})"
    
    class Meta:
        ordering = ['-created_at']