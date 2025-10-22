from rest_framework.test import  APITestCase
from accounts.models import  CustomUser
from workspaces.models import  Workspace, WorkspaceMember

class PermissionsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = CustomUser.objects.create_user(username="owner", email="owner@example.com", password="password123")
        cls.admin = CustomUser.objects.create_user(username="admin", email="admin@example.com", password="password123")
        cls.member = CustomUser.objects.create_user(username="member", email="member@example.com", password="password123")

        cls.workspace = Workspace.objects.create(name="Workspace1", owner=cls.owner)

        # signal would create owner member automatically,
        cls.owner_member = WorkspaceMember.objects.get(user=cls.owner, workspace=cls.workspace)
        cls.admin_member = WorkspaceMember.objects.create(user=cls.admin, workspace=cls.workspace, role="admin",
                                                          joined_at="2025-01-01T00:00:00Z", is_active=True)
        cls.member_member = WorkspaceMember.objects.create(user=cls.member, workspace=cls.workspace, role="member",
                                                           joined_at="2025-01-01T00:00:00Z", is_active=True)

    def setup(self):
       self.client.force_authenticate(user=self.owner)
       
    def test_owner_permissions(self):
        self.assertEqual(self.owner_member.can_invite(), True)
        self.assertEqual(self.owner_member.can_manage_member("admin"), True)
        self.assertEqual(self.owner_member.can_manage_member("member"), True)
        self.assertEqual(self.owner_member.can_manage_project(), True)
        self.assertEqual(self.owner_member.can_manage_workspace(), True)
        self.assertEqual(self.owner_member.can_view_project(), True)
        self.assertEqual(self.owner_member.can_view_members(), True)
        self.assertEqual(self.owner_member.can_view_workspace(), True)
        
    
        
    