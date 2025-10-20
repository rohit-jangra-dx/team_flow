from .models import Workspace, WorkspaceMember

def get_workspace_from_view(view):
    """
    Try to get the Workspace instance from a view.
    """
    if hasattr(view, "get_workspace"):
        workspace = view.get_workspace()
        if workspace:
            return workspace
    
    #Fallback to direct url kwarg
    workspace_id = view.kwargs.get("workspace_id")
    if workspace_id:
        return Workspace.objects.filter(id=workspace_id).first()

    return None 

def get_workspace_member(user, workspace):
    """
    Returns the WorkspaceMember record for the given user/workspace pair
    """
    if not user or not workspace:
        return None 

    try:
        return WorkspaceMember.objects.get(user=user, workspace=workspace)
    except WorkspaceMember.DoesNotExist:
        return None 
