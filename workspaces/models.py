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

