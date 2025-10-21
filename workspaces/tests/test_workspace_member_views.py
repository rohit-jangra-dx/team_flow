from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from accounts.models import CustomUser
from workspaces.models import Workspace, WorkspaceMember

class WorkspaceAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.owner = CustomUser.objects.create_user(username="owner", email="owner@example.com", password="password123")
        cls.admin = CustomUser.objects.create_user(username="admin", email="admin@example.com", password="password123")
        cls.member = CustomUser.objects.create_user(username="member", email="member@example.com", password="password123")

        cls.workspace = Workspace.objects.create(name="Workspace1", owner=cls.owner)
        
        # signal would create owner member automatically, 
        cls.owner_member = WorkspaceMember.objects.get(user=cls.owner, workspace=cls.workspace)
        cls.admin_member = WorkspaceMember.objects.create(user=cls.admin, workspace=cls.workspace, role="admin", joined_at="2025-01-01T00:00:00Z", is_active=True)
        cls.member_member = WorkspaceMember.objects.create(user=cls.member, workspace=cls.workspace, role="member", joined_at="2025-01-01T00:00:00Z", is_active=True)

    def setUp(self):
        self.client.force_authenticate(user=self.owner)
    
    def test_member_list(self):
        url = reverse("workspace-member-list-create", kwargs={"workspace_id": self.workspace.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)  # owner + admin + member

    def test_member_invite_permission(self):
        url = reverse("workspace-member-list-create", kwargs={"workspace_id": self.workspace.id})
        #owner invites new user
        new_user = CustomUser.objects.create_user(username="new", email="new@gmail.com", password="12345678")    
        response = self.client.post(url, {"user": new_user.id, "role": "member", "workspace":self.workspace.id})
        self.assertEqual(response.status_code, 201)
        
        #member can't invite, notice the same user used for invitation
        #this test passing means it won't even reach teh view logic layer
        self.client.force_authenticate(user=self.member)
        response = self.client.post(url, {"user": new_user.id, "role": "member"})
        self.assertEqual(response.status_code, 403)
    
        
    def test_member_update_delete_permission(self):
        url = reverse("workspace-member-details", kwargs={"workspace_id": self.workspace.id, "member_id": self.member_member.id})
        
        #Owner updates role 
        response = self.client.put(url,{"role": "admin"}) 
        self.assertEqual(response.status_code, 200)
        self.member_member.refresh_from_db()
        self.assertEqual(self.member_member.role, "admin")
        
        
        #owner deletes member
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WorkspaceMember.objects.filter(id=self.member_member.id).exists())
        
        