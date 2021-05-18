from django.apps import AppConfig


class BulkManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bulk_manager'

    def ready(self):
        from . import signals
