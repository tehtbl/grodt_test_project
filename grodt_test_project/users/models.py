from core import constants as const_core
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import smart_text
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


#
#
#
class MyUser(AbstractUser):
    """Default user for GRODT Test Project.
    """

    username = models.CharField(_("Username"), max_length=255, unique=True)
    email = models.EmailField(_("E-Mail"), max_length=255, blank=True, db_index=True)
    password = models.CharField(_("Password"), max_length=256)

    is_staff = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    language = models.CharField(
        _("Language"),
        max_length=17,
        default=const_core.LanguageEnum.EN,
        choices=const_core.LanguageEnum.choices(),
    )

    class Meta(object):
        ordering = ["username"]
        index_together = [
            ["email", "is_active"]
        ]
        verbose_name = _("MyUser")
        verbose_name_plural = _("MyUsers")
        app_label = "users"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return smart_text(self.get_username())

    @property
    def enabled(self):
        return self.is_active

    def is_owner(self, obj):
        """Tell if the user is the unique owner of this object

        :param obj: an object inheriting from ``models.Model``
        :return: a boolean
        """
        ct = ContentType.objects.get_for_model(obj)

        try:
            ooentry = self.objectaccess_set.get(content_type=ct, object_id=obj.id)
        except ObjectAccess.DoesNotExist:
            return False

        return ooentry.is_owner

    def can_access(self, obj):
        """Check if the user can access a specific object

        This function is recursive: if the given user hasn't got
        direct access to this object and if he has got access to other
        ``User`` objects, we check if one of those users owns the
        object.

        :param obj: a admin object
        :return: a boolean
        """
        if self.is_superuser:
            return True

        ct = ContentType.objects.get_for_model(obj)
        try:
            ooentry = self.objectaccess_set.get(content_type=ct, object_id=obj.id)
        except ObjectAccess.DoesNotExist:
            pass
        else:
            return True

        if ct.model == "user":
            return False

        ct = ContentType.objects.get_for_model(self)
        qs = self.objectaccess_set.filter(content_type=ct)

        for ooentry in qs.all():
            if ooentry.content_object.is_owner(obj):
                return True

        return False

    @property
    def role(self):
        """Return user role."""
        if not hasattr(self, "_role"):
            if self.is_superuser:
                self._role = const_core.ROLE_SUPERADMINS[0]  # "SuperAdmins"
            else:
                try:
                    self._role = self.groups.all()[0].name
                except IndexError:
                    self._role = "---"
        return self._role

    @role.setter
    def role(self, role):
        """Set administrative role for this account

        :param string role: the role to set
        """

        if role is None or self.role == role:
            return

        self.groups.clear()
        if role == const_core.ROLE_SUPERADMINS[0]:  # "SuperAdmins":
            self.is_superuser = True
        else:
            if self.is_superuser or role == const_core.ROLE_SIMPLEUSERS[0]:  # "SimpleUsers":
                ObjectAccess.objects.filter(user=self).delete()

            self.is_superuser = False

            try:
                self.groups.add(Group.objects.get(name=role))
            except Group.DoesNotExist:
                self.groups.add(Group.objects.get(name="SimpleUsers"))

            if role != const_core.ROLE_SIMPLEUSERS[0] and not self.can_access(self):
                from lib.permissions import grant_access_to_object
                grant_access_to_object(self, self)

        self.save()
        self._role = role

    def get_role_display(self):
        """Return the display name of this role."""
        for role in const_core.ROLES:
            if role[0] == self.role:
                return role[1]
        return _("Unknown")

    @cached_property
    def is_admin(self):
        """Shortcut to check if user is administrator."""
        return self.role in const_core.ADMIN_GROUPS

    def post_create(self, creator):
        """Grant permission on this user to creator."""
        from lib.permissions import grant_access_to_object
        grant_access_to_object(creator, self, is_owner=True)

    def save(self, *args, **kwargs):
        creator = kwargs.pop("creator", None)
        super().save(*args, **kwargs)
        if creator is not None:
            self.post_create(creator)


#
#
#
class ObjectAccess(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    is_owner = models.BooleanField(default=False)

    class Meta(object):
        unique_together = (("user", "content_type", "object_id"),)
        verbose_name = _("ObjectAccess")
        verbose_name_plural = _("ObjectAccess")

    def __str__(self):
        return "%s => %s (%s)" % (
            self.user, self.content_object, self.content_type
        )
