from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'apps.notification'

    def ready(self):
        import apps.notification.signals
