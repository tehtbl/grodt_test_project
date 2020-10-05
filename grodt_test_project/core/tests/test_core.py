from django.core import management
from django.test import TestCase


class ManagementCommandsTestCase(TestCase):
    """Test management commands."""

    def test_change_default_admin(self):
        """Use dedicated option."""
        management.call_command("load_initial_data", "--admin-username", "newadmin")
        self.assertTrue(self.client.login(username="newadmin", password="admin"))


# class AuthenticationTestCase(MyTestCase):
#     """Validate authentication scenarios."""
#
#     @classmethod
#     def setUpTestData(self):  # NOQA:N802
#         """Create test data."""
#         super().setUpTestData()
#         self.account = factories.UserFactory(
#             username="user@test.com", groups=("SimpleUsers",)
#         )
#
#     def test_authentication(self):
#         """Validate simple case."""
#         self.client.logout()
#         data = {"username": "user@test.com", "password": "toto"}
#         response = self.client.post(reverse("core:login"), data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url.endswith(reverse("core:user_index")))
#
#         response = self.client.post(reverse("core:logout"), {})
#         self.assertEqual(response.status_code, 302)
#
#         data = {"username": "admin", "password": "password"}
#         response = self.client.post(reverse("core:login"), data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url.endswith(reverse("core:dashboard")))
