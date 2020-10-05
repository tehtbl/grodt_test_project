from enum import Enum, unique

from django.utils.translation import ugettext_lazy as _

LIST_MODEL_FIELD_EXCLUDES = ["uuidpk", "creation", "enabled"]


#
# Languages
#
@unique
class LanguageEnum(Enum):
    DE = _("Deutsch")
    EN = _("English")

    @classmethod
    def choices(cls):
        # return tuple((i, i.value) for i in cls)
        return tuple((i.name, i.value) for i in cls)


#
# Roles
#
ROLE_SIMPLEUSERS = ("SimpleUsers", _("Simple User"))
ROLE_NORMALADMINS = ("NormalAdmins", _("Normal Administrator"))
ROLE_SUPERADMINS = ("SuperAdmins", _("Super Administrator"))

ROLES = (
    ROLE_SIMPLEUSERS,
    ROLE_NORMALADMINS,
    ROLE_SUPERADMINS,
)

ADMIN_GROUPS = [
    "NormalAdmins",
    "SuperAdmins",
]

#
# Permissions
#
PERM_SIMPLEUSERS = []

PERM_NORMALADMINS = [
    # ["mydevops", "machine", "add_machine"],
    # ["mydevops", "machine", "change_machine"],
    # ["mydevops", "machine", "view_machine"],
    # ["mydevops", "machine", "delete_machine"],
]

PERM_SUPERADMINS = [
    ["users", "myuser", "add_myuser"],
    ["users", "myuser", "change_myuser"],
    ["users", "myuser", "delete_myuser"],
]
PERM_SUPERADMINS += PERM_SIMPLEUSERS
PERM_SUPERADMINS += PERM_NORMALADMINS

PERMISSIONS = {
    "SimpleUsers": PERM_SIMPLEUSERS,
    "NormalAdmins": PERM_NORMALADMINS,
    "SuperAdmins": PERM_SUPERADMINS,
}
