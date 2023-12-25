from django.apps import AppConfig


class FlashdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FlashDS'

    def ready(self):
        import FlashDS.signals

