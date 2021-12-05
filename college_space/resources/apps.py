""" Resource App configuration."""

from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resources'

    def ready(self) -> None:
        #Signals to delete image and file field of resources.
        from resources import signals
        return super().ready()
