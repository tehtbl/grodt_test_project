"""A management command to load initial data:

* Create a default super admin if none exists
* Create groups and permissions
"""

import logging
import os

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from lib.permissions import add_permissions_to_group
from users.models import MyUser as User

from ... import constants as const_core
from ...models import ObjectAccess

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command definition."""

    help = "Load initial data"  # NOQA:A003

    def add_arguments(self, parser):
        """Add extra arguments to command."""
        parser.add_argument(
            "--admin-username", default="admin",
            help="Username of the initial super administrator."
        )

    def handle(self, *args, **options):
        """Command entry point."""

        adminpw = os.getenv('MY_ADMINPW') or 'admin'
        userpw = os.getenv('MY_USRONEPW') or 'user1'

        if not User.objects.filter(is_superuser=True).count():
            admin = User.objects.create_superuser(
                username=options["admin_username"],
                email='admin@example.com',
                password=adminpw
            )
            ObjectAccess.objects.create(user=admin, content_object=admin, is_owner=True)

        user1 = User.objects.create_user(
            username="user1",
            email='user1@example.com',
            password=userpw
        )
        ObjectAccess.objects.create(user=user1, content_object=user1, is_owner=True)

        groups = list(const_core.PERMISSIONS.keys())
        for groupname in groups:
            group, created = Group.objects.get_or_create(name=groupname)
            permissions = const_core.PERMISSIONS.get(groupname, [])

            if not permissions:
                continue

            add_permissions_to_group(group, permissions)

        logger.info("user and permissions added")
