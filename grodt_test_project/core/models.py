import datetime
import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from users.models import ObjectAccess


class MyAbstractModelObjectManager(models.Manager):

    def get_for_admin(self, admin):
        if admin.is_superuser:
            return self.get_queryset()

        return self.get_queryset().filter(owners__user=admin)


class MyAbstractModelObject(models.Model):
    # https://stackoverflow.com/questions/3936182/using-a-uuid-as-a-primary-key-in-django-models-generic-relations-impact
    uuidpk = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    enabled = models.BooleanField(_("enabled"), help_text=_("Check to activate this Model"), default=True)

    creation = models.DateTimeField(default=timezone.now)
    last_modification = models.DateTimeField(auto_now=True)

    owners = GenericRelation(ObjectAccess)
    _objectname = None

    objects = MyAbstractModelObjectManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Custom constructor."""
        super(MyAbstractModelObject, self).__init__(*args, **kwargs)
        self._loaded_values = {}

    @classmethod
    def from_db(cls, db, field_names, values):
        """Store loaded values."""
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    @property
    def objectname(self):
        if self._objectname is None:
            return self.__class__.__name__

        return self._objectname

    @property
    def just_created(self):
        now = timezone.now()
        delta = datetime.timedelta(days=1)
        return self.creation + delta > now

    def add_admin(self, account):
        from lib.permissions import grant_access_to_object
        grant_access_to_object(account, self)

    def remove_admin(self, account):
        from lib.permissions import ungrant_access_to_object
        ungrant_access_to_object(self, account)

    def post_create(self, creator):
        from lib.permissions import grant_access_to_object
        grant_access_to_object(creator, self, is_owner=True)

    def save(self, *args, **kwargs):
        creator = kwargs.pop("creator", None)
        super(MyAbstractModelObject, self).save(*args, **kwargs)

        if creator is not None:
            self.post_create(creator)

    def delete(self):
        from lib.permissions import ungrant_access_to_object
        ungrant_access_to_object(self)
        super(MyAbstractModelObject, self).delete()
