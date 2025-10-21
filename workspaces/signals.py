from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workspace, WorkspaceMember

@receiver(post_save, sender=Workspace)
def create_workspace_member(sender, instance, created, **kwargs):
    if created:
        #BUG: joined_at and is_active is false by default
        WorkspaceMember.objects.create(user=instance.owner, workspace=instance, role="owner")