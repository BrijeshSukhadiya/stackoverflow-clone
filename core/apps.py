from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Uses 64-bit integers for primary keys
    name = 'core'  # Name of the Django app

    def ready(self):
        # Imports signals when Django starts (for signal handlers)
        import core.signals