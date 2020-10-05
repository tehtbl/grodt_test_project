"""Testing utilities."""

import socket

from django.core import management
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
# from core import models as core_models
from users.models import MyUser

try:
    s = socket.create_connection(("127.0.0.1", 25))
    s.close()
    NO_SMTP = False
except socket.error:
    NO_SMTP = True


class MyTestCase(TestCase):
    """All test cases must inherit from this one."""

    @classmethod
    def setUpTestData(cls):  # noqa
        """Create a default user."""
        super().setUpTestData()
        management.call_command("load_initial_data")

    def setUp(self, username="admin", password="admin"):
        """Initiate test context."""
        self.assertEqual(
            self.client.login(username=username, password=password), True)

    def ajax_request(self, method, url, params=None, status=200):
        if params is None:
            params = {}

        response = getattr(self.client, method)(url, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, status)
        return response.json()

    def ajax_post(self, *args, **kwargs):
        return self.ajax_request("post", *args, **kwargs)

    def ajax_put(self, *args, **kwargs):
        return self.ajax_request("put", *args, **kwargs)

    def ajax_delete(self, *args, **kwargs):
        return self.ajax_request("delete", *args, **kwargs)

    def ajax_get(self, *args, **kwargs):
        return self.ajax_request("get", *args, **kwargs)


class MyAPITestCase(APITestCase):
    """All test cases must inherit from this one."""

    @classmethod
    def setUpTestData(self):  # noqa
        """Create a default user."""
        super().setUpTestData()
        management.call_command("load_initial_data")
        self.token = Token.objects.create(
            user=MyUser.objects.get(username="admin"))

    def setUp(self):
        """Setup."""
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
