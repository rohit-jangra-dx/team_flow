from django.urls import reverse

from rest_framework import status 
from rest_framework.test import APITestCase
from rest_framework.exceptions import PermissionDenied

from accounts.models import CustomUser
from workspaces.models import Workspace, WorkspaceMember


class WorkspaceAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.owner = CustomUser.objects.create_user(username="owner", email="owner@example.com", password="password123")
        cls.other_user = CustomUser.objects.create_user(username="other", email="other@example.com", password="password123")
        cls.workspace = Workspace.objects.create(name="Workspace1", owner=cls.owner)
        cls.owner_member = WorkspaceMember.objects.get(user=cls.owner, workspace=cls.workspace)

    def setUp(self):
        self.client.force_authenticate(user=self.owner)
        
    
    def test_list_view(self):
        url = reverse("workspace-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Workspace1")
        
    
    def test_create_view(self):
        url = reverse("workspace-list-create")
        response = self.client.post(url, {"name": "New Workspace"})
        print(response.data)
        self.assertEqual(response.status_code, 201)
        
        ws = Workspace.objects.get(name="New Workspace")
        member = WorkspaceMember.objects.get(user=self.owner, workspace=ws)
        self.assertEqual(member.role, "owner")
        
    
    def test_workspace_details_permission(self):
        url = reverse("workspace-details", kwargs={"workspace_id": self.workspace.id})
        
        #owner can access
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        #other user cannot update
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(url, {"name": "Updated"})
        self.assertEqual(response.status_code, 403)