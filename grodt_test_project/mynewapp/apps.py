from django.apps import AppConfig


class MyNewAppConfig(AppConfig):

    name = "mynewapp"
    verbose_name = "MyNewApp Module"

    def ready(self):
        pass
        # load_mynewapp_settings()
        # from . import handlers  # NOQA:F401
