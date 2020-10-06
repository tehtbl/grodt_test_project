from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import MyAbstractModelObject
from users.models import MyUser


class MyNewAppModel(MyAbstractModelObject):
    name = models.CharField(_("Name"), max_length=100, unique=True)

    prvkey = models.CharField(_("Private Key"), max_length=32)
    pubkey = models.CharField(_("Public Key"), max_length=65)
    balance = models.FloatField(_("Balance"))

    class Meta:
        ordering = ["name"]
        app_label = "mynewapp"
        verbose_name = _("MyNewAppModel")
        verbose_name_plural = _("MyNewAppModels")

    def __init__(self, *args, **kwargs):
        super(MyNewAppModel, self).__init__(*args, **kwargs)

    @property
    def tags(self):
        return [
            {
                "name": self.balance,
                "label": self.balance,
                "type": "tag-item",
                "color": "warning"  # TODO
            }
        ]

    @property
    def admins(self):
        """Return the administrators of this Model.

        :return: a list of User objects
        """

        return MyUser.objects.filter(
            is_superuser=False,
            objectaccess__content_type__model="mynewappmodel",
            objectaccess__object_id=self.pk
        )

    def __str__(self):
        return f"{self.name}"
