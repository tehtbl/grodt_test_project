from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "core module"

    def ready(self):
        pass
