from django.apps import AppConfig


class UsersConfig(AppConfig):
    """App configuration."""

    name = "users"
    verbose_name = "Users Module"

    def ready(self):
        pass
